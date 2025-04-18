"""User interface module that contains user interface class"""

import tkinter as tk
import multiprocessing
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE
import screeninfo

import settings


class UI:
    """用户界面类，用于在游戏过程中在屏幕上绘制标签"""

    def __init__(self, message_queue: multiprocessing.Queue) -> None:
        self.champ_text: str = UI.rgb_convert(settings.UI_COLOR)
        self.transparent: str = UI.rgb_convert((0, 0, 0))
        self.label_container: list = []
        self.message_queue = message_queue
        self.root = tk.Tk()
        self.setup_window_size()
        self.root.overrideredirect(True)
        self.root.config(bg='#000000')
        self.root.attributes("-alpha", 1)
        self.root.wm_attributes("-topmost", 1)
        self.root.attributes('-transparentcolor', '#000000', '-topmost', 1)
        self.root.resizable(False, False)
        self.set_clickthrough(self.root.winfo_id())

    @classmethod
    def rgb_convert(cls, rgb: tuple) -> str:
        """Turns tuple rgb value into string for use by the UI"""
        return "#%02x%02x%02x" % rgb # pylint: disable=consider-using-f-string

    def setup_window_size(self) -> None:
        """Setups window size"""
        primary_monitor: None = next(
            (
                monitor
                for monitor in screeninfo.get_monitors()
                if monitor.is_primary
            ),
            None,
        )
        if primary_monitor is None:
            print("没有找到显示器 请使用 1920x1080 分辨率")
            self.root.geometry("1920x1080")
            return
        self.root.geometry(f'{primary_monitor.width}x{primary_monitor.height}')

    def set_clickthrough(self, hwnd: int) -> None:
        """使用window API函数实现窗口点击"""
        styles: int = GetWindowLong(hwnd, GWL_EXSTYLE)
        styles: int = WS_EX_LAYERED | WS_EX_TRANSPARENT
        SetWindowLong(hwnd, GWL_EXSTYLE, styles)
        SetLayeredWindowAttributes(hwnd, 0, 255, 0x00000001)

    def consume_text(self) -> None:
        """从消息队列中消耗UI更改"""
        if self.message_queue.empty() is False:
            message = self.message_queue.get()
            if 'CLEAR' in message:
                for label in self.label_container:
                    label.destroy()
                self.label_container.clear()
            else:
                for labels in message[1]:
                    label = tk.Label(self.root, text=f"{labels[0]}", bg=self.transparent, fg=self.champ_text,
                                     font=(settings.UI_FONT, 13), bd=0)
                    label.place(x=labels[1][0] - 15, y=labels[1][1] + 30)
                    self.label_container.append(label)

        self.root.after(ms=1, func=self.consume_text)

    def ui_loop(self) -> None:
        """无限运行以处理UI更改的循环"""
        self.consume_text()
        self.root.mainloop()
