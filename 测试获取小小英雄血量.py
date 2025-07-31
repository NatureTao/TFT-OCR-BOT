import threading
import time

from PIL import ImageGrab

import ocr
import screen_coords
from vec4 import Vec4


def get_HP() -> list:
    """返回小小英雄排名和生命值的"""
    screen_capture = ImageGrab.grab(bbox=screen_coords.HEALTH_POS.get_coords())
    # screen_capture.save("screenshot.png", "PNG")
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
    print(little_hero)
    if little_hero.isnumeric() and len(little_hero) <= 3:
        HP.append((index + 1, int(little_hero)))


if __name__ == '__main__':
    print(get_HP())




