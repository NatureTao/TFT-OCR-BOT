"""
处理进入游戏
"""
import os
import re
from time import sleep
import json
from requests.auth import HTTPBasicAuth
import requests
import urllib3

import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.system('chcp 65001')  # 设置cmd窗口字符


def create_lobby(client_info: tuple) -> bool:
    """创建一个房间"""
    payload: dict[str, int] = {"queueId": settings.QUEUE_ID}
    payload: dict[str, int] = json.dumps(payload)
    try:
        status = requests.post(
            f"{client_info[1]}/lol-lobby/v2/lobby/",
            payload,
            auth=HTTPBasicAuth('riot', client_info[0]),
            timeout=10,
            verify=False,
        )
        if status.status_code == 200:
            print("  游戏大厅")
            return True
        return False
    except ConnectionError:
        return False


def start_queue(client_info: tuple) -> bool:
    """Starts queue"""
    try:
        status = requests.post(
            f"{client_info[1]}/lol-lobby/v2/lobby/matchmaking/search",
            auth=HTTPBasicAuth('riot', client_info[0]),
            timeout=10,
            verify=False,
        )
        if status.status_code == 204:
            print("  队列中")
            return True
        return False
    except ConnectionError:
        return False


def check_queue(client_info: tuple) -> bool:
    """检查队列，看看我们是否正在搜索"""
    try:
        status = requests.get(
            f"{client_info[1]}/lol-lobby/v2/lobby/matchmaking/search-state",
            auth=HTTPBasicAuth('riot', client_info[0]),
            timeout=10,
            verify=False,
        )
        return status.json()['searchState'] == 'Searching'
    except ConnectionError:
        return False


def check_game_status(client_info: tuple) -> bool:
    """检查我们是否在游戏中"""
    try:
        status = requests.get(
            f"{client_info[1]}/lol-gameflow/v1/session",
            auth=HTTPBasicAuth('riot', client_info[0]),
            timeout=10,
            verify=False,
        )
        return status.json().get("phase", "None")
    except ConnectionError:
        return False


def accept_queue(client_info: tuple) -> bool:
    """Accepts the queue"""
    requests.post(
        f"{client_info[1]}/lol-matchmaking/v1/ready-check/accept",
        auth=HTTPBasicAuth('riot', client_info[0]),
        timeout=10,
        verify=False,
    )


def change_arena_skin(client_info: tuple) -> bool:
    """更改竞技场皮肤为默认，其他竞技场皮肤有不同的坐标"""
    try:
        status = requests.delete(
            f"{client_info[1]}/lol-cosmetics/v1/selection/tft-map-skin",
            auth=HTTPBasicAuth('riot', client_info[0]),
            timeout=10,
            verify=False,
        )
        if status.status_code == 204:
            print("  更改棋盘皮肤为:默认")
            return True
        return False
    except ConnectionError:
        return False


def get_client() -> tuple:
    """获取英雄联盟客户端数据 如端口 令牌"""
    print(f"=====自动匹配对局=====")
    remoting_auth_token = ""
    server_url = ""
    re_app_port = re.compile(r'--app-port=([0-9]*)')  # 获取 app_port 的正则表达式
    re_remoting_auth_token = re.compile(r'--remoting-auth-token=([\w-]*)')  # 获取 remoting_auth_token 的正则表达式

    cmd = 'WMIC PROCESS WHERE name="LeagueClientUx.exe" GET commandline'  # 通过命令获取进程启动信息

    got_lock_file = False
    while not got_lock_file:
        game_data = "".join(os.popen(cmd).readlines())
        if '\n\n\n\n' != game_data:  # No Instance(s) Available.
            app_port: str = re.findall(re_app_port, game_data)[0]
            remoting_auth_token: str = re.findall(re_remoting_auth_token, game_data)[0]
            server_url: str = f"https://127.0.0.1:{app_port}"
            got_lock_file = True
        else:
            print("英雄联盟客户端未打开!10秒后再检测一次。")
            sleep(10)
    print("客户端已启动～(∠・ω< )⌒☆",flush=True)

    return remoting_auth_token, server_url





def reconnect(client_info: tuple) -> None:
    """发现连接失败重新连接英雄"""
    requests.post(
        f"{client_info[1]}/lol-gameflow/v1/reconnect",
        auth=HTTPBasicAuth('riot', client_info[0]),
        timeout=10,
        verify=False,
    )


def queue() -> None:
    """进入对局的方法"""

    client_info: tuple = get_client()
    # 检测是否在游戏内
    while check_game_status(client_info) == "InProgress":
        sleep(2)
    # 检测是否需要重新连接
    if check_game_status(client_info) == "Reconnect":
        print("重新连接游戏")
        reconnect(client_info)
        return
    # 上面条件都不是 创建一个房间
    while not create_lobby(client_info):
        sleep(3)

    # 修改竞技场皮肤
    change_arena_skin(client_info)

    sleep(3)

    while state := check_game_status(client_info):
        if state == "None":
            create_lobby(client_info)
        if state == "Lobby":
            start_queue(client_info)
        if state == "ReadyCheck":
            accept_queue(client_info)
            print("等待其他玩家接受")
        if state == "InProgress":
            return
        sleep(3)


if __name__ == '__main__':
    print(get_client())
