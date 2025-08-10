import time

import ocr
import screen_coords

if __name__ == '__main__':
    while True:
        time.sleep(1)
        fruits: list = []
        print("开始")
        for coords in screen_coords.FRUITS_POS:
            augment: str = ocr.get_text(
                screenxy=coords.get_coords(), scale=1
            )
            fruits.append(augment)
        print(f"  强化果实: {fruits}")
        if len(fruits) == 3 and "" not in fruits:
            break