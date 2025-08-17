"""
包含与机器人使用的单个棋盘槽相关的所有信息
"""


class Champion:
    """英雄类，包含关于棋盘或备战区上的单个单位的信息"""

    # pylint: disable=too-many-instance-attributes,too-few-public-methods,too-many-arguments

    def __init__(self, name: str, coords: tuple, build, slot: int, size: int, final_comp: bool,
                 trait1: str,
                 trait2: str,
                 trait3: str,
                 center) -> None:

        self.name: str = name
        self.coords: tuple = coords
        self.build = build
        self.index: int = slot
        self.size: int = size
        self.completed_items: list = []
        self.current_building: list = []
        self.final_comp: bool = final_comp
        self.traits = [trait1, trait2, trait3] # 英雄羁绊

        self.center: bool = center # C 位标记
        self.eatenFruit = False # 使用强化果实标记
        self.expect_fruit = False # 是否是预期的水果

    def does_need_items(self) -> bool:
        """返回 英雄 实例是否需要装备"""
        return len(self.completed_items) != 3 or len(self.build) + len(self.current_building) == 0

    def does_need_trait(self) -> bool:
        """返回当前英雄是否还有装备栏位置"""
        return len(self.completed_items) != 3 and len(self.build) + len(self.current_building) <= 2

    def hero_type(self) -> bool:
        """获取英雄类型 前排返回False  后排返回True """
        return 0 <= self.index <= 13

    def check_trait(self, item: str) -> bool:
        """判断装备栏纹章 是否和当前英雄相同羁绊"""
        if not item or not isinstance(item, str):  # 过滤None/空字符串/非字符串
            return False

        trait_to_check = item.replace("纹章", "")
        return trait_to_check not in self.traits and "纹章" in item

    def check_center(self) -> bool:
        """ 是否为C位"""
        return self.center

    def check_eaten_fruit(self) -> bool:
        """使用过水果"""
        return self.eatenFruit

    def check_expect_fruit(self) -> bool:
        """是否预期水果"""
        return self.expect_fruit

if __name__ == '__main__':
    cm = Champion("阿木木", None, None, None, None, None, "监察", None, None,center=True)
    print(cm.check_trait("锁子甲"))
    print(cm.check_trait("监察纹章"))
