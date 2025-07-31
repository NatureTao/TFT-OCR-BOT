# _*_ coding: utf-8 _*_
"""
@Project ：TFT-OCR-BOT 
@File    ：service.py
@IDE     ：PyCharm 
@Author  ：NatureTao
@Date    ：2025/4/14 15:00 
"""
import os
import re

from datetime import datetime
import psutil
import requests
import urllib3
from requests import RequestException
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_client_uptime() -> int:
    try:
        # 遍历所有进程，查找 LeagueClientUx.exe
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            if proc.info.get('name') == 'LeagueClientUx.exe':
                # 获取进程创建时间
                create_time = proc.info['create_time']
                creation_time = datetime.fromtimestamp(create_time)

                # 计算运行时间
                current_time = datetime.now()
                uptime = current_time - creation_time
                return uptime.seconds
        return 0
    except Exception as e:
        return 0


class LOLService(object):
    """用户客户端数据"""

    def __init__(self):
        self.remoting_auth_token = ""  # 临时密钥
        self.server_url = ""  # 临时端口

        self.pass_id = ""  # 通行证ID
        self.pass_name = "未知"  # 通行证名称
        self.currentLevel = 0  # 通行证等级
        self.currentLevelXP = 0  # 当前经验
        self.totalLevelXP = 0  # 升级经验

        self.gameName = "未知"  # 玩家昵称
        self.tagLine = "未知"  # 玩家标签
        self.profileIconId = "未知"  # 玩家头像ID
        self.avatar = None  # 玩家头像
        self.summonerLevel = 0  # 玩家等级
        self.xpSinceLastLevel = 0  # 玩家当前经验
        self.xpUntilNextLevel = 0  # 玩家升级经验

        self.RP = "未知"  # 点卷
        self.lol_blue_essence = 1919  # 蓝色精粹
        self.lol_orange_essence = 810  # 橙色精粹
        self.lol_mythic_essence = "未知"  # 神话精粹
        self.TFT_TREASURE_TROVE_TOKEN = "未知"  # 云石
        self.tft_standard_coin = "未知"  # 云顶召唤水晶
        self.tft_star_fragments = "未知"  # 星之碎片

        self.refresh_client()

    def empty(self):
        self.pass_id = ""  # 通行证ID
        self.pass_name = "等待游戏启动"  # 通行证名称
        self.currentLevel = 114514  # 通行证等级
        self.currentLevelXP = 0  # 当前经验
        self.totalLevelXP = 0  # 升级经验

        self.gameName = "未知"  # 玩家昵称
        self.tagLine = "未知"  # 玩家标签
        self.profileIconId = "未知"  # 玩家头像ID
        self.avatar = None  # 玩家头像
        self.summonerLevel = 0  # 玩家等级
        self.xpSinceLastLevel = 0  # 玩家当前经验
        self.xpUntilNextLevel = 0  # 玩家升级经验

        self.RP = "未知"  # 点卷
        self.lol_blue_essence = 1919  # 蓝色精粹
        self.lol_orange_essence = 810  # 橙色精粹
        self.lol_mythic_essence = "未知"  # 神话精粹
        self.TFT_TREASURE_TROVE_TOKEN = "未知"  # 云石
        self.tft_standard_coin = "未知"  # 云顶召唤水晶
        self.tft_star_fragments = "未知"  # 星之碎片

    def refresh_client(self):
        if get_client_uptime() < 25:
            self.empty()
            return
        try:
            # print("连接客户端")
            self.get_client()
            self.get_player_info()
            self.get_pass_info()
            self.get_avatar()
            self.get_player_wallet()

        except ConnectionError as e:
            self.empty()
        except RequestException as e:
            self.empty()
            pass
            # raise RequestException("客户端正在启动中")
        except Exception as e:
            self.empty()
            pass

    def get_client(self) -> None:
        """获取英雄联盟客户端数据 如端口 令牌"""
        re_app_port = re.compile(r'--app-port=([0-9]*)')
        re_remoting_auth_token = re.compile(r'--remoting-auth-token=([\w-]*)')
        cmd = 'WMIC PROCESS WHERE name="LeagueClientUx.exe" GET commandline  2>nul'

        game_data = "".join(os.popen(cmd).readlines())
        if '\n\n\n\n' != game_data:
            app_port: str = re.findall(re_app_port, game_data)[0]
            self.remoting_auth_token: str = re.findall(re_remoting_auth_token, game_data)[0]
            self.server_url: str = f"https://127.0.0.1:{app_port}"
        else:
            raise ConnectionError("客户端未启动")

    def get_player_info(self) -> any:
        """获取玩家基本信息"""
        try:
            status = requests.get(
                f"{self.server_url}/lol-summoner/v1/current-summoner",
                auth=HTTPBasicAuth('riot', self.remoting_auth_token),
                timeout=10,
                verify=False,
            )
            if status.status_code == 200:
                self.gameName = status.json()["gameName"]
                self.profileIconId = status.json()["profileIconId"]
                self.summonerLevel = status.json()["summonerLevel"]
                self.tagLine = status.json()["tagLine"]
                self.xpSinceLastLevel = status.json()["xpSinceLastLevel"]
                self.xpUntilNextLevel = status.json()["xpUntilNextLevel"]
        except ConnectionError:
            return None

    def get_player_wallet(self) -> any:
        """获取玩家货币信息"""
        try:
            status = requests.get(
                f"{self.server_url}/lol-inventory/v1/wallet/me",
                auth=HTTPBasicAuth('riot', self.remoting_auth_token),
                timeout=10,
                verify=False,
            )
            if status.status_code == 200:
                self.RP = status.json().get('RP', "未知")  # 点卷
                self.lol_blue_essence = status.json().get('lol_blue_essence', "未知")  # 蓝色精粹
                self.lol_orange_essence = status.json().get('lol_orange_essence', "未知")  # 橙色精粹
                self.lol_mythic_essence = status.json().get('lol_mythic_essence', "未知")  # 神话精粹
                self.TFT_TREASURE_TROVE_TOKEN = status.json().get('TFT_TREASURE_TROVE_TOKEN', "未知")  # 云石
                self.tft_standard_coin = status.json().get('tft_standard_coin', "未知")  # 云顶召唤水晶
                self.tft_star_fragments = status.json().get('tft_star_fragments', "未知")  # 星之碎片

        except ConnectionError:
            return None

    def get_pass_info(self) -> any:
        """获取通行证基本信息"""
        try:
            status = requests.get(
                f"{self.server_url}/lol-event-hub/v1/events",
                auth=HTTPBasicAuth('riot', self.remoting_auth_token),
                timeout=10,
                verify=False,
            )
            if status.status_code == 200:
                self.pass_id = status.json()[len(status.json())-1]["eventId"]
                self.pass_name = status.json()[len(status.json())-1]["eventInfo"]['eventName']

                _ = requests.get(
                    f"{self.server_url}/lol-event-hub/v1/events/{self.pass_id}/reward-track/xp",
                    auth=HTTPBasicAuth('riot', self.remoting_auth_token),
                    timeout=10,
                    verify=False,
                )
                if _.status_code == 200:
                    self.currentLevel = _.json()['currentLevel']
                    self.currentLevelXP = _.json()['currentLevelXP']
                    self.totalLevelXP = _.json()['totalLevelXP']

        except ConnectionError:
            return None

    def get_avatar(self) -> any:
        """获取用户客户端头像"""
        try:
            status = requests.get(
                f"{self.server_url}/lol-game-data/assets/v1/profile-icons/{self.profileIconId}.jpg",
                auth=HTTPBasicAuth('riot', self.remoting_auth_token),
                timeout=10,
                verify=False,
            )
            if status.status_code == 200:
                self.avatar = status.content
        except ConnectionError:
            return None


if __name__ == '__main__':
    lol = LOLService()
    print(lol.server_url, lol.remoting_auth_token)
    print("通行证名称: " + lol.pass_name)
    print("通行证等级: " + str(lol.currentLevel))
    print("当前经验: " + str(lol.currentLevelXP))
    print("升级经验: " + str(lol.totalLevelXP))
    print("玩家昵称: " + lol.gameName + "#" + lol.tagLine)
    print("玩家等级: " + str(lol.summonerLevel))
    print("玩家经验: " + str(lol.xpSinceLastLevel))
    print("玩家升级经验: " + str(lol.xpUntilNextLevel))
    print("蓝色精粹: " + str(lol.lol_blue_essence))
    print("橙色精粹: " + str(lol.lol_orange_essence))
    print("神话精粹: " + str(lol.lol_mythic_essence))
    print("点卷: " + str(lol.RP))
    print("云石: " + str(lol.TFT_TREASURE_TROVE_TOKEN))
    print("云顶召唤水晶: " + str(lol.tft_standard_coin))
    print("星之碎片: " + str(lol.tft_star_fragments))
