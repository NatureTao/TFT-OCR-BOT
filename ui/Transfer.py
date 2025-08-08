""" 穿梭框实现 """

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QListWidgetItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit
)
from PySide6.QtCore import Qt
from qfluentwidgets import LineEdit


class Transfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("穿梭框")
        self.resize(500, 300)
        self._init_ui()
        # self._load_data()

    def _init_ui(self):
        """初始化UI布局和组件"""
        # 左侧面板（待选列表 + 搜索框）
        self.left_search = LineEdit()
        self.left_search.setClearButtonEnabled(True)
        self.left_search.setPlaceholderText("搜索待选")
        self.left_search.setFixedHeight(45)
        self.left_search.textChanged.connect(self._filter_left)

        self.left_list = QListWidget()
        self.left_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  # 允许多选

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("待选"))
        left_layout.addWidget(self.left_search)
        left_layout.addWidget(self.left_list)

        # 右侧面板（已选列表 + 搜索框）
        self.right_search = LineEdit()
        self.right_search.setFixedHeight(45)
        self.right_search.setPlaceholderText("搜索已选")
        self.right_search.textChanged.connect(self._filter_right)

        self.right_list = QListWidget()
        self.right_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("已选"))
        right_layout.addWidget(self.right_search)
        right_layout.addWidget(self.right_list)


        font = QFont()
        font.setPointSize(10) # 标题字体大小

        # 操作按钮
        self.btn_to_right = QPushButton(">")
        self.btn_to_right.setFont(font)
        self.btn_to_right.clicked.connect(self._move_to_right)

        self.btn_to_left = QPushButton("<")
        self.btn_to_left.setFont(font)
        self.btn_to_left.clicked.connect(self._move_to_left)

        self.btn_all_to_right = QPushButton(">>")
        self.btn_all_to_right.setFont(font)
        self.btn_all_to_right.clicked.connect(self._move_all_to_right)

        self.btn_all_to_left = QPushButton("<<")
        self.btn_all_to_left.setFont(font)
        self.btn_all_to_left.clicked.connect(self._move_all_to_left)

        # 按钮垂直布局
        btn_layout = QVBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_all_to_right)
        btn_layout.addWidget(self.btn_to_right)
        btn_layout.addWidget(self.btn_to_left)
        btn_layout.addWidget(self.btn_all_to_left)
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 10)

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.addLayout(left_layout, 40)  # 左侧占40%宽度
        main_layout.addLayout(btn_layout, 20)  # 按钮占20%宽度
        main_layout.addLayout(right_layout, 40)  # 右侧占40%宽度

        # 美化样式
        self._set_style()

    def _set_style(self):
        """设置组件样式"""
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit {
                padding: 5px;
                margin-bottom: 10px;
                border: 1px solid #aaa;
                border-radius: 4px;
            }
            QPushButton {
                min-width: 50px;
                padding: 8px;
                margin: 5px;
                background: #f0f0f0;
                border: 1px solid #aaa;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
        """)

    def load_data(self, items=None):
        """加载测试数据"""
        if items is None:
            items = []
        for item in items:
            self.left_list.addItem(QListWidgetItem(item))

    def _filter_left(self):
        """过滤左侧列表"""
        self._filter_list(self.left_list, self.left_search.text())

    def _filter_right(self):
        """过滤右侧列表"""
        self._filter_list(self.right_list, self.right_search.text())

    def _filter_list(self, list_widget: QListWidget, keyword: str):
        """通用列表过滤方法"""
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            # 如果搜索关键词为空，或当前项包含关键词（不区分大小写）
            match = keyword.lower() in item.text().lower()
            item.setHidden(not match) if keyword else item.setHidden(False)

    def _move_to_right(self):
        """将选中项移动到右侧"""
        self._transfer_items(self.left_list, self.right_list)

    def _move_to_left(self):
        """将选中项移动回左侧"""
        self._transfer_items(self.right_list, self.left_list)

    def _transfer_items(self, from_list: QListWidget, to_list: QListWidget):
        """通用转移方法"""
        selected_items = from_list.selectedItems()
        for item in selected_items:
            row = from_list.row(item)
            from_list.takeItem(row)
            to_list.addItem(item)
            item.setHidden(False)  # 确保转移后可见

    def _move_all_to_right(self):
        """全部移动到右侧"""
        self._transfer_all(self.left_list, self.right_list)

    def _move_all_to_left(self):
        """全部移动回左侧"""
        self._transfer_all(self.right_list, self.left_list)

    def _transfer_all(self, from_list: QListWidget, to_list: QListWidget):
        """全部转移方法"""
        while from_list.count() > 0:
            item = from_list.takeItem(0)
            to_list.addItem(item)
            item.setHidden(False)

    def get_selected_data(self) -> list:
        """获取右侧列表（已选列表）的所有数据，返回数组格式"""
        selected_data = []
        for i in range(self.right_list.count()):
            item = self.right_list.item(i)
            selected_data.append(item.text())
        return selected_data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Transfer()
    window.show()
    sys.exit(app.exec())