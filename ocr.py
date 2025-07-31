"""
包含所有与截图转换为字符串相关的代码
"""

""" START 运行时动态替换EasyOCR警告问题"""
import torch.utils.data
# 保存原始 DataLoader
original_dataloader = torch.utils.data.DataLoader

# 定义新的 DataLoader 临时解决等待官方更新
def patched_dataloader(*args, **kwargs):
    kwargs['pin_memory'] = settings.USE_GPU  # 强制覆盖 pin_memory
    return original_dataloader(*args, **kwargs)
# 替换 DataLoader
torch.utils.data.DataLoader = patched_dataloader
""" END 运行时动态替换EasyOCR警告问题"""

from typing import Any
import cv2
import numpy as np
from PIL import ImageGrab
import easyocr
import settings

"""初始化全局EasyOCR"""
reader = easyocr.Reader(['ch_sim'], gpu=settings.USE_GPU, verbose=False)


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
    # resize.save("get_text.png")  # 查看当前图片
    array = image_array(resize)  # 将图像转换成数组
    # grayscale = image_grayscale(array)  # 图像转换为灰度，使OCR更容易破译字符
    # thresholding = image_thresholding(grayscale)  # 将阈值化应用于图像
    if array is not None:
        try:
            result = reader.readtext(array, add_margin=0.2, text_threshold=0.5)
        except Exception as e:
            # print("get_text异常:", e)
            return ""

    if result.__len__() != 0:
        return result[0][1]

    return ""


def get_text_from_image(image: ImageGrab.Image) -> str:
    """从图片中获取文本"""
    result = ""

    resize = image_resize(image, 1)  # 调整图像大小
    resize2 = image_resize(image, 3)  # 调整图像大小

    # resize.save("get_text_from_image.png")  # 测试当前图片

    array = image_array(resize)  # 将图像转换成数组
    array2 = image_array(resize2)  # 将图像转换成数组

    if array is not None:
        try:
            result = reader.readtext(array, add_margin=0.2, text_threshold=0.5)
            if result.__len__() == 0:
                result = reader.readtext(array2, add_margin=0.2, text_threshold=0.5)

        except RuntimeError as e:
            # print("运行的异常不管")
            return ""
        except Exception as e:
            # print("get_text_from_image异常:", e)
            return ""

    if result.__len__() != 0:
        return result[0][1]
    return ""
