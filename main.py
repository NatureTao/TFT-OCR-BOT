"""机器人执行从哪里开始并包含让机器人无限运行的游戏循环"""

import multiprocessing
import os
import time
import traceback
import argparse
import json
from pathlib import Path

import settings
from ui import UI
import auto_queue
from game import Game


def show_inform() -> None:
    print("TFT OCR BOT | https://github.com/NatureTao/TFT-OCR-BOT",flush=True)
    print("Set15：天下无双格斗大赛",flush=True)
    if settings.AUTO_POWER_OFF:
        print("自动关机功能已开启!",flush=True)
    if settings.QUEUE_ID == 1100:
        game_mode = "排位模式"
    elif settings.QUEUE_ID == 1090:
        game_mode = "匹配模式"
    else:
        game_mode = f"警告:当前选择房间ID不是(匹配/排位)云顶模式|当前ID =>{settings.QUEUE_ID}"
    print("当前挂机模式:", game_mode,flush=True)


def game_loop(ui_queue: multiprocessing.Queue, squad_data=None) -> None:
    """通过在循环中调用queue和game start，让程序无限期地运行"""
    counter = 0
    while True:
        if counter == settings.NUMBER_OF_HANGING_UP_GAMES and settings.AUTO_POWER_OFF:
            os.system("shutdown -s -t  60 ")
            exit(0)
        try:
            auto_queue.queue()
            # 传递阵容数据给游戏实例
            game_instance = Game(ui_queue)
            if squad_data:
                # 这里可以根据需要将阵容数据传递给游戏实例
                # 例如: game_instance.set_squad(squad_data)
                print(f"使用阵容配置进行游戏", flush=True)
            counter += 1
        except Exception as e:
            print("本地游戏服务器连接失败,正在重新连接!", flush=True)
            print(e, flush=True)
            print("=== 错误详情 ===", flush=True)
            traceback.print_exc()  # 打印完整错误堆栈（含文件名和行号）
            print("===============", flush=True)
            time.sleep(1)


def load_squad(squad_name):
    """加载指定的阵容配置"""
    try:
        squad_path = Path(__file__).parent / "squads" / f"{squad_name}.json"
        if squad_path.exists():
            with open(squad_path, 'r', encoding='utf-8') as f:
                squad_data = json.load(f)
                print(f"已加载阵容配置: {squad_name}", flush=True)
                # 这里可以根据需要处理阵容数据
                return squad_data
        else:
            print(f"阵容配置文件不存在: {squad_name}", flush=True)
            return None
    except Exception as e:
        print(f"加载阵容配置失败: {e}", flush=True)
        return None

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='TFT OCR BOT')
    parser.add_argument('--squad', type=str, help='指定使用的阵容配置')
    args = parser.parse_args()
    
    # 如果指定了阵容，则加载阵容配置
    squad_data = None
    if args.squad:
        squad_data = load_squad(args.squad)
    
    message_queue = multiprocessing.Queue()
    overlay: UI = UI(message_queue)
    # 将阵容数据传递给 game_loop 函数
    game_thread = multiprocessing.Process(target=game_loop, args=(message_queue, squad_data))
    show_inform()
    game_thread.start()
    overlay.ui_loop()
