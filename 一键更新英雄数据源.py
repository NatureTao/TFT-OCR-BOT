# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：一键更新数据源.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/11 17:17 
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
    temp: dict[str, dict[str, int | str]] = {}  # 存储数据容器

    json_data = askURL(url)
    # 构建符合我们格式的数据
    for item in json_data.get("data", []):
        jobs = item['jobs'].split(',')
        trait2 = jobs[0] if len(jobs) > 0 else ""
        trait3 = jobs[1] if len(jobs) > 1 else ""

        # 将英雄数据添加到 CHAMPIONS 容器中
        temp[item['displayName']] = {  # 使用 displayName 的值作为键
            "Gold": int(item['price']),  # 将 price 转为整数
            "Board Size": 1,  # 人口占位
            "Trait1": item['races'],  # 种族
            "Trait2": trait2,
            "Trait3": trait3
        }
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


def updateChange(new_champions: Dict[str, Dict[str, Any]]):
    """
    覆写 game_assets.py 中的 CHAMPIONS 字典，精确保持原始缩进

    :param new_champions: 新的英雄数据字典
    """
    file_path = os.path.join(os.path.dirname(__file__), "game_assets.py")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用更精确的正则匹配，捕获缩进
    pattern = r"^( *CHAMPIONS\s*:\s*dict\[.*?\]\s*=\s*)(\{.*?\})"

    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

    if not match:
        raise ValueError("无法在文件中找到 CHAMPIONS 字典定义")

    # 计算原始缩进
    base_indent = match.group(1)
    indent_size = len(base_indent) - len(base_indent.lstrip())
    indent = ' ' * indent_size

    # 生成带正确缩进的字典字符串
    json_str = json.dumps(new_champions, indent=4, ensure_ascii=False)
    lines = json_str.split('\n')

    # 重新应用缩进
    formatted_lines = []
    for i, line in enumerate(lines):
        if i == 0:
            formatted_lines.append(line)
        else:
            formatted_lines.append(indent + line)

    # 处理Python与JSON的语法差异
    formatted_dict = '\n'.join(formatted_lines)
    formatted_dict = (
        formatted_dict
        .replace('"', "'")
        .replace("false", "False")
        .replace("true", "True")
        .replace("null", "None")
    )

    # 构建新内容
    new_content = content[:match.start(2)] + formatted_dict + content[match.end(2):]

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def updateToJson(new_champions):
    basePath = Path(__file__).parent / "config"
    print(basePath)
    if os.path.exists(basePath):
        if os.path.isfile(existing_path := os.path.join(basePath, "resource.json")):
            try:
                with open(existing_path, "r", encoding="utf-8") as f:
                    existingData = json.load(f)
                    # 读取文件 替换数据
                    existingData["CHAMPIONS"] = new_champions

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
    """删除原数据容器后在运行"""
    baseurl = "https://game.gtimg.cn/images/lol/act/img/tft/js/chess.js"  # 目标网页
    data_list = getData(baseurl)
    # updateChange(data_list)
    updateToJson(data_list)

