# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：test2.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/16 13:36 
"""
import sys

from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, Qt, QPen, QFont, QPainter
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget, QApplication, QVBoxLayout


import psutil
from datetime import datetime

def get_process_uptime():
    try:
        # 遍历所有进程，查找 LeagueClientUx.exe
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            if proc.info.get('name') == 'LeagueClientUx.exe':
                # 获取进程创建时间
                create_time = proc.info['create_time']
                creation_time = datetime.fromtimestamp(create_time)

                # 计算运行时间
                current_time = datetime.now()
                uptime = current_time - creation_time
                return uptime
        return None
    except Exception as e:
        return None


# 调用示例
if __name__ == "__main__":
    uptime = get_process_uptime()
    if uptime:
        print(f"LeagueClientUx.exe 已运行: {uptime.seconds}秒")