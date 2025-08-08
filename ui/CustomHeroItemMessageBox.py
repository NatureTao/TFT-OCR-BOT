from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QButtonGroup, QCompleter
from qfluentwidgets import LineEdit, RadioButton, SwitchButton, CheckBox, MessageBoxBase

import game_assets


class CustomHeroItemMessageBox(MessageBoxBase):
    def __init__(self, parent=None,item = None):
        super().__init__(parent)
        self.setMaskColor(QColor(0, 0, 0, 0)) # 白色遮罩
        font = QFont()
        font.setPointSize(12)

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
        self.center = CheckBox()
        self.center.setText("C位")

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