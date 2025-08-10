from PySide6.QtCore import Qt, Signal, QThread, QRunnable, QObject
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import CardWidget, AvatarWidget, ProgressBar

from HomeStateInfo import HomeStateInfo
from RadialGauge import RadialGauge
# 导入组件
from service import LOLService

lol = LOLService()  # 客户端服务

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
        # self.startInfo = HomeStateInfo()
        # self.startInfo.setMaximumWidth(165)
        # self.startInfo.setMinimumWidth(165)
        # self.hBoxLayout.addWidget(self.startInfo, Qt.AlignmentFlag.AlignRight)

    def updateData(self, lol_service=None):
        print("刷新数据")
        # 使用传入的 lol_service 对象或全局 lol 对象
        data = lol_service if lol_service else lol
        
        # 批量收集所有需要更新的 UI 元素，减少重绘次数
        updates_needed = False
        
        # 准备头像更新
        if data.avatar is None:
            image = QImage("icon/default.jpg")  # 默认头像
        else:
            image = QImage()
            image.loadFromData(data.avatar)
        scaled_image = image.scaled(90, 90)  # 缩放图片
        
        # 开始批量更新 UI
        self.setUpdatesEnabled(False)  # 暂时禁用更新以减少闪烁
        
        try:
            # 更新头像
            self.avatar.setPixmap(QPixmap.fromImage(scaled_image))
            
            # 更新进度环相关数据
            if self.rg.maximum() != int(data.xpUntilNextLevel):
                self.rg.setMaximum(int(data.xpUntilNextLevel))
                updates_needed = True
                
            if self.rg.getVal() != int(data.xpSinceLastLevel):
                self.rg.setValue(int(data.xpSinceLastLevel))
                updates_needed = True
                
            if self.rg.bottomText != str(data.summonerLevel):
                self.rg.bottomText = str(data.summonerLevel)
                updates_needed = True
            
            # 更新通行证信息
            if self.passName.text() != data.pass_name:
                self.passName.setText(data.pass_name)
                updates_needed = True
                
            if self.passNum.text() != str(data.currentLevel):
                self.passNum.setText(str(data.currentLevel))
                updates_needed = True
            
            # 更新通行证经验条
            if self.passLevel.maximum() != int(data.totalLevelXP):
                self.passLevel.setMaximum(int(data.totalLevelXP))
                updates_needed = True
                
            if self.passLevel.getVal() != int(data.currentLevelXP):
                self.passLevel.setValue(int(data.currentLevelXP))
                updates_needed = True
            
            # 更新货币信息
            if self.currencyBlueNumLabel.text() != str(data.lol_blue_essence):
                self.currencyBlueNumLabel.setText(str(data.lol_blue_essence))
                updates_needed = True
                
            if self.currencyOrangeNumLabel.text() != str(data.lol_orange_essence):
                self.currencyOrangeNumLabel.setText(str(data.lol_orange_essence))
                updates_needed = True
                
        finally:
            self.setUpdatesEnabled(True)  # 重新启用更新
            
            # 如果有更新，强制重绘一次
            if updates_needed:
                self.update()

# 创建信号类
class RefreshSignals(QObject):
    """用于在线程间传递信号的类"""
    finished = Signal(object)  # 传递 lol 对象

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
        self.signals = RefreshSignals()
        self.signals.finished.connect(callback)

    def run(self):
        lol.refresh_client()
        # 发送信号而不是直接调用回调
        self.signals.finished.emit(lol)