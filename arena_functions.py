"""
Arena类用于获取游戏数据的函数
"""
import time
import os
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

def save_debug_screenshot(name: str, coords: Vec4) -> None:
    """保存带红框标记的调试截图"""
    # 截取更大范围的图片,包含周围区域
    larger_bbox = (
        coords.get_coords()[0] - 50,
        coords.get_coords()[1] - 50, 
        coords.get_coords()[2] + 50,
        coords.get_coords()[3] + 50
    )
    screen_capture = ImageGrab.grab(bbox=larger_bbox)
    
    # 在大图上绘制红框标记识别区域
    from PIL import ImageDraw
    draw = ImageDraw.Draw(screen_capture)
    draw.rectangle(
        (
            50, 50,
            coords.get_coords()[2] - coords.get_coords()[0] + 50,
            coords.get_coords()[3] - coords.get_coords()[1] + 50
        ),
        outline="red",
        width=2
    )
    
    text = ocr.get_text(screenxy=coords.get_coords(), scale=3)
    print(f"{name}识别失败,识别内容为: {text}")
    print(f"截图位置: {coords.get_coords()}")
    
    # 保存带红框标记的截图到debug目录
    os.makedirs("debug", exist_ok=True)
    screen_capture.save(f"debug/{name}_{int(time.time())}.png")


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


# def get_health() -> int:
#     """返回召唤师生命值"""
#     try:
#         response = requests.get(
#             "https://127.0.0.1:2999/liveclientdata/allgamedata",
#             timeout=10,
#             verify=False,
#         )
#         return int(response.json()["activePlayer"]["championStats"]["currentHealth"])
#     except (requests.exceptions.ConnectionError, KeyError):
#         return -1

def get_alive() -> int:
    """返回召唤师是否存活"""
    try:
        response = requests.get(
            "https://127.0.0.1:2999/liveclientdata/allgamedata",
            timeout=20,
            verify=False,
        )
        myName = response.json()["activePlayer"]["riotId"]
        datas = response.json()["allPlayers"]
        for data in datas:
            if data["riotId"] == myName:
                return int(data["scores"]["deaths"])
    except (requests.exceptions.ConnectionError, KeyError):
        return 1


def get_HP() -> list:
    """返回小小英雄排名和生命值的"""
    screen_capture = ImageGrab.grab(bbox=screen_coords.HEALTH_POS.get_coords())
    HP: list = []
    thread_list: list = []
    for index, pos in enumerate(screen_coords.HEALTH_ITEM_POS):
        thread = threading.Thread(
            target=get_little_hero_health, args=(screen_capture, pos, index, HP)
        )
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
        time.sleep(0.05)
    for thread in thread_list:
        thread.join()
    return HP


def get_little_hero_health(screen_capture: ImageGrab.Image, pos: Vec4, index: int, HP: list):
    """遍历搜索右边小小英雄血量位置"""
    little_hero: str = screen_capture.crop(pos.get_coords())
    little_hero: str = ocr.get_text_from_image(image=little_hero)
    try:
        if little_hero.isnumeric() and 3 >= len(little_hero) == len(str(int(little_hero))) and int(little_hero) <= 100:
            HP.append((index + 1, int(little_hero)))
    except ValueError:
        save_debug_screenshot("little_hero_health", pos)
        pass


def get_round_remaining_time() -> int:
    """返回回合剩于时间"""
    try:
        # 获取当前回合
        round_text = ocr.get_text(screenxy=screen_coords.ROUND_POS.get_coords(), scale=3)
        # 如果是2-x及以后的回合,识别区域向右移动50像素
        if round_text.startswith("2-") or round_text.startswith("3-") or round_text.startswith("4-") or round_text.startswith("5-") or round_text.startswith("6-") or round_text.startswith("7-"):
            coords = list(screen_coords.REMAINING_TIME_POS.get_coords())
            coords[0] += 50
            coords[2] += 50
            second = int(ocr.get_text(screenxy=tuple(coords), scale=3))
        else:
            second = int(ocr.get_text(screenxy=screen_coords.REMAINING_TIME_POS.get_coords(), scale=3))
        return second
    except ValueError:
        save_debug_screenshot("round_time", screen_coords.REMAINING_TIME_POS)
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
        save_debug_screenshot("gold", screen_coords.GOLD_POS)
        return 0


def get_abnormal_gold() -> int:
    """S13 4-6钱包位置"""
    gold: str = ocr.get_text(
        screenxy=screen_coords.GOLD_ABNORMAL_POS.get_coords(),
        scale=3
    )
    try:
        return int(gold)
    except ValueError:
        save_debug_screenshot("abnormal_gold", screen_coords.GOLD_ABNORMAL_POS)
        return 0


def get_abnormal() -> str:
    """获取S13异常突变buff名称"""
    abnormal: str = ocr.get_text(
        screenxy=screen_coords.ABNORMAL_POS.get_coords(),
        scale=3
    )
    try:
        return str(abnormal)
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
        valid = valid_item(item)
        item_bench.append(valid)
        if valid is None:
            break
    mk_functions.move_mouse(screen_coords.DEFAULT_LOC.get_coords())
    return item_bench
