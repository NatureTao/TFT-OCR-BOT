import ocr
import screen_coords
import time
from typing import Any
import cv2
import numpy as np
from PIL import ImageGrab
from paddleocr import PaddleOCR
import settings


if __name__ == '__main__':
    while True:
        time.sleep(1)
        augments: list = []
        print("开始")
        for coords in screen_coords.AUGMENT_POS:
            augment: str = ocr.get_text(
                screenxy=coords.get_coords(), scale=1
            )
            augments.append(augment)
        print(f"  强化符文: {augments}")
        if len(augments) == 3 and "" not in augments:
            break