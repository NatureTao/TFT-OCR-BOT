import threading
import time

from PIL import ImageGrab

import arena_functions
import screen_coords
import ocr
from vec4 import Vec4

if __name__ == '__main__':

    while True:
        shop: list = arena_functions.get_shop()
        print(shop)
        time.sleep(1)



