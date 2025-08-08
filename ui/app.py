# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：app.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/13 13:37
    程序入口,新的页面可以在这里添加
首页 设置 阵容 更新 使用说明 交流群

"""
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont

from Army import Army
from Home import Home
from Setting import Setting


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

class Window(FluentWindow):
    """ 主界面 """
    def __init__(self):
        super().__init__()
        # 创建子界面
        self.homeInterface = Home(self)

        self.troopInterface = Army(self)

        self.updateInterface = Widget("更新参数", self)

        self.settingInterface = Setting(self)

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

        self.addSubInterface(self.updateInterface, FIF.UPDATE, '更新')

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置')

        self.navigationInterface.addSeparator()  # 分隔线

        self.addSubInterface(self.explainInterface, FIF.BOOK_SHELF, '使用说明', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.channelInterface, FIF.QRCODE, '交流群', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        """设置 最小宽高 标题 LOGO """
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
