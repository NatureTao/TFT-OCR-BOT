""" 颜色设置卡 """

from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog, QLabel, QPushButton
from qfluentwidgets import SettingCard, PushButton, ConfigItem, qconfig


class ColorSettingCard(SettingCard):
    """ Color 选择 设置卡 """
    def __init__(self, configItem: ConfigItem, icon, title: str,
                 content: str = None, parent=None):
        super().__init__(icon, title, content, parent)
        self.configItem = configItem  # 保存ConfigItem引用

        # 颜色预览按钮
        self.colorButton = PushButton(self)
        self.colorButton.setFixedSize(70, 32)
        self.updateButtonColor()

        # 添加到卡片右侧
        self.hBoxLayout.addWidget(self.colorButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(15)

        # 连接信号
        self.colorButton.clicked.connect(self.showColorDialog)
        self.configItem.valueChanged.connect(self.updateButtonColor)

    def showColorDialog(self):
        """ 显示颜色选择对话框 """
        initial_color = self.get_safe_color()

        dialog = QColorDialog(initial_color, self.window())
        dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)
        dialog.setWindowTitle("选择颜色")

        for label in dialog.findChildren(QLabel):
            if label.text() == "&Custom colors":
                label.setText("自定义颜色")

            elif label.text() == "&Red:":
                label.setText("红(R):")
            elif label.text() == "&Green:":
                label.setText("绿(G)")
            elif label.text() == "Bl&ue:":
                label.setText("蓝(B):")
            elif label.text() == "A&lpha channel:":
                label.setText("透明度(A):")

            elif label.text() == "Hu&e:":
                label.setText("色相(H):")
            elif label.text() == "&Sat:":
                label.setText("饱和度(A):")
            elif label.text() == "&Val:":
                label.setText("明度(V):")
            elif label.text() == "&Basic colors":
                label.setText("基本颜色")


        # 获取并修改按钮文本
        for btn in dialog.findChildren(QPushButton):
            if btn.text() == "OK":
                btn.setText("确定")
            elif btn.text() == "Cancel":
                btn.setText("取消")
            elif btn.text() == "&Pick Screen Color":
                btn.setText("拾取屏幕颜色")
            elif btn.text() == "&Add to Custom Colors":
                btn.setText("添加自定义颜色")

        if dialog.exec():
            color = dialog.currentColor()
            self.setValue([color.red(), color.green(), color.blue(), color.alpha()])

    def updateButtonColor(self):
        """ 更新按钮颜色预览 """
        current_value = self.configItem.value  # 获取当前值
        if len(current_value) == 4:
            r, g, b, a = current_value
            self.colorButton.setStyleSheet(f"""
                background-color: rgba({r}, {g}, {b}, {a});
                border: 1px solid #EBECEC;
                border-radius: 6px;
            """)

    def get_safe_color(self):
        """安全获取QColor对象"""
        value = self.configItem.value
        if not isinstance(value, (list, tuple)) or len(value) < 3:
            return QColor(255, 255, 255)  # 默认白色

        # 确保值在合法范围内
        r = max(0, min(255, int(value[0])))
        g = max(0, min(255, int(value[1])))
        b = max(0, min(255, int(value[2])))
        a = max(0, min(255, int(value[3]))) if len(value) > 3 else 255

        return QColor(r, g, b, a)

    def setValue(self, value):
        """ 设置颜色值 """
        self.configItem.value = value  # 通过ConfigItem设置值
        qconfig.set(self.configItem, value)  #自动触发保存
        qconfig.save()  # 立即保存到文件



class Validator(ABC):
    """ Configuration item validator """

    @abstractmethod
    def validate(self, value):
        """ Verify whether the value is legal """
        pass

    @abstractmethod
    def correct(self, value):
        """ Correct illegal value """
        pass

class ColorValidator(Validator):
    def validate(self, value):
        return (
            isinstance(value, (list, tuple)) and
            len(value) == 4 and
            all(0 <= x <= 255 for x in value)
        )

    def correct(self, value):
        return [max(0, min(255, x)) for x in value][:4]



