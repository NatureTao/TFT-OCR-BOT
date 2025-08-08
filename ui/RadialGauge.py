from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QFontMetrics
from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import setFont, ProgressBar, isDarkTheme



class RadialGauge(ProgressBar):
    """ 重绘进度环，并预留中心容器位置 """

    def __init__(self, parent=None, useAni=True):
        super().__init__(parent, useAni=useAni)
        self.lightBackgroundColor = QColor(0, 0, 0, 34)
        self.darkBackgroundColor = QColor(255, 255, 255, 34)
        self._strokeWidth = 7
        self.setTextVisible(False)  # 禁用文本显示
        self.setFixedSize(200, 200)
        self.containerSize = 200  # 容器大小（宽高）
        self.bottomText = ""
        setFont(self)

        # 创建中心容器控件
        self.centerWidget = QWidget(self)  # 使用 QWidget 作为容器
        # 使用垂直布局管理器
        self.center = QVBoxLayout(self)
        self.center.addWidget(self.centerWidget, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.center.setContentsMargins(15, 0, 0, 15)  # 调整中心

        self.updateCenterWidgetPosition()

    def getCenterContainerRect(self):
        """ 获取中心容器的矩形区域 """
        centerX = self.width() / 2 - self.containerSize / 2
        centerY = self.height() / 2 - self.containerSize / 2
        return QRectF(centerX, centerY, self.containerSize, self.containerSize)

    def updateCenterWidgetPosition(self):
        """ 更新中心容器控件的位置 """
        centerRect = self.getCenterContainerRect()
        self.centerWidget.setGeometry(centerRect.toRect())

    def resizeEvent(self, e):
        """ 在窗口大小改变时更新中心容器位置 """
        super().resizeEvent(e)
        self.updateCenterWidgetPosition()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        cw = self._strokeWidth  # 圆环厚度
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw / 2, self.height() / 2 - w / 2, w, w)

        # 绘制背景环
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 240 * 16, -300 * 16)  # 背景环

        if self.maximum() <= self.minimum():
            return

        # 绘制进度条
        pen.setColor(self.barColor())
        painter.setPen(pen)
        degree = int(self.val / (self.maximum() - self.minimum()) * 300)
        painter.drawArc(rc, 240 * 16, -degree * 16)  # 进度条

        font = QFont("微软雅黑", 9)
        font.setBold(True)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.2)
        fm = QFontMetrics(font)
        textRect = fm.boundingRect(self.bottomText)
        textPos = QPointF(
            rc.center().x() - textRect.width() / 2,  # 水平方向居中
            (rc.center().y() + textRect.height() / 2) + self.height() / 2.5  # 垂直方向在中心正下方
        )
        painter.setFont(font)
        painter.drawText(textPos, self.bottomText)