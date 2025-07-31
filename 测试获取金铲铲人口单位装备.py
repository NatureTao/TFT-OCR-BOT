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

"""初始化全局飞浆OCR"""
ocr = PaddleOCR(lang="ch",  # 默认中文
                            show_log=False,
                            use_gpu=settings.USE_GPU,
                            use_space_char=False,
                            use_angle_cls=True,
                            use_mp=settings.USE_MP,
                            det_db_score_mode=settings.DET_DB_SCORE_MODE)  # 推理模型路径

def image_grayscale(image: ImageGrab.Image) -> Any:
    """将图像转换为灰度，使OCR更容易破译字符"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def image_thresholding(image: ImageGrab.Image) -> Any:
    """将阈值化应用于图像 https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html"""
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

def image_array(image: ImageGrab.Image) -> Any:
    """将图像转换为数组"""
    image = np.array(image)
    image = image[..., :3]
    return image

def image_resize(image: int, scale: int) -> Any:
    """使用参数2中的比例来调整图像的大小"""
    (width, height) = (image.width * scale, image.height * scale)
    return image.resize((width, height))


def get_text(screenxy: tuple, scale: int) -> str:
    """从屏幕坐标返回文本"""
    result = ""
    screenshot = ImageGrab.grab(bbox=screenxy)
    resize = image_resize(screenshot, scale)  # 调整图像大小
    array = image_array(resize)  # 将图像转换成数组

    resize.save("get_text.png")  # 测试当前图片

    grayscale = image_grayscale(array)  # 图像转换为灰度，使OCR更容易破译字符
    thresholding = image_thresholding(grayscale)  # 将阈值化应用于图像
    if thresholding is not None:
        try:
            result = ocr.ocr(thresholding, cls=True)
        except Exception as e:
            ocr_ex = PaddleOCR(lang="ch",  # 默认中文
                            show_log=False,
                            use_gpu=settings.USE_GPU,
                            use_space_char=False,
                            use_angle_cls=True,
                            use_mp=settings.USE_MP,
                            det_db_score_mode=settings.DET_DB_SCORE_MODE)
            result = ocr_ex.ocr(thresholding, cls=True)


    if result[0] is not None:
        text = result[0][0][1][0].strip()
        if text is not None:
            return text
    return ""

def get_text_from_image(image: ImageGrab.Image) -> str:
    """从图像中获取文本"""
    result = ""
    resize = image_resize(image, 3)  # 调整图像大小
    image.save("get_text_from_image.png") # 测试当前图片
    array = image_array(resize)  # 将图像转换成数组
    grayscale = image_grayscale(array)  # 图像转换为灰度，使OCR更容易破译字符
    thresholding = image_thresholding(grayscale)  # 将阈值化应用于图像
    if thresholding is not None:
        try:
            result = ocr.ocr(thresholding, cls=True)
        except Exception as e:
            ocr_ex = PaddleOCR(lang="ch",  # 默认中文
                               show_log=False,
                               use_gpu=settings.USE_GPU,
                               use_space_char=False,
                               use_angle_cls=True,
                               use_mp=settings.USE_MP,
                               det_db_score_mode=settings.DET_DB_SCORE_MODE)
            result = ocr_ex.ocr(thresholding, cls=True)

    if result[0] is not None:
        text = result[0][0][1][0].strip()
        if text is not None:
            return text
    return ""

if __name__ == '__main__':

    item: str = ocr.get_text(
        screenxy=screen_coords.ITEM_POS[0][1].get_coords(),
        scale=3
    )
    print(item)

