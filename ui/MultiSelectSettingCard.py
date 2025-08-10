from ColorSettingCard import Validator

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QWidget, QFrame, QGridLayout
from qfluentwidgets import (ExpandSettingCard, BodyLabel, CheckBox,
                            ConfigItem, qconfig, ScrollArea)

from ColorSettingCard import Validator


class MultiSelectSettingCard(ExpandSettingCard):
    """支持多选等级的下拉设置卡（完全修复版）"""
    valueChanged = Signal(list)

    def __init__(self, configItem: ConfigItem, icon, title, content,
                 min_level=1, max_level=10, parent=None):
        super().__init__(icon, title, content, parent)

        # 初始化配置
        self.configItem = configItem
        self.min_level = min_level
        self.max_level = max_level

        # 顶部显示标签
        self.summaryLabel = BodyLabel(self)
        self.summaryLabel.setObjectName("summaryLabel")
        self.addWidget(self.summaryLabel)

        # 设置下拉区域（根据源码调整边距）
        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)  # 重要：必须与源码一致

        # 创建可滚动复选框区域
        self._create_checkboxes()
        self._update_summary()

        # 连接配置项变化信号
        self.configItem.valueChanged.connect(self.setValue)

        # 关键修复：确保布局计算正确
        self._adjustViewSize()

    def _create_checkboxes(self):
        """创建等级复选框(平铺布局)"""
        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # 关键修改：设置背景色（使用 QSS）
        container.setStyleSheet("background-color: #F9F9F9; border-radius: 5px;")

        # 使用网格布局实现平铺效果
        self.gridLayout = QGridLayout(container)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setContentsMargins(0, 5, 10, 5)

        # 关键修改1：设置布局的对齐方式为水平居中
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # 创建复选框
        self.checkboxes = {}
        columns = 10
        for i, level in enumerate(range(self.min_level, self.max_level + 1)):
            row, col = divmod(i, columns)
            cb = CheckBox(f"等级 {level}")
            cb.setChecked(level in self.configItem.value)
            cb.clicked.connect(self._on_checkbox_changed)
            self.checkboxes[level] = cb
            self.gridLayout.addWidget(cb, row, col)

            # 关键修改2：设置每个复选框的对齐方式
            self.gridLayout.setAlignment(cb, Qt.AlignmentFlag.AlignHCenter)

        scroll.setWidget(container)
        self.viewLayout.addWidget(scroll)

        # 关键修复：添加空白撑开空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewLayout.addWidget(spacer)

    def _on_checkbox_changed(self):
        """复选框状态变化处理"""
        selected = [lvl for lvl, cb in self.checkboxes.items() if cb.isChecked()]
        self.configItem.value = selected
        qconfig.set(self.configItem, selected)
        self._update_summary()
        self.valueChanged.emit(selected)

    def _update_summary(self):
        """更新顶部摘要文本"""
        selected = self.configItem.value
        count = len(selected)

        if count == 0:
            text = "未选择等级"
        elif count == 1:
            text = f"已选: 等级 {selected[0]}"
        elif count < 2:
            text = f"已选: {', '.join(f'等级 {x}' for x in sorted(selected))}"
        else:
            text = f"已选: {count}个等级 (点击查看)"

        self.summaryLabel.setText(text)
        self.summaryLabel.adjustSize()

    def setValue(self, values):
        """外部设置值"""

        if not isinstance(values, list):
            values = []

        # 更新复选框状态
        for level, cb in self.checkboxes.items():
            cb.setChecked(level in values)

        # 更新配置
        self.configItem.value = values
        qconfig.set(self.configItem, values)
        qconfig.save()
        self._update_summary()

    def _adjustViewSize(self):
        """重写高度计算方法"""
        if hasattr(super(), '_adjustViewSize'):
            super()._adjustViewSize()

        # 确保内容高度正确计算
        if self.isExpand:
            self.setFixedHeight(self.card.height() + self.viewLayout.sizeHint().height())

class ListValidator(Validator):
    """验证列表类型配置项的验证器"""

    def __init__(self, value_type=int):
        """
        Args:
            value_type: 列表元素的类型（int/float/str等）
        """
        self.value_type = value_type

    def validate(self, value):
        """验证是否为有效列表"""
        if not isinstance(value, list):
            return False
        try:
            return all(isinstance(x, self.value_type) for x in value)
        except (TypeError, ValueError):
            return False

    def correct(self, value):
        """修正为合法列表"""
        if isinstance(value, list):
            corrected = []
            for x in value:
                try:
                    corrected.append(self.value_type(x))
                except (ValueError, TypeError):
                    continue
            return corrected
        elif isinstance(value, (int, float, str)):
            try:
                return [self.value_type(value)]
            except (ValueError, TypeError):
                return []
        return []