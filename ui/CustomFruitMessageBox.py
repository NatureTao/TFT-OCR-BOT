from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import MessageBoxBase

from Transfer import Transfer

import game_assets


class CustomFruitMessageBox(MessageBoxBase):
    """强化果实弹窗"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaskColor(QColor(0, 0, 0, 0))  # 白色遮罩
        self.box1 = QHBoxLayout()
        font = QFont()
        font.setPointSize(16)
        box2 = QVBoxLayout()
        self.leftLabel = QLabel("强化果实白名单")
        self.leftLabel.setFont(font)
        self.leftLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fruitTransfer = Transfer()
        self.fruitTransfer.load_data(game_assets.FRUIT) # 加载数据

        self.avoidFruitTransfer = Transfer()
        self.avoidFruitTransfer.load_data(game_assets.FRUIT) # 加载数据

        box2.addWidget(self.leftLabel)
        box2.addWidget(self.fruitTransfer)
        self.box1.addLayout(box2)

        box3 = QVBoxLayout()
        self.rightLabel = QLabel("强化果实黑名单")
        self.rightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rightLabel.setFont(font)
        box3.addWidget(self.rightLabel)
        box3.addWidget(self.avoidFruitTransfer)
        self.box1.addLayout(box3)

        # 将组件添加到布局中
        self.viewLayout.addLayout(self.box1)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(800)
        self.widget.setMinimumHeight(500)