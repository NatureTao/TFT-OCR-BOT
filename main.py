"""
机器人执行从哪里开始并包含让机器人无限运行的游戏循环
"""

import multiprocessing
import os
import time
import traceback

import settings
from ui import UI
import auto_queue
from game import Game


def show_inform() -> None:
    print("TFT OCR BOT | https://github.com/NatureTao/TFT-OCR-BOT",flush=True)
    print("关闭此窗口或点击结束程序按钮,以终止程序!",flush=True)
    print("加载配置文件 setting.py ",flush=True)
    print("S14:赛博之城",flush=True)
    if settings.AUTO_POWER_OFF:
        print("自动关机功能已开启!",flush=True)
    if settings.QUEUE_ID == 1100:
        game_mode = "排位模式"
    elif settings.QUEUE_ID == 1090:
        game_mode = "匹配模式"
    else:
        game_mode = f"警告:当前选择房间ID不是(匹配/排位)云顶模式|当前ID =>{settings.QUEUE_ID}"
    print("当前挂机模式:", game_mode,flush=True)


def game_loop(ui_queue: multiprocessing.Queue) -> None:
    """通过在循环中调用queue和game start，让程序无限期地运行"""
    counter = 0
    while True:
        if counter == settings.NUMBER_OF_HANGING_UP_GAMES and settings.AUTO_POWER_OFF:
            os.system("shutdown -s -t  60 ")
            exit(0)
        try:
            auto_queue.queue()
            Game(ui_queue)
            counter += 1
        except Exception as e:
            print("本地游戏服务器连接失败,正在重新连接!")
            print(e)
            print("=== 错误详情 ===")
            traceback.print_exc()  # 打印完整错误堆栈（含文件名和行号）
            print("===============")
            time.sleep(1)


if __name__ == "__main__":
    message_queue = multiprocessing.Queue()
    overlay: UI = UI(message_queue)
    game_thread = multiprocessing.Process(target=game_loop, args=(message_queue,))
    show_inform()
    game_thread.start()
    overlay.ui_loop()
