""" 游戏固定事件数据 加载JSON数据入口 回合信息 """
import os
from pathlib import Path
import json

ROUNDS: set[str] = {"1-1", "1-2", "1-3", "1-4",
                    "2-1", "2-2", "2-3", "2-4", "2-5", "2-6", "2-7", "2-8",
                    "3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7", "3-8",
                    "4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7", "4-8",
                    "5-1", "5-2", "5-3", "5-4", "5-5", "5-6", "5-7", "5-8",
                    "6-1", "6-2", "6-3", "6-4", "6-5", "6-6", "6-7", "6-8",
                    "7-1", "7-2", "7-3", "7-4", "7-5", "7-6", "7-7", "7-8"}

SECOND_ROUND: set[str] = {"1-2"}

# 选秀回合
CAROUSEL_ROUND: set[str] = {"1-1", "2-4", "3-4", "4-4", "5-4", "6-4", "7-4"}

PVE_ROUND: set[str] = {"1-3", "1-4", "2-7", "3-7", "4-6", "4-7", "5-7", "6-7", "7-7"}

PVP_ROUND: set[str] = {"2-1", "2-2", "2-3", "2-5", "2-6",
                       "3-1", "3-2", "3-3", "3-5", "3-6",
                       "4-1", "4-2", "4-3", "4-5",
                       "5-1", "5-2", "5-3", "5-5", "5-6",
                       "6-1", "6-2", "6-3", "6-5", "6-6",
                       "7-1", "7-2", "7-3", "7-5", "7-6"}
# 拾取战利品回合
PICKUP_ROUNDS: set[str] = {"2-1", "3-1", "4-1", "4-3", "5-1", "6-1", "7-1"}

ANVIL_ROUNDS: set[str] = {"2-1", "2-5", "3-1", "3-5", "4-1", "4-5", "5-1", "5-5", "6-1", "6-5", "7-1", "7-5"}

# 强化符文回合
AUGMENT_ROUNDS: set[str] = {"2-1", "3-2", "4-2"}

# 这些回合给装备
ITEM_PLACEMENT_ROUNDS: set[str] = {
    "2-1", "2-5", "2-7",
    "3-3", "3-5", "3-7",
    "4-2", "4-3", "4-4", "4-7",
    "5-1", "5-2", "5-3", "5-4", "5-5", "5-7",
    "6-1", "6-2", "6-3", "6-5", "6-6", "6-7",
    "7-1", "7-2", "7-3", "7-5", "7-6", "7-7"
}
# 刚开始的回合
ENCOUNTER_ROUNDS: set[str] = {"0-0"}

# 自动投降回合
FINAL_COMP_ROUND = "5-5"

# 动态读取数据
existingData = {}
basePath = Path(__file__).parent / "config"
if os.path.exists(basePath):
    if os.path.isfile(existing_path := os.path.join(basePath, "resource.json")):
        try:
            with open(existing_path, "r", encoding="utf-8") as f:
                existingData = json.load(f)
        except Exception as e:
            print(e)
    else:
        print("未找到文件")
else:
    print("未找到文件夹")

# 基本装备
BASIC_ITEM = set(existingData['BASIC_ITEM'])
# 合成装备
COMBINED_ITEMS = set(existingData['COMBINED_ITEMS'])
# 合成表
FULL_ITEMS = existingData['FULL_ITEMS']
# 辅助装备
SUPPORT_ITEM = existingData['SUPPORT_ITEM']
# 不可合成的
NON_CRAFTABLE_ITEMS = existingData['NON_CRAFTABLE_ITEMS']
# 奥恩装备
ORNN_ITEMS = set(existingData['ORNN_ITEMS'])
# 光明装备
SACRED_ITEMS = set(existingData['SACRED_ITEMS'])
SACRED_MATCHED_GROUP = existingData['SACRED_MATCHED_GROUP']
# 英雄信息
CHAMPIONS = existingData['CHAMPIONS']
# 符文
RUNE = existingData['RUNE']
# 果实
FRUIT = existingData['FRUIT']

REAR_ITEMS = existingData['REAR_ITEMS']
FRONTLINE_ITEMS = existingData['FRONTLINE_ITEMS']

# 所有装备
ITEMS: set[str] = BASIC_ITEM.union(COMBINED_ITEMS).union(SUPPORT_ITEM).union(NON_CRAFTABLE_ITEMS).union(
    ORNN_ITEMS).union(SACRED_ITEMS)

# 铁砧奇遇
ANVIL_PORTALS: list[str] = [
    "基础装备锻造器",
    "神器锻造器"
]
# 假人等奇遇
DUMMY_PORTALS: list[str] = [
    "魔像训练师",
]
ADDITIONAL_AUGMENT: list[str] = [
    "黑入:笫四个强化符文",
]

def champion_board_size(champion: str) -> int:
    """Takes a string (champion name) and returns board size of champion"""
    return CHAMPIONS[champion]["Board Size"]


def champion_gold_cost(champion: str) -> int:
    """根据字符串（英雄名称）返回英雄购买需要的金币"""
    return CHAMPIONS[champion]["Gold"]
