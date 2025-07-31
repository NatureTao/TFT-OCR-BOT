import threading
import time

from PIL import ImageGrab

import comps
import game_assets
import screen_coords
import ocr
from arena_functions import valid_item
from vec4 import Vec4


def get_anvil_items() -> list:
    """返回铁砧上的物品"""
    screen_capture = ImageGrab.grab(bbox=screen_coords.ANVIL_ITEMS_POS.get_coords())
    items: list = []
    thread_list: list = []
    for index, pos in enumerate(screen_coords.ORDINARY_ANVIL_ITEM_POS):
        thread = threading.Thread(
            target=get_anvil_item, args=(screen_capture, pos, index, items)
        )
        thread_list.append(thread)
    for index, pos in enumerate(screen_coords.DIVINE_ANVIL_ITEM_POS):
        thread = threading.Thread(
            target=get_anvil_item, args=(screen_capture, pos, index, items)
        )
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()
        time.sleep(0.05)
    for thread in thread_list:
        thread.join()
    return sorted(items)


def get_anvil_item(screen_capture: ImageGrab.Image, pos: Vec4, index: int, items: list):
    """遍历识别每个铁砧物品"""
    item: str = screen_capture.crop(pos.get_coords())
    item: str = ocr.get_text_from_image(image=item)
    item = valid_item(item)
    if item is not None:
        items.append((index, item))


if __name__ == '__main__':
    print(get_anvil_items())

    # while True:
    #     time.sleep(1)
    #     items: list = []
    #     for coords in screen_coords.DIVINE_ANVIL_ITEM_POS:
    #         item: str = ocr.get_text(screenxy=coords.get_coords(), scale=3)
    #         items.append(item)
    #     if len(list(filter(None, items))) == 5 and '' not in items:
    #         print(" [高级]铁砧")
    #         print(items)
    #         break
    #
    #     items.__init__()  # 刷新
    #
    #     for coords in screen_coords.ORDINARY_ANVIL_ITEM_POS:
    #         item: str = ocr.get_text(screenxy=coords.get_coords(), scale=3)
    #         items.append(item)
    #     if len(list(filter(None, items))) == 4 and '' not in items:
    #         print(" [普通]铁砧")
    #         print(items)
    #         break

    # for champ_name in comps.COMP:
    #     print(comps.COMP[champ_name]["items"])
    #     print(comps.COMP[champ_name]["items"].__len__())
    #     for item in comps.COMP[champ_name]["items"]:
    #         print(item)
    #
    #
    # for t in game_assets.FULL_ITEMS:
    #     print(t)

    # print(game_assets.FULL_ITEMS["死亡之刃"])
    # for t in game_assets.FULL_ITEMS["死亡之刃"]:
    #     print(t)
