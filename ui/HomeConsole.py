import os
import sys

from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import CardWidget, TextEdit, FluentIcon, PrimaryPushButton


class HomeConsole(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.vBoxLayout = QVBoxLayout(self)  # 垂直布局
        self.hBoxLayout = QHBoxLayout(self)  # 水平布局
        self.status = False  # 脚本启动状态
        # 日志展示
        self.textEdit = TextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.textEdit.textBackgroundColor()

        # 启动按钮
        self.startButton = PrimaryPushButton(FluentIcon.PLAY, '启动程序')
        self.startButton.setStyleSheet(f"""
                        {self.startButton.styleSheet()}
                        PrimaryPushButton {{
                            border-radius: 10px;
                        }}""")

        self.startButton.setFixedSize(180, 35)
        self.startButton.clicked.connect(self.start_button_clicked)

        self.hBoxLayout.addStretch()  # 占据左侧空间
        self.hBoxLayout.addWidget(self.startButton)

        # 构建布局
        self.vBoxLayout.addWidget(self.textEdit)
        self.vBoxLayout.addLayout(self.hBoxLayout)

    def handle_stdout(self):
        # output = self.process.readAllStandardOutput().data().decode()
        while self.process.canReadLine():  # 按行读取
            output = self.process.readLine().data().decode().strip()

            current_html = self.textEdit.toHtml()
            # 构造新的日志内容
            new_log = f'<h3 style="color:#352A29">[信息] {output} </h3>'
            # 检查是否是初始空内容
            if self.textEdit.toPlainText() == '':
                updated_html = new_log
            else:
                updated_html = current_html + new_log
            # 设置更新后的 HTML 内容
            self.textEdit.setHtml(updated_html)
            # 滚动到底部以显示最新内容
            self.scroll_to_bottom()

    def handle_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        # print("[脚本错误]", error)
        current_html = self.textEdit.toHtml()
        # 构造新的日志内容
        new_log = f'<h3 style="color:#F8231D">[错误] {error} </h3>'
        # 检查是否是初始空内容
        if self.textEdit.toPlainText() == '':
            updated_html = new_log
        else:
            updated_html = current_html + new_log
        # 设置更新后的 HTML 内容
        self.textEdit.setHtml(updated_html)
        # 滚动到底部以显示最新内容
        self.scroll_to_bottom()

    def start_button_clicked(self):

        current_html = self.textEdit.toHtml()
        # 构造新的日志内容
        new_log = f''

        if self.status:
            # 结束游戏脚本
            if self.process.state() == QProcess.ProcessState.Running:
                self.process.kill()  # 强制终止
                self.process.waitForFinished(1000)  # 再给1秒清理时间
            new_log = f'<h3 style="color:#EA6334">[信息] 脚本已停止 </h3>'
            print("脚本已停止")

            self.status = False
            self.startButton.setIcon(FluentIcon.PLAY)
            self.startButton.setText("启动程序")
            original_style = self.startButton.styleSheet()
            self.startButton.setStyleSheet(f"""
                {original_style}
                PrimaryPushButton {{
                    background-color: #009FAA;
                    border: 1px solid #009FAA;  /* 同步边框与背景色 */
                }}

                PrimaryPushButton:hover {{
                    background-color: #00A7B3;  
                    border: 1px solid #00A7B3;  /* 悬停状态边框 */
                }}
                PrimaryPushButton:pressed {{
                    background-color: #3EABB3;   /* 按压状态颜色 */
                    border: 1px solid #3EABB3;
                }}
            """)

        else:
            # 运行游戏脚本
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取项目根目录路径
            main_script = os.path.join(project_root, "main.py")
            self.process.start(sys.executable, [main_script])
            new_log = f'<h3 style="color:#EA6334">[信息] 脚本已启动 </h3>'
            print("脚本已启动")

            self.status = True
            self.startButton.setIcon(FluentIcon.POWER_BUTTON)
            self.startButton.setText("结束程序")
            original_style = self.startButton.styleSheet()
            self.startButton.setStyleSheet(f"""
                {original_style}
                PrimaryPushButton {{
                    background-color: #A81113;
                    border: 1px solid #A81113;  /* 同步边框与背景色 */
                }}
                PrimaryPushButton:hover {{
                    background-color: #AD1618;  
                    border: 1px solid #AD1618;  /* 悬停状态边框 */
                }}
                PrimaryPushButton:pressed {{
                    background-color: #B46464;   /* 按压状态颜色 */
                    border: 1px solid #B46464;
                }}
            """)

        # 输出内容到UI控制台
        if self.textEdit.toPlainText() == '':
            updated_html = new_log
        else:
            updated_html = current_html + new_log
        # 设置更新后的 HTML 内容
        self.textEdit.setHtml(updated_html)
        # 滚动到底部以显示最新内容
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """
        滚动到 TextEdit 的底部
        """
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)  # 正确引用 QTextCursor.End
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()