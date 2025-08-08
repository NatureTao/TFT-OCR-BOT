from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import CardWidget, FluentIcon, InfoBar, InfoBarPosition, Icon

from CustomHeroItemMessageBox import CustomHeroItemMessageBox


class HeroItem(CardWidget):
    def __init__(self, parent=None, index=None):
        super().__init__(parent)
        self._originalStyle = self.styleSheet()  # 初始样式

        self.isContent = False # 是否已经被编辑过了
        self.index = index # 英雄位置
        self.heroName = None # 英雄名称
        self.items = [] # 装备
        self.level = 0 # 星级
        self.final_comp = False # 必须
        self.center = False # C位

        self.vBoxLayout = QVBoxLayout(self)  # 垂直容器
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter) # 设置对齐方式

        # 使用 QLabel 显示图标
        self.iconLabel = QLabel()
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 获取 FluentIcon.ADD 的 QPixmap 并设置大小
        icon = Icon(FluentIcon.ADD)
        self.pixmap = icon.pixmap(QSize(16, 16))  #图标设置大小
        self.iconLabel.setPixmap(self.pixmap)

        # 添加到布局
        self.vBoxLayout.addWidget(self.iconLabel)

        # 设置鼠标样式为手型（表示可点击）
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    # 鼠标左键点击事件
    def mousePressEvent(self, event):
        """阵容单元鼠标事件处理"""
        if event.button() == Qt.MouseButton.LeftButton:
            # print(f"阵容编辑框 {self.index} clicked!")
            self.onItemLeftClicked()
        if (event.type() == QEvent.Type.MouseButtonDblClick and
        event.button() == Qt.MouseButton.RightButton):
            self.onItemRightClicked()
        super().mousePressEvent(event) # 确保父类事件仍能正常触发

    def onItemLeftClicked(self):
        """弹出英雄详细编辑对话框"""
        # 确保每次创建新的对话框实例
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
                self.iconLabel.setText("未输入英雄名称")
            else:
                self.iconLabel.setText(self.heroName)
            if self.center:
                newStyle = f"""
                    {self._originalStyle}
                    HeroItem {{
                        background: qlineargradient(
                        x1:0, y1:0,
                        x2:0, y2:1,
                        stop:0 #F38138,
                        stop:1 white
                    );
                    border-radius: 6px;
                    }}
                """
                self.setStyleSheet(newStyle)
            else:
                self.resetStyle()  # 还原样式
        else:
            pass

    def onItemRightClicked(self):
        # 初始化当前单元数据
        if self.heroName is not None or self.iconLabel.text() == "未输入英雄名称":
            self.resetData()
            InfoBar.new(
                icon=FluentIcon.DELETE,
                title='TFT-OCR-BOT',
                content=f"已重置 第{4 - (self.index // 7)} 排 , 第 {self.index % 7 + 1} 格",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self.parent()
            ).setCustomBackgroundColor('#CCCCCC', '#202020')

    def resetData(self):
        """重置单元数据"""
        self.isContent = False
        self.heroName = None
        self.items = []
        self.level = 0
        self.final_comp = False
        self.center = False
        self.iconLabel.setPixmap(self.pixmap)
        self.resetStyle() # 还原样式

    def toDict(self):
        """转换为 JSON 可序列化的字典格式"""
        return {
            "board_position": self.index,
            "items": self.items,
            "level": self.level,
            "final_comp": self.final_comp,
            "center": self.center,
        }

    def resetStyle(self):
        """重置为初始样式"""
        self.setStyleSheet(self._originalStyle)