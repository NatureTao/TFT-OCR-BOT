import arena_functions
import screen_coords
import time
from typing import Any
import cv2
import numpy as np
from PIL import ImageGrab
from paddleocr import PaddleOCR
import settings
from arena_functions import get_items

if __name__ == '__main__':
    items = arena_functions.get_items()
    print(items)
    # print(f"  装备: {list(filter((None).__ne__, items))}")
