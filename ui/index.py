# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：index.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/13 13:37

首页 设置 阵容 更新 使用说明 交流群
"""
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
from time import sleep
import json
from PySide6.QtGui import QIcon, QPixmap, QImage, QTextCursor, QColor, QPainter, QPen, QFont, QFontMetrics, QPalette, \
    QCursor
from PySide6.QtCore import Qt, QSize, QRectF, Property, QPointF, Signal, QThread, QTimer, QThreadPool, QRunnable, QRect, \
    QProcess, QPoint, QDir
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QTableWidget, \
    QSpacerItem, QSizePolicy, QLabel, QWidget, QHeaderView, QButtonGroup, QCompleter, QStyle, QStyleOptionButton, \
    QLayout, QGridLayout, QLineEdit, QListWidget
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, CardWidget, AvatarWidget, \
    TableWidget, TextEdit, TogglePushButton, FluentIcon, PrimaryPushButton, SimpleCardWidget, BodyLabel, LineEdit, \
    VerticalSeparator, ProgressRing, ProgressBar, isDarkTheme, PushButton, InfoBar, InfoBarPosition, IconInfoBadge, \
    ToolButton, InfoBadge, InfoBadgePosition, IconWidget, InfoBarIcon, SmoothMode, ElevatedCardWidget, RadioButton, \
    ComboBox, EditableComboBox, SwitchButton, CheckBox, Icon, MessageBox, MessageBoxBase
from qfluentwidgets import FluentIcon as FIF
from requests import RequestException

import game_assets
from service import LOLService

lol = LOLService()  # 客户端服务


class RadialGauge(ProgressBar):
    """ 重绘进度环，并预留中心容器位置 """

    def __init__(self, parent=None, useAni=True):
        super().__init__(parent, useAni=useAni)
        self.lightBackgroundColor = QColor(0, 0, 0, 34)
        self.darkBackgroundColor = QColor(255, 255, 255, 34)
        self._strokeWidth = 7
        self.setTextVisible(False)  # 禁用文本显示
        self.setFixedSize(200, 200)
        self.containerSize = 200  # 容器大小（宽高）
        self.bottomText = ""
        setFont(self)

        # 创建中心容器控件
        self.centerWidget = QWidget(self)  # 使用 QWidget 作为容器
        # 使用垂直布局管理器
        self.center = QVBoxLayout(self)
        self.center.addWidget(self.centerWidget, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.center.setContentsMargins(15, 0, 0, 15)  # 调整中心

        self.updateCenterWidgetPosition()

    def getCenterContainerRect(self):
        """ 获取中心容器的矩形区域 """
        centerX = self.width() / 2 - self.containerSize / 2
        centerY = self.height() / 2 - self.containerSize / 2
        return QRectF(centerX, centerY, self.containerSize, self.containerSize)

    def updateCenterWidgetPosition(self):
        """ 更新中心容器控件的位置 """
        centerRect = self.getCenterContainerRect()
        self.centerWidget.setGeometry(centerRect.toRect())

    def resizeEvent(self, e):
        """ 在窗口大小改变时更新中心容器位置 """
        super().resizeEvent(e)
        self.updateCenterWidgetPosition()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth  # 圆环厚度
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw / 2, self.height() / 2 - w / 2, w, w)

        # 绘制背景环
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 240 * 16, -300 * 16)  # 背景环

        if self.maximum() <= self.minimum():
            return

        # 绘制进度条
        pen.setColor(self.barColor())
        painter.setPen(pen)
        degree = int(self.val / (self.maximum() - self.minimum()) * 300)
        painter.drawArc(rc, 240 * 16, -degree * 16)  # 进度条

        font = QFont("微软雅黑", 9)
        font.setBold(True)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.2)
        fm = QFontMetrics(font)
        textRect = fm.boundingRect(self.bottomText)
        textPos = QPointF(
            rc.center().x() - textRect.width() / 2,  # 水平方向居中
            (rc.center().y() + textRect.height() / 2) + self.height() / 2.5  # 垂直方向在中心正下方
        )
        painter.setFont(font)
        painter.drawText(textPos, self.bottomText)


class Widget(QFrame):
    """示例"""

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Home(QFrame):
    """首页"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.timer = None
        self.thread = None
        self.lock = threading.Lock()
        self.setObjectName("首页")

        self.vBoxLayout = QVBoxLayout(self)  # 垂直布局

        self.userInfoModule = HomeUserInfo(self)  # 用户信息模块
        self.consoleModule = HomeConsole(self)  # 控制台模块

        self.vBoxLayout.addWidget(self.userInfoModule)
        self.vBoxLayout.addWidget(self.consoleModule)

        self.connectClientClicked()

    def connectClientClicked(self):
        QThreadPool.globalInstance().setMaxThreadCount(1)  # 限制并发数
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_refresh_thread)
        self.timer.start(10000)  # 刷新时间10秒

    def start_refresh_thread(self):
        task = RefreshTask(self.userInfoModule.updateData)
        QThreadPool.globalInstance().start(task)

    def info_log(self, msg: str) -> None:
        """给首页控制台添加信息"""
        current_html = self.consoleModule.textEdit.toHtml()
        new_log = f'<h3 style="color:#7a7374">[信息] {msg}</h3>'
        updated_html = current_html + new_log
        self.consoleModule.textEdit.setHtml(updated_html)

    def success_log(self, msg: str) -> None:
        """给首页控制台添加信息"""
        current_html = self.consoleModule.textEdit.toHtml()
        new_log = f'<h3 style="color:#12aa9c">[信息] {msg}</h3>'
        updated_html = current_html + new_log
        self.consoleModule.textEdit.setHtml(updated_html)


class HomeUserInfo(CardWidget):
    """首页用户信息"""
    # connectClientClickEmit = Signal()  # 信号
    def __init__(self, parent=None):
        super().__init__(parent)
        self.avatar = None
        self.rg = None
        self.vBoxLayout = None
        self.hBoxLayout = None

        self.hBoxLayout = QHBoxLayout(self)  # 水平布局
        self.vBoxLayout = QVBoxLayout(self)  # 垂直布局

        # 玩家等级进度环
        self.rg = RadialGauge()
        self.rg.setFixedSize(120, 120)
        self.rg.setMaximum(lol.xpUntilNextLevel)
        self.rg.setValue(lol.xpSinceLastLevel)
        # 等级
        self.rg.bottomText = str(lol.summonerLevel)
        # 玩家头像
        self.avatar = AvatarWidget()
        if lol.avatar is None:
            image = QImage("icon/default.jpg")  # 默认头像
        else:
            image = QImage()
            image.loadFromData(lol.avatar)

        scaled_image = image.scaled(90, 90)  # 缩放图片
        self.avatar.setPixmap(QPixmap.fromImage(scaled_image))

        self.rg.center.addWidget(self.avatar)  # 把头像放入进度环

        self.vBoxLayout.addWidget(self.rg, alignment=Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout.addLayout(self.vBoxLayout)

        # 构建用户信息展示
        self.userInfoVBox = QVBoxLayout(self)  # 垂直布局
        self.userInfoVBox.setSpacing(0)  # 移除子控件间的垂直间距
        self.userInfoVBox.setContentsMargins(0, 0, 0, 0)  # 移除布局与父容器的边距
        self.passName = QLabel(lol.pass_name)  # 通行证名称
        self.passName.setStyleSheet("font-size: 20px;")  # 设置字体大小
        self.userInfoVBox.addWidget(self.passName, alignment=Qt.AlignmentFlag.AlignCenter)

        self.passNum = QLabel(str(lol.currentLevel))  # 通行证等级
        self.passNum.setStyleSheet("""
            font-size: 20px;
            color: #cb2326;
            font-weight: bold;      
        """)

        self.userInfoVBox.addWidget(self.passNum, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.passLevel = ProgressBar()  # 通行证进度条
        self.passLevel.setFixedHeight(6)
        self.passLevel.setCustomBarColor(QColor(165, 71, 66), QColor(165, 71, 66))
        self.passLevel.setMaximum(int(lol.totalLevelXP))
        self.passLevel.setValue(int(lol.currentLevelXP))
        self.userInfoVBox.addWidget(self.passLevel, alignment=Qt.AlignmentFlag.AlignTop)

        # 货币显示
        self.currencyHBox = QHBoxLayout(self)  # 水平布局
        self.currencyBlueLabel = QLabel("蓝色精粹：")
        self.currencyBlueLabel.setStyleSheet("""
            font-size: 18px;
            color: #0AC8E6;
            font-weight: bold;
        """)
        self.currencyBlueNumLabel = QLabel(str(lol.lol_blue_essence))
        self.currencyBlueNumLabel.setStyleSheet("""
            font-size: 18px;
            color: #0AC8E6;
            font-weight: bold;
        """)
        self.currencyHBox.addWidget(self.currencyBlueLabel)
        self.currencyHBox.addWidget(self.currencyBlueNumLabel)

        self.currencyOrangeLabel = QLabel("橙色精粹：")
        self.currencyOrangeLabel.setStyleSheet("""
            font-size: 18px;
            color: #DB9130;
            font-weight: bold;
        """)
        self.currencyOrangeNumLabel = QLabel(str(lol.lol_orange_essence))
        self.currencyOrangeNumLabel.setStyleSheet("""
            font-size: 18px;
            color: #DB9130;
            font-weight: bold;
        """)
        self.currencyHBox.addWidget(self.currencyOrangeLabel)
        self.currencyHBox.addWidget(self.currencyOrangeNumLabel)

        self.userInfoVBox.addLayout(self.currencyHBox)

        self.hBoxLayout.addLayout(self.userInfoVBox)

        # 状态数据展示容器
        self.startInfo = HomeStateInfo()
        self.startInfo.setMaximumWidth(165)
        self.startInfo.setMinimumWidth(165)
        self.hBoxLayout.addWidget(self.startInfo, Qt.AlignmentFlag.AlignRight)

    def updateData(self):
        print("刷新数据")
        # 更新头像
        if lol.avatar is None:
            image = QImage("icon/default.jpg")  # 默认头像
        else:
            image = QImage()
            image.loadFromData(lol.avatar)
        scaled_image = image.scaled(90, 90)  # 缩放图片
        self.avatar.setPixmap(QPixmap.fromImage(scaled_image))

        if not self.rg.maximum() == lol.xpUntilNextLevel:
            self.rg.setMaximum(int(lol.xpUntilNextLevel))

        if not self.rg.getVal() == lol.xpSinceLastLevel:
            self.rg.setValue(int(lol.xpSinceLastLevel))

        if not self.rg.bottomText == str(lol.summonerLevel):
            self.rg.bottomText = str(lol.summonerLevel)

        # 更新通行证名称
        if not self.passName.text() == lol.pass_name:
            self.passName.setText(lol.pass_name)  # 通行证名称

        # 更新通行证等级
        if not self.passNum.text() == str(lol.currentLevel):
            self.passNum.setText(str(lol.currentLevel))  # 通行证等级

        # 更新通行证经验条
        if not self.passLevel.maximum() == int(lol.totalLevelXP):
            self.passLevel.setMaximum(int(lol.totalLevelXP))
        if not self.passLevel.getVal() == int(lol.currentLevelXP):
            self.passLevel.setValue(int(lol.currentLevelXP))

        # 更新货币
        if not self.currencyBlueNumLabel.text() == str(lol.lol_blue_essence):
            self.currencyBlueNumLabel.setText(str(lol.lol_blue_essence))

        if not self.currencyOrangeNumLabel.text() == str(lol.lol_orange_essence):
            self.currencyOrangeNumLabel.setText(str(lol.lol_orange_essence))


class HomeStateInfo(SimpleCardWidget):
    """程序运行状态"""

    def __init__(self, parent=None):
        super().__init__(parent)


        self.vBoxLayout = QVBoxLayout(self)

        self.table = TableWidget(self)

        self.table.setWordWrap(True)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(TableWidget.SelectionMode.NoSelection)

        # 隐藏滚动条
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 内容自适应
        self.table.resizeColumnsToContents()

        self.table.setRowCount(6)
        self.table.setColumnCount(1)

        self.table.setItem(0, 0, QTableWidgetItem(f'对局次数:\t{1}'))
        self.table.setItem(1, 0, QTableWidgetItem(f'挂机模式:\t{"匹配"}'))
        self.table.setItem(2, 0, QTableWidgetItem(f'自动投降:\t{"禁用"}'))
        self.table.setItem(3, 0, QTableWidgetItem(f'自动关机:\t{"禁用"}'))
        self.table.setItem(4, 0, QTableWidgetItem(f'使用显卡:\t{"关闭"}'))
        self.table.setItem(5, 0, QTableWidgetItem(f'打完暂停:\t{"关闭"}'))

        self.table.resizeColumnsToContents()
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()

        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.vBoxLayout.addWidget(self.table)



class HomeConsole(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.vBoxLayout = QVBoxLayout(self)  # 垂直布局
        self.hBoxLayout = QHBoxLayout(self)  # 水平布局
        self.status = False # 脚本启动状态
        # 日志展示
        self.textEdit = TextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.textEdit.textBackgroundColor()

        # 启动按钮
        self.startButton = PrimaryPushButton(FluentIcon.PLAY, '启动程序')
        self.startButton.setStyleSheet(f"""
                        {self.startButton.styleSheet()}
                        PrimaryPushButton {{
                            border-radius: 10px;
                        }}""")

        self.startButton.setFixedSize(180, 35)
        self.startButton.clicked.connect(self.start_button_clicked)

        self.hBoxLayout.addStretch()  # 占据左侧空间
        self.hBoxLayout.addWidget(self.startButton)

        # 构建布局
        self.vBoxLayout.addWidget(self.textEdit)
        self.vBoxLayout.addLayout(self.hBoxLayout)

    def handle_stdout(self):
        # output = self.process.readAllStandardOutput().data().decode()
        while self.process.canReadLine():  # 按行读取
            output = self.process.readLine().data().decode().strip()

            current_html = self.textEdit.toHtml()
            # 构造新的日志内容
            new_log = f'<h3 style="color:#352A29">[信息] {output} </h3>'
            # 检查是否是初始空内容
            if self.textEdit.toPlainText() == '':
                updated_html = new_log
            else:
                updated_html = current_html + new_log
            # 设置更新后的 HTML 内容
            self.textEdit.setHtml(updated_html)
            # 滚动到底部以显示最新内容
            self.scroll_to_bottom()

    def handle_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        # print("[脚本错误]", error)
        current_html = self.textEdit.toHtml()
        # 构造新的日志内容
        new_log = f'<h3 style="color:#F8231D">[错误] {error} </h3>'
        # 检查是否是初始空内容
        if self.textEdit.toPlainText() == '':
            updated_html = new_log
        else:
            updated_html = current_html + new_log
        # 设置更新后的 HTML 内容
        self.textEdit.setHtml(updated_html)
        # 滚动到底部以显示最新内容
        self.scroll_to_bottom()


    def start_button_clicked(self):

        current_html = self.textEdit.toHtml()
        # 构造新的日志内容
        new_log = f''


        if self.status:
            # 结束游戏脚本
            if self.process.state() == QProcess.ProcessState.Running:
                    self.process.kill()  # 强制终止
                    self.process.waitForFinished(1000)  # 再给1秒清理时间
            new_log = f'<h3 style="color:#EA6334">[信息] 脚本已停止 </h3>'
            print("脚本已停止")

            self.status = False
            self.startButton.setIcon(FluentIcon.PLAY)
            self.startButton.setText("启动程序")
            original_style = self.startButton.styleSheet()
            self.startButton.setStyleSheet(f"""
                {original_style}
                PrimaryPushButton {{
                    background-color: #009FAA;
                    border: 1px solid #009FAA;  /* 同步边框与背景色 */
                }}
                
                PrimaryPushButton:hover {{
                    background-color: #00A7B3;  
                    border: 1px solid #00A7B3;  /* 悬停状态边框 */
                }}
                PrimaryPushButton:pressed {{
                    background-color: #3EABB3;   /* 按压状态颜色 */
                    border: 1px solid #3EABB3;
                }}
            """)

        else:
            # 运行游戏脚本
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 获取项目根目录路径
            main_script = os.path.join(project_root, "main.py")
            self.process.start(sys.executable, [main_script])
            new_log = f'<h3 style="color:#EA6334">[信息] 脚本已启动 </h3>'
            print("脚本已启动")

            self.status = True
            self.startButton.setIcon(FluentIcon.POWER_BUTTON)
            self.startButton.setText("结束程序")
            original_style = self.startButton.styleSheet()
            self.startButton.setStyleSheet(f"""
                {original_style}
                PrimaryPushButton {{
                    background-color: #A81113;
                    border: 1px solid #A81113;  /* 同步边框与背景色 */
                }}
                PrimaryPushButton:hover {{
                    background-color: #AD1618;  
                    border: 1px solid #AD1618;  /* 悬停状态边框 */
                }}
                PrimaryPushButton:pressed {{
                    background-color: #B46464;   /* 按压状态颜色 */
                    border: 1px solid #B46464;
                }}
            """)

        # 输出内容到UI控制台
        if self.textEdit.toPlainText() == '':
            updated_html = new_log
        else:
            updated_html = current_html + new_log
        # 设置更新后的 HTML 内容
        self.textEdit.setHtml(updated_html)
        # 滚动到底部以显示最新内容
        self.scroll_to_bottom()


    def scroll_to_bottom(self):
        """
        滚动到 TextEdit 的底部
        """
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)  # 正确引用 QTextCursor.End
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()


class RefreshClientThread(QThread):
    """用户刷新客户端信息"""
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTerminationEnabled(True)

    def run(self):
        try:
            lol.refresh_client()
            print("刷新客户端")
            self.finished.emit()
        finally:
            self.quit()  # 确保线程退出

class RefreshTask(QRunnable):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def run(self):
        lol.refresh_client()
        self.callback()


class Army(QFrame):
    def __init__(self, parent=None,rows=4,cols=7):
        super().__init__(parent=parent)
        self.setObjectName("阵容")

        # 创建主垂直布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(10)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # 添加水平布局（在网格布局上方）
        self.header_layout = QHBoxLayout()
        self.selectItem = EditableComboBox() # 下拉框
        self.selectItem.setPlaceholderText("选择或输入阵容配置")
        self.selectItem.setMaxVisibleItems(10)
        # 加载下拉框可用配置
        self.selectItem.addItems(self.loadSquadsList())
        self.selectItem.setCurrentIndex(-1)  # -1 表示无选中项
        self.selectItem.currentIndexChanged.connect(self.onSelectChanged) # 监听事件


        self.saveBtn = PrimaryPushButton(FluentIcon.SAVE,'保存')
        self.saveBtn.clicked.connect(self.saveClicked)
        self.restBtn = PushButton(FluentIcon.ERASE_TOOL,'重置')
        self.restBtn.clicked.connect(self.restClicked)
        self.deleteBtn = PushButton(FluentIcon.DELETE,'删除')
        self.deleteBtn.clicked.connect(self.deleteClicked)
        self.header_layout.addWidget(self.selectItem)
        self.header_layout.addWidget(self.saveBtn)
        self.header_layout.addWidget(self.restBtn)
        self.header_layout.addWidget(self.deleteBtn)
        mainLayout.addLayout(self.header_layout)  # 先添加水平布局

        # 创建网格布局
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(10)  # 设置项目之间的间距
        mainLayout.addLayout(self.grid_layout) # 再添加网格布局

        # 创建 HeroItem 实例并添加到网格中
        self.hero_items = []
        for row in range(rows):
            for col in range(cols):
                hero_item = HeroItem(parent=self, index=(rows - 1 - row) * cols + col)
                self.grid_layout.addWidget(hero_item, row, col)
                self.hero_items.append(hero_item)

    def loadSquadsList(self,squads_dir = "squads"):
        """加载配置文件"""
        path_dir = Path(__file__).parent.parent / squads_dir
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
            return []
        files = QDir(path_dir).entryList(["*.json"], QDir.Filter.Files)
        return [os.path.splitext(f)[0] for f in files]  # 去掉.json后缀

    def onSelectChanged(self,index):
        if index >= 0:
            print(self.selectItem.currentText())
            print("模拟执行加载文件")

    def saveClicked(self):
        print("保存按钮")
        pass

    def restClicked(self):
        print("清空按钮")
        pass

    def deleteClicked(self):
        print("删除按钮")
        pass




class HeroItem(CardWidget):
    def __init__(self, parent=None, index=None):
        super().__init__(parent)
        self.isContent = False # 是否已经被编辑过了
        self.index = index
        self.heroName = None
        self.items = []
        self.level = 2
        self.final_comp = False
        self.center = False

        self.vBoxLayout = QVBoxLayout(self)  # 垂直容器
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter) # 设置对齐方式

        # 使用 QLabel 显示图标
        self.iconLabel = QLabel()
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 获取 FluentIcon.ADD 的 QPixmap 并设置大小
        icon = Icon(FluentIcon.ADD)
        pixmap = icon.pixmap(QSize(16, 16))  #图标设置大小
        self.iconLabel.setPixmap(pixmap)

        # 添加到布局
        self.vBoxLayout.addWidget(self.iconLabel)

        # 设置鼠标样式为手型（表示可点击）
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


    # 添加鼠标点击事件
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"阵容编辑框 {self.index} clicked!")  # 示例：打印点击事件
            # 在这里添加你的点击逻辑
            self.onItemClicked()
        super().mousePressEvent(event)  # 确保父类事件仍能处

    def onItemClicked(self):
        """弹出英雄详细编辑对话框"""
        editItem = CustomHeroItemMessageBox(self.parent(),self)
        editItem.yesButton.setText("确定")
        editItem.cancelButton.setText("取消")

        if self.isContent:
            if editItem.heroNameInput.text().strip() != "未输入英雄名称":
                editItem.heroNameInput.setText(self.heroName)
            else:
                editItem.heroNameInput.setText('')

            editItem.weaponry1.setText(self.items[0])
            editItem.weaponry2.setText(self.items[1])
            editItem.weaponry3.setText(self.items[2])
            editItem.starGroup.buttons()[self.level-1].setChecked(True)
            editItem.center.setChecked(self.center)
            editItem.necessaryBtn.setChecked(self.final_comp)

        else:
            pass

        if editItem.exec():
            self.heroName = editItem.heroNameInput.text().strip()
            self.items = [editItem.weaponry1.text(),editItem.weaponry2.text(),editItem.weaponry3.text()]
            self.level = int(editItem.starGroup.checkedButton().property("value"))
            self.final_comp = editItem.necessaryBtn.isChecked()
            self.center = editItem.center.isChecked()
            self.isContent = True
            if not self.heroName:
                self.heroName = "未输入英雄名称"
            self.iconLabel.setText(self.heroName) # 如果有值
        else:
            pass



class CustomHeroItemMessageBox(MessageBoxBase):
    def __init__(self, parent=None,item = None):
        super().__init__(parent)
        self.setMaskColor(QColor(0, 0, 0, 0)) # 白色遮罩
        font = QFont()
        font.setPointSize(12) # 标题字体大小

        bodyVBox = QVBoxLayout() # 垂直布局

        box1 = QHBoxLayout()
        self.heroNameLabel = QLabel("英雄名称:")
        self.heroNameLabel.setFont(font)
        self.heroNameInput = LineEdit()
        self.heroNameInput.setClearButtonEnabled(True)
        self.heroNameInput.setPlaceholderText("请输入英雄名称")

        # 快速补全 英雄名称
        stands1 = list(game_assets.CHAMPIONS.keys()) # 加载英雄名称
        completer1 = QCompleter(stands1, self.heroNameInput)
        completer1.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.heroNameInput.setCompleter(completer1)
        completer1.setFilterMode(Qt.MatchFlag.MatchContains)
        box1.addWidget(self.heroNameLabel)
        box1.addWidget(self.heroNameInput)
        bodyVBox.addLayout(box1)

        box2 = QHBoxLayout()
        self.weaponryNameLabel = QLabel("选择装备:")
        self.weaponryNameLabel.setFont(font)
        self.weaponry1 = LineEdit()
        self.weaponry2 = LineEdit()
        self.weaponry3 = LineEdit()
        self.weaponry1.setPlaceholderText("可留空")
        self.weaponry2.setPlaceholderText("可留空")
        self.weaponry3.setPlaceholderText("可留空")
        self.weaponry1.setClearButtonEnabled(True)
        self.weaponry2.setClearButtonEnabled(True)
        self.weaponry3.setClearButtonEnabled(True)
        box2.addWidget(self.weaponryNameLabel)
        box2.addWidget(self.weaponry1)
        box2.addWidget(self.weaponry2)
        box2.addWidget(self.weaponry3)
        # 快速补全 装备名称
        stands2 = list(game_assets.ITEMS)
        completer2_1 = QCompleter(stands2, self.weaponry1)
        completer2_2 = QCompleter(stands2, self.weaponry2)
        completer2_3 = QCompleter(stands2, self.weaponry3)
        self.weaponry1.setCompleter(completer2_1)
        self.weaponry2.setCompleter(completer2_2)
        self.weaponry3.setCompleter(completer2_3)
        completer2_1.setFilterMode(Qt.MatchFlag.MatchContains)
        completer2_2.setFilterMode(Qt.MatchFlag.MatchContains)
        completer2_3.setFilterMode(Qt.MatchFlag.MatchContains)
        bodyVBox.addLayout(box2)

        box3 = QHBoxLayout()
        self.starNameLabel = QLabel("选择星级:")
        self.starNameLabel.setFont(font)
        box3.addWidget(self.starNameLabel)
        self.starGroup = QButtonGroup(self)
        options = [
            {"display": "1星", "value": "1"},
            {"display": "2星", "value": "2"},
            {"display": "3星", "value": "3"},

        ]
        # 动态添加 RadioButton
        for opt in options:
            btn = RadioButton(opt["display"], self)  # 显示文本
            btn.setProperty("value", opt["value"])  # 存储实际值
            self.starGroup.addButton(btn)  # 加入按钮组
            box3.addWidget(btn)
        self.starGroup.buttons()[1].setChecked(True) # 2星默认选中
        # 当前选中的按钮发生改变
        # starGroup.buttonToggled.connect(lambda button,checked: print(button.property("value"))if checked else None)
        bodyVBox.addLayout(box3)

        box4 = QHBoxLayout()
        self.heroDutyLabel = QLabel("英雄定位:")
        self.heroDutyLabel.setFont(font)
        self.necessaryBtn = SwitchButton()
        self.necessaryBtn.setOffText("过度棋子")
        self.necessaryBtn.setOnText("必须棋子")
        self.center = CheckBox("C位")
        box4.addWidget(self.heroDutyLabel)
        box4.addWidget(self.necessaryBtn)
        box4.addWidget(self.center)
        bodyVBox.addLayout(box4)

        box5 = QHBoxLayout()
        self.indexLabel = QLabel("当前位置：")
        self.indexNum = QLabel(f"第 {4 - (item.index // 7)} 排 , 第 {item.index % 7 + 1} 格")
        self.indexNum.setFont(font)
        self.indexLabel.setFont(font)
        box5.addWidget(self.indexLabel,Qt.AlignmentFlag.AlignCenter)
        box5.addWidget(self.indexNum,Qt.AlignmentFlag.AlignCenter)
        bodyVBox.addLayout(box5)


        # 将组件添加到布局中
        self.viewLayout.addLayout(bodyVBox)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(700)

class MyEditableComboBox(EditableComboBox):
    """重写编辑下拉框功能 取消回车添加新项"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.returnPressed.connect(self._onReturnPressed)
        self.setClearButtonEnabled(True)

    def _onReturnPressed(self):
        pass


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        # 创建子界面
        self.homeInterface = Home(self)

        self.troopInterface = Army(self)

        self.troopRuneInterface = Widget('符文黑白名单', self)

        self.settingInterface = Widget('设置挂机参数', self)

        self.explainInterface = Widget('使用说明', self)

        self.channelInterface = Widget('交流群', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        """初始化侧边导航"""
        self.navigationInterface.setExpandWidth(180)  # 导航栏展开宽度

        self.navigationInterface.setMinimumExpandWidth(1180)
        self.addSubInterface(self.homeInterface, FIF.HOME, '首页', NavigationItemPosition.TOP)

        self.addSubInterface(self.troopInterface, QIcon("./icon/army.png"), '阵容')

        self.addSubInterface(self.troopRuneInterface, QIcon("./icon/强化符文.png"), '强化符文')

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置')

        self.navigationInterface.addSeparator()  # 只是一条分隔线

        self.addSubInterface(self.explainInterface, FIF.BOOK_SHELF, '使用说明', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.channelInterface, FIF.QRCODE, '交流群', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1000, 700)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)
        self.setWindowIcon(QIcon('icon/logo.png'))
        self.setWindowTitle('TFT-OCR-BOT')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
