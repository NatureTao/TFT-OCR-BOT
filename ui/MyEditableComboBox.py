from qfluentwidgets import EditableComboBox

class MyEditableComboBox(EditableComboBox):
    """重写编辑下拉框功能 取消回车添加新项"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.returnPressed.connect(self._onReturnPressed)
        self.setClearButtonEnabled(True)

    def _onReturnPressed(self):
        pass
