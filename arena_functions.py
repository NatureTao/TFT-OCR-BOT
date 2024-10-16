"""
Arena类用于获取游戏数据的函数
"""
import time
from difflib import SequenceMatcher
import threading
from PIL import ImageGrab
import numpy as np
import requests
import screen_coords
import ocr
import game_assets
import mk_functions
from vec4 import Vec4


def get_level() -> int:
    """返回召唤师的等级"""
    try:
        response = requests.get(
            "https://127.0.0.1:2999/liveclientdata/allgamedata",
            timeout=10,
            verify=False,
        )
        return int(response.json()["activePlayer"]["level"])
    except (requests.exceptions.ConnectionError, KeyError):
        return 1


def get_health() -> int:
    """返回召唤师生命值"""
    try:
        response = requests.get(
            "https://127.0.0.1:2999/liveclientdata/allgamedata",
            timeout=10,
            verify=False,
        )
        return int(response.json()["activePlayer"]["championStats"]["currentHealth"])
    except (requests.exceptions.ConnectionError, KeyError):
        return -1


def get_gold() -> int:
    """Returns the gold for the tactician"""
    gold: str = ocr.get_text(
        screenxy=screen_coords.GOLD_POS.get_coords(),
        scale=3
    )
    try:
        return int(gold)
    except ValueError:
        return 0

def get_wand() -> str:
    """获取新赛季魔杖buff"""
    wand_name: str = ocr.get_text(
        screenxy=screen_coords.WAND_POS.get_coords(),
        scale=3
    )
    try:
        return str(wand_name)
    except Exception:
        return ""



def valid_champ(champ: str) -> str:
    """将英雄字符串匹配为有效的英雄名称字符串并返回"""
    if champ in game_assets.CHAMPIONS:
        return champ

    return next(
        (
            champion
            for champion in game_assets.CHAMPIONS
            if SequenceMatcher(a=champion, b=champ).ratio() >= 0.7
        ),
        "",
    )


def get_champ(
    screen_capture: ImageGrab.Image, name_pos: Vec4, shop_pos: int, shop_array: list
) -> str:
    """返回包含商店位置和冠军名称的元组"""
    champ: str = screen_capture.crop(name_pos.get_coords())
    champ: str = ocr.get_text_from_image(image=champ)
    shop_array.append((shop_pos, valid_champ(champ)))

def get_shop() -> list:
    """ 返回商店中的英雄列表 """
    screen_capture = ImageGrab.grab(bbox=screen_coords.SHOP_POS.get_coords())
    shop: list = []
    thread_list: list = []
    for shop_index, name_pos in enumerate(screen_coords.CHAMP_NAME_POS):

        thread = threading.Thread(

            target=get_champ, args=(screen_capture, name_pos, shop_index, shop)
        )
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
        time.sleep(0.05)
    for thread in thread_list:
        thread.join()
    return sorted(shop)


def empty_slot() -> int:
    """找到备战区第一个位置"""
    for slot, positions in enumerate(screen_coords.BENCH_HEALTH_POS):
        screen_capture = ImageGrab.grab(bbox=positions.get_coords())
        screenshot_array = np.array(screen_capture)
        is_health_color = np.all(screenshot_array == [0, 255, 18], axis=-1)
        if not any(np.convolve(is_health_color.reshape(-1), np.ones(5), mode='valid')):
            return slot  # Slot 0-8
    return -1  # No empty slot


def bench_occupied_check() -> list:
    """返回一个布尔值列表，该列表映射到每个工作台槽，指示其是否被占用"""
    bench_occupied: list = []
    for positions in screen_coords.BENCH_HEALTH_POS:
        screen_capture = ImageGrab.grab(bbox=positions.get_coords())
        screenshot_array = np.array(screen_capture)
        is_health_color = np.all(screenshot_array == [0, 255, 18], axis=-1)
        occupied = any(np.convolve(is_health_color.reshape(-1), np.ones(5), mode='valid'))
        bench_occupied.append(occupied)
    return bench_occupied


def valid_item(item: str) -> str | None:
    """检查参数1中传递的项是否有效"""
    return next(
        (
            valid_item_name
            for valid_item_name in game_assets.ITEMS
            if valid_item_name in item
            or SequenceMatcher(a=valid_item_name, b=item).ratio() >= 0.85
        ),
        None,
    )


def get_items() -> list:
    """返回当前棋盘上装备的列表"""
    item_bench: list = []
    for positions in screen_coords.ITEM_POS:
        mk_functions.move_mouse(positions[0].get_coords())
        item: str = ocr.get_text(
            screenxy=positions[1].get_coords(),
            scale=3
        )
        item_bench.append(valid_item(item))
    mk_functions.move_mouse(screen_coords.DEFAULT_LOC.get_coords())
    return item_bench
