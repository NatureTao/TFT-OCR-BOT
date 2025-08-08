from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QTableWidgetItem, QTableWidget, \
    QSizePolicy
from qfluentwidgets import TableWidget, SimpleCardWidget


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