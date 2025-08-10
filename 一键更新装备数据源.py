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
    temp = []
    BASIC_ITEM: set[str] = set()  # 基本装备 1
    COMBINED_ITEMS: set[str] = set()  # 合成装备 2
    FULL_ITEMS = {}  # 合成公式
    NON_CRAFTABLE_ITEMS: set[str] = set()  # 特殊装备 4 5 7
    SACRED_MATCHED_GROUP:dict[str,str] = dict()

    json_data = askURL(url)
    # 构建符合我们格式的数据
    for item in json_data.get("data", []):
        if item['type'] == '1':
            # 处理一个游戏自带的BUG显示问题
            name = item['name'] = "暴风之剑" if item['name'] == "暴风大剑" else item['name']
            BASIC_ITEM.add(name)
            BASIC_ITEM.add("不稳定的" + name)

        elif item['type'] == '2':
            COMBINED_ITEMS.add(item['name'])
            # 获取合成配方
            formula = item['formula'].split(',')
            for _ in json_data.get("data", []):
                # 第一个装备
                if _['equipId'] == formula[0]:
                    # 如果相同直接合成跳过循环
                    if formula[0] == formula[1]:
                        name = _['name'] = "暴风之剑" if _['name'] == "暴风大剑" else _['name']
                        FULL_ITEMS[item['name']] = (name, name)
                    else:
                        for __ in json_data.get("data", []):
                            # 第二个装备
                            if __['equipId'] == formula[1]:
                                name = _['name'] = "暴风之剑" if _['name'] == "暴风大剑" else _['name']
                                name2 = __['name'] = "暴风之剑" if __['name'] == "暴风大剑" else __['name']
                                FULL_ITEMS[item['name']] = (name, name2)
        elif item['type'] == '3':
            prefix = item['name'].partition("版")[0] + item['name'].partition("版")[1]
            suffix = item['name'].partition("版")[2]
            SACRED_MATCHED_GROUP[prefix+suffix] = suffix

        elif item['type'] == '4' or item['type'] == '5' or item['type'] == '7':
            NON_CRAFTABLE_ITEMS.add(item['name'])
    # 添加一些额外数据
    BASIC_ITEM.add("次级英雄复制器")
    BASIC_ITEM.add("英雄复制器")
    BASIC_ITEM.add("装备拆卸器")
    BASIC_ITEM.add("重铸器")
    BASIC_ITEM.add("装备重铸器")
    BASIC_ITEM.add("强化果实移除器")
    BASIC_ITEM.add("强化果实")

    temp.append(BASIC_ITEM)
    temp.append(COMBINED_ITEMS)
    temp.append(FULL_ITEMS)
    temp.append(NON_CRAFTABLE_ITEMS)
    temp.append(SACRED_MATCHED_GROUP)

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


def updateChange(data_list) -> None:
    """
    覆写 game_assets.py 文件中的多个容器内容，包括 BASIC_ITEM、COMBINED_ITEMS、FULL_ITEMS 和 NON_CRAFTABLE_ITEMS。

    :param data_list: 包含四个元素的列表，分别是基本装备、合成装备、合成公式和不可合成的装备。
    """
    file_path = os.path.join(os.path.dirname(__file__), "game_assets.py")

    # 读取目标文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # print("文件内容：")
    # print(content)  # 打印文件内容，确认格式

    # 定义容器名称和对应的正则表达式模式
    containers = [
        ("BASIC_ITEM", r"^( *BASIC_ITEM\s*:.*?=\s*)(\{\s*.*?\s*\})"),
        ("COMBINED_ITEMS", r"^( *COMBINED_ITEMS\s*:.*?=\s*)(\{\s*.*?\s*\})"),
        ("FULL_ITEMS", r"^( *FULL_ITEMS\s*=\s*)(\{\s*.*?\s*\})"),
        ("NON_CRAFTABLE_ITEMS", r"^( *NON_CRAFTABLE_ITEMS\s*:.*?=\s*)(\{\s*.*?\s*\})")
    ]

    # 遍历每个容器并更新内容
    for i, (container_name, pattern) in enumerate(containers):
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

        if not match:
            print(f"正则表达式未匹配到 {container_name} 定义")
            raise ValueError(f"无法在文件中找到 {container_name} 容器定义")

        # print(f"匹配到的内容：{match.group(0)}")  # 打印匹配到的内容

        # 计算原始缩进
        base_indent = match.group(1)
        indent_size = len(base_indent) - len(base_indent.lstrip())
        indent = ' ' * indent_size

        # 获取新数据
        new_data = data_list[i]

        # 根据容器类型生成字符串
        if isinstance(new_data, set):  # 处理集合类型
            formatted_data = "{" + ", ".join([f"'{item}'" for item in sorted(new_data)]) + "}"
        elif isinstance(new_data, dict):  # 处理字典类型
            json_str = json.dumps(new_data, indent=4, ensure_ascii=False)
            lines = json_str.split('\n')

            # 重新应用缩进
            formatted_lines = []
            for j, line in enumerate(lines):
                if j == 0:
                    formatted_lines.append(line)
                else:
                    formatted_lines.append(indent + line)

            formatted_data = '\n'.join(formatted_lines).replace('"', "'")
        else:
            raise TypeError(f"不支持的数据类型：{type(new_data)}")

        # 替换容器内容
        content = content[:match.start(2)] + formatted_data + content[match.end(2):]

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def updateToJson(data_list) -> None:

    basePath = Path(__file__).parent / "config"
    print(data_list)
    if os.path.exists(basePath):
        if os.path.isfile(existing_path := os.path.join(basePath,"resource.json")):
            try:
                with open(existing_path, "r", encoding="utf-8") as f:
                    existingData = json.load(f)
                    existingData["BASIC_ITEM"] = list(data_list[0])
                    existingData["COMBINED_ITEMS"] = list(data_list[1])
                    existingData["FULL_ITEMS"] = data_list[2]
                    existingData["NON_CRAFTABLE_ITEMS"] = list(data_list[3])
                    existingData["SACRED_MATCHED_GROUP"] = data_list[4]
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
    """可直接运行,会替换原数据"""
    baseurl = "https://game.gtimg.cn/images/lol/act/img/tft/js/equip.js"  # 目标网页
    data_list = getData(baseurl)
    # updateChange(data_list)
    # print(data_list)
    updateToJson(data_list)
