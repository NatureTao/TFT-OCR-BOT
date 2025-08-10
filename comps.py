"""
该机器人使用的队伍配置
配置信息来自 https://tftactics.gg/tierlist/team-comps
物品采用驼峰式命名，并使用 a-z 字母
物品将首先放置在最上方的英雄位置，并优先在左侧进行装备物品的配置。
"""
import json
import os
from pathlib import Path

# COMP = {}
# # 强化白名单
# AUGMENTS: list[str] = []
# # 异常突变白名单
# ABRUPT_ANOMALY: list[str] = []
# # 强化黑名单
# AVOID_AUGMENTS: list[str] = []

# 1. 直接定义路径
basePath = Path(__file__).parent / "squads"
configPath = Path(__file__).parent / "config" / "setting.json"

# 2. 直接读取 setting.json 获取阵容名称
try:
    with open(configPath, "r", encoding="utf-8") as f:
        setting_data = json.load(f)
    selected_squad = setting_data.get("游戏运营", {}).get("选择阵容", "")

except Exception as e:
    print(f"读取配置文件失败: {e}")
    selected_squad = ""

# 3. 加载阵容文件
if selected_squad and os.path.exists(basePath):
    json_path = basePath / f"{selected_squad}.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                existingData = json.load(f)
            print(f"成功加载阵容: {selected_squad}")
        except Exception as e:
            print(f"阵容文件解析失败: {e}")
    else:
        print(f"阵容文件不存在: {json_path}")
else:
    print("未选择阵容或路径不存在")
COMP = existingData['COMP']
AUGMENTS: list[str] = existingData['AUGMENTS']
AVOID_AUGMENTS: list[str] = existingData['AVOID_AUGMENTS']
FRUIT: list[str] = existingData['FRUIT']
AVOID_FRUIT: list[str] = existingData['AVOID_FRUIT']


def champions_to_buy() -> dict:
    """返回需要购买英雄的数量 以达到目标星级"""
    champs_to_buy: dict = {}
    for champion, champion_data in COMP.items():
        if champion_data["level"] == 1:
            champs_to_buy[champion] = 1
        elif champion_data["level"] == 2:
            champs_to_buy[champion] = 3
        elif champion_data["level"] == 3:
            champs_to_buy[champion] = 9
        else:
            raise ValueError("Comps.py | Champion level must be a valid level (1-3)")
    return champs_to_buy


def get_unknown_slots() -> list:
    """创建棋盘上没有冠军的位置列表"""
    container: list = []
    for _, champion_data in COMP.items():
        container.append(champion_data["board_position"])
    return [n for n in range(27) if n not in container]


def get_key(comps, index: int) -> str:
    """
     @param comps:预设阵容列表
     @param index:查询英雄棋盘位置
     @return: 英雄名称
    """
    return next((k for k, v in comps.items() if any(goal == index for goal in v.values())), None)

if __name__ == '__main__':
    pass