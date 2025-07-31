"""
Handles sending input to the game, coords contain a cartesian ordered pair (x, y)
负责向游戏发送输入，coords包含一个笛卡儿有序对(x, y)
"""

import random
import pydirectinput
pydirectinput.FAILSAFE=False

def left_click(coords: tuple) -> None:
    """Left clicks at argument ones coordinates"""
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords[0] - offset, coords[1] - offset)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()


def left_click_drag(coords1: tuple,coords2: tuple) -> None:
    """位置1 点击拖动鼠标到 位置2"""
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords1[0] - offset, coords1[1] - offset)
    pydirectinput.mouseDown()
    pydirectinput.moveTo(coords2[0] - offset, coords2[1] - offset)
    pydirectinput.mouseUp()


def right_click(coords: tuple) -> None:
    """Right clicks at argument ones coordinates"""
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords[0] - offset, coords[1] - offset)
    pydirectinput.mouseDown(button="right")
    pydirectinput.mouseUp(button="right")


def press_e(coords: tuple) -> None:
    """Presses e at argument ones coordinates"""
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords[0] - offset, coords[1] - offset)
    pydirectinput.press("e")


def move_mouse(coords: tuple) -> None:
    """Moves mouse to argument ones coordinates"""
    pydirectinput.moveTo(coords[0], coords[1])


def buy_xp() -> None:
    """Presses hotkey to purchase XP"""
    pydirectinput.press("f")


def reroll() -> None:
    """Presses hotkey to purchase reroll"""
    pydirectinput.press("d")


def press_esc() -> None:
    """Presses escape key"""
    pydirectinput.press("esc")
