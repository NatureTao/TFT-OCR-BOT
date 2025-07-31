import arena_functions
import comps
import mk_functions
import screen_coords

if __name__ == '__main__':

    # wand_name: str = arena_functions.get_wand()
    # print(wand_name)
    # print("模拟购买魔杖BUFF")
    # mk_functions.left_click(screen_coords.WAND_LOC.get_coords())

    wand_name: str = arena_functions.get_abnormal()
    print("Wand_name = ",wand_name)
    for potential in comps.ABRUPT_ANOMALY:
        if potential in wand_name:
            print(f"  选择魔杖BUFF {wand_name}")
            # mk_functions.left_click(screen_coords.WAND_LOC.get_coords())






