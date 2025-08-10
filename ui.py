import multiprocessing
from typing import Tuple

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from screeninfo import get_monitors

import settings


class UI:
    """用户界面类，使用 PySide6 在游戏屏幕上绘制标签（支持 RGBA 透明度）"""

    def __init__(self, message_queue: multiprocessing.Queue) -> None:
        self.champ_color: QColor = self.rgb_convert(settings.UI_COLOR)
        self.transparent: QColor = QColor(0, 0, 0, 0)  # 完全透明
        self.label_container: list[QLabel] = []
        self.message_queue = message_queue

        # 初始化 Qt 应用
        self.app = QApplication.instance() or QApplication([])
        self.root = QWidget()
        self.setup_window()
        self.root.show()

    @staticmethod
    def rgb_convert(rgba: Tuple[int, int, int, int]) -> QColor:
        """ 颜色 """
        r, g, b, a = rgba
        # 确保值在 0-255 范围内（可选）
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        a = max(0, min(255, a))
        return QColor(r, g, b, a)

    def setup_window(self) -> None:
        """设置窗口属性（透明、置顶、无边框）"""
        self.root.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.root.setStyleSheet("background: transparent;")

        # 设置窗口大小为全屏
        primary_monitor = next(
            (mon for mon in get_monitors() if mon.is_primary),
            None
        )
        if not primary_monitor:
            print("未找到主显示器，默认使用 1920x1080")
            self.root.setGeometry(0, 0, 1920, 1080)
        else:
            self.root.setGeometry(
                0, 0,
                primary_monitor.width,
                primary_monitor.height
            )

    def consume_text(self) -> None:
        """从消息队列中更新 UI 标签"""
        if not self.message_queue.empty():
            message = self.message_queue.get()
            if 'CLEAR' in message:
                for label in self.label_container:
                    label.deleteLater()
                self.label_container.clear()
            else:
                for labels in message[1]:
                    label = QLabel(self.root)
                    label.setText(f"{labels[0]}")
                    label.setStyleSheet(
                        f"color: {self.champ_color.name(QColor.NameFormat.HexArgb)};"
                        "background: transparent;"
                    )
                    label.setFont(QFont(settings.UI_FONT, 13))
                    label.move(QPoint(labels[1][0] - 15, labels[1][1] + 30))
                    label.show()
                    self.label_container.append(label)

        # 继续监听队列
        QTimer.singleShot(1, self.consume_text)

    def ui_loop(self) -> None:
        """启动 UI 事件循环"""
        self.consume_text()
        self.app.exec()
