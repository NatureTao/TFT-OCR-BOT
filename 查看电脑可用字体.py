# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：查看电脑可用字体.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/12 19:34 
"""

import tkinter as tk
from tkinter import font


def list_available_fonts():
    """
    列出当前系统中所有可用的字体。
    """
    # 创建一个临时的Tk根窗口，因为我们只需要访问字体信息
    root = tk.Tk()
    # 获取系统支持的所有字体家族名称
    available_fonts = font.families()

    # 对字体名称进行排序以方便阅读
    available_fonts_sorted = sorted(available_fonts)

    print("Available fonts on your system:")
    for f in available_fonts_sorted:
        print(f)

    # 销毁临时创建的Tk根窗口
    root.destroy()


if __name__ == "__main__":
    list_available_fonts()