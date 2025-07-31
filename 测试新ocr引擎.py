# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：测试新ocr引擎.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/12 0:12 
"""
import time

import easyocr

reader = easyocr.Reader(['ch_sim'], gpu=True)

start = time.perf_counter()
result = reader.readtext('get_text_from_image.png', add_margin=0.2, text_threshold=0.6)
end = time.perf_counter()
runTime = end - start


print(result)
for detection in result:
    print(detection[1])  # 识别结果

print("运行时间：", runTime)