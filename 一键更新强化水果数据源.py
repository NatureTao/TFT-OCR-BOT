# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT
"""
from pathlib import Path

import requests
from fake_useragent import UserAgent
import os
import re
import json
from typing import Dict, Any


def get_user_agent():  # 伪装浏览器
    ua = UserAgent()
    user_agent = ua.random
    return user_agent


def getData(url: str):
    temp = []

    json_data = askURL(url)
    items = json_data.get('data')
    # 构建符合我们格式的数据
    for tag in items:
        temp.append(items[tag].get('title'))
    return temp


def askURL(url: str):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Pragma": "no-cache",
        "User-Agent": get_user_agent()
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        # 解析JSON数据
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


def updateChange(items):
    basePath = Path(__file__).parent / "config"
    print(basePath)
    if os.path.exists(basePath):
        if os.path.isfile(existing_path := os.path.join(basePath,"resource.json")):
            try:
                with open(existing_path, "r", encoding="utf-8") as f:
                    existingData = json.load(f)
                    # 读取文件 替换数据
                    existingData["FRUIT"] = items

                with open(existing_path, "w", encoding="utf-8") as f:
                    json.dump(existingData, f, ensure_ascii=False, indent=4)

                print("更新完成")

            except Exception as e:
                print(e)
        else:
            print("未找到文件")
    else:
        print("未找到文件夹")


if __name__ == '__main__':
    baseurl = "https://game.gtimg.cn/images/lol/act/img/tft/js/15.15-2025.S15/fruit.js"  # 目标网页
    data_list = getData(baseurl)
    updateChange(data_list)
    # print("更新完成!")
