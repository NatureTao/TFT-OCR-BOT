"""首页页面组件"""
import threading
from datetime import datetime

from PySide6.QtCore import QTimer, QThreadPool
from PySide6.QtWidgets import QFrame, QVBoxLayout

from HomeConsole import HomeConsole
# 导入组件
from HomeUserInfo import HomeUserInfo, RefreshTask


class Home(QFrame):
    """首页"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.timer = None
        self.thread = None
        self.lock = threading.Lock()
        self.setObjectName("首页")

        self.vBoxLayout = QVBoxLayout(self)  # 垂直布局

        self.userInfoModule = HomeUserInfo(self)  # 用户信息模块
        self.consoleModule = HomeConsole(self)  # 控制台模块

        self.vBoxLayout.addWidget(self.userInfoModule)
        self.vBoxLayout.addWidget(self.consoleModule)

        self.connectClientClicked()

    def connectClientClicked(self):
        QThreadPool.globalInstance().setMaxThreadCount(1)  # 限制并发数
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_refresh_thread)
        self.timer.start(10000)  # 刷新时间10秒

    def start_refresh_thread(self):
        # 使用新的 RefreshTask 实现
        task = RefreshTask(self.userInfoModule.updateData)
        QThreadPool.globalInstance().start(task)

    def info_log(self, msg: str) -> None:
        """给首页控制台添加信息"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_html = self.consoleModule.textEdit.toHtml()
        new_log = f'<h3 style="color:#7a7374">{current_time}[信息] {msg}</h3>'
        updated_html = current_html + new_log
        self.consoleModule.textEdit.setHtml(updated_html)

    def success_log(self, msg: str) -> None:
        """给首页控制台添加信息"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_html = self.consoleModule.textEdit.toHtml()
        new_log = f'<h3 style="color:#12aa9c">{current_time}[信息] {msg}</h3>'
        updated_html = current_html + new_log
        self.consoleModule.textEdit.setHtml(updated_html)













