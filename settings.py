"""
    程序参数设置
"""
import json
import os
from pathlib import Path

existingData = None
basePath = Path(__file__).parent / "config"
if os.path.exists(basePath):
    if os.path.isfile(existing_path := os.path.join(basePath, "setting.json")):
        try:
            with open(existing_path, "r", encoding="utf-8") as f:
                existingData = json.load(f)
        except Exception as e:
            print(e)
    else:
        print("未找到文件")
else:
    print("未找到文件夹")


"""系统设置"""
GAME_HWND_NAME = existingData["系统设置"]["游戏窗口"]  # 检测游戏加载窗口名
USE_GPU = existingData["引擎设置"]["调用显卡"]  # 英伟达显卡设置 True AMD或其他显卡设置 False
UI_FONT = existingData["系统设置"]["标记字体"]  # 设置屏幕标记字体
UI_COLOR = tuple(existingData["系统设置"]["标记颜色"])   # 设置屏幕字体颜色

"""引擎设置"""
DET_DB_SCORE_MODE = existingData["引擎设置"]["模型"]  # fast/slow模式
USE_MP = existingData["引擎设置"]["多进程"]  # 是否开启多进程预测
TOTAL_PROCESS_NUM = existingData["引擎设置"]["多进程数"]  # 开启的进程数

"""游戏挂机设置"""
QUEUE_ID = existingData["挂机设置"]["游戏模式"]  # 1090匹配 1100排位
FORFEIT = existingData["挂机设置"]["主动投降"]  # 是否主动投降
FORFEIT_TIME = existingData["挂机设置"]["投降时间"]  # 投降时间(秒)
NUMBER_OF_HANGING_UP_GAMES = existingData["挂机设置"]["对局次数"]  # 对局次数后关机
AUTO_POWER_OFF = existingData["挂机设置"]["自动关机"]  # 是否自动关机

"""游戏运营设置"""
MIN_GOLD = existingData["游戏运营"]["最小金币"]  # 最小预留金币
MAX_GOLD = existingData["游戏运营"]["最大金币"]  # 最大预留金币

MAX_ITEM = existingData["游戏运营"]["装备阈值"]  # 装备数量达到阈值就随机上装备
RANDOM_MAX_ITEM = existingData["游戏运营"]["随机上装备"]  # 装备数量随机上装备开关
HEALTH = existingData["游戏运营"]["生命阈值"]  # 生命值达到阈值就随机给装备
RANDOM_ITEM = existingData["游戏运营"]["生命值低随机上装备"]  # 生命值随机上装备开关

UPGRADE_LEVEL = existingData["游戏运营"]["不买经验等级"]  # 指定等级内不购买经验
BUY_EXP_REFRESH_STORE = existingData["游戏运营"]["购买经验刷新商店"]  # 购买经验循环是否刷新商店




# """系统设置"""
# GAME_HWND_NAME = 'League of Legends (TM) Client'  # 检测游戏加载窗口名
# USE_GPU = False  # 英伟达显卡设置 True AMD或其他显卡设置 False
# UI_FONT = '宋体'  # 设置屏幕标记字体 -->  'STCaiyun','Microsoft YaHei'
# UI_COLOR = (252, 161, 4)  # 设置屏幕字体颜色
#
# """引擎设置"""
# DET_DB_SCORE_MODE = 'fast'  # fast是根据polygon的外接矩形边框内的所有像素计算平均得分，slow是根据原始polygon内的所有像素计算平均得分，计算速度相对较慢一些，但是更加准确一些。
# USE_MP = False  # 是否开启多进程预测 True False
# TOTAL_PROCESS_NUM = 2  # 开启的进程数，USE_MP为True时生效
#
# """游戏挂机设置"""
# QUEUE_ID = 1090  # 1090匹配 1100排位
# FORFEIT = False  # 是否主动投降
# FORFEIT_TIME = 600  # 多久投降 单位 秒 目前10分钟投降
# NUMBER_OF_HANGING_UP_GAMES = 3  # 进行多少次对局 后关机
# AUTO_POWER_OFF = False  # 是否自动关机
#
# """游戏运营设置"""
# MIN_GOLD = 6  # 最小预留金币
# MAX_GOLD = 56  # 最大预留金币
#
# MAX_ITEM = 18  # 装备数量达到阈值就随机上装备 最大20
# RANDOM_MAX_ITEM = True  # 装备数量随机上装备开关 True False
# HEALTH = 25  # 生命值达到阈值就随机给装备
# RANDOM_ITEM = True  # 生命值随机上装备开关 True False
#
# UPGRADE_LEVEL = [8, ]  # 指定等级内不购买经验
# TARGET_HERO_INDEX_SATISFY_GRADE = 5  # C位满足预设等级 忽略上面不购买经验 填写C位下标
# BUY_EXP_REFRESH_STORE = True  # 购买经验循环是否刷新商店
#
# MAX_REFRESH_ABNORMAL = 20  # 4-6异常突变BUFF尝试刷新多少次
# HERO_COUNTER_INDEX = 0  # C位下标
