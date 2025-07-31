import time
from time import sleep

import ocr
import screen_coords



def get_round_remaining_time() -> int:
    """返回回合剩于时间"""
    try:
        second = int(ocr.get_text(screenxy=screen_coords.REMAINING_TIME_POS.get_coords(), scale=1))
        return second
    except ValueError:
        return -1


if __name__ == '__main__':
    while True:
        start = time.perf_counter()
        s = get_round_remaining_time()
        end = time.perf_counter()

        runTime = end - start
        print("运行时间：", runTime)
        print(s)
        sleep(1)
