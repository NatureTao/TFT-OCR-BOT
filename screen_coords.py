"""
包含机器人使用的静态屏幕坐标
Screen coords for 1920x1080 screens
(x, y, x+w, y+h) for Vec4 locations, (x, y) for Vec2 locations
"""

from vec4 import Vec4, GameWindow
from vec2 import Vec2

# 备战期位置
BENCH_HEALTH_POS: list[Vec4] = [
    Vec4(GameWindow(369, 650, 472, 757)),
    Vec4(GameWindow(485, 650, 588, 757)),
    Vec4(GameWindow(601, 650, 704, 757)),
    Vec4(GameWindow(728, 650, 831, 757)),
    Vec4(GameWindow(844, 650, 947, 757)),
    Vec4(GameWindow(960, 650, 1063, 757)),
    Vec4(GameWindow(1076, 650, 1179, 757)),
    Vec4(GameWindow(1192, 650, 1295, 757)),
    Vec4(GameWindow(1308, 650, 1411, 757)),
]
# 装备栏
ITEM_POS: list[list] = [
    [Vec2(28, 296), Vec4(GameWindow(127, 336, 290, 369))],
    [Vec2(28, 347), Vec4(GameWindow(127, 387, 290, 420))],
    [Vec2(28, 398), Vec4(GameWindow(127, 438, 290, 471))],
    [Vec2(28, 449), Vec4(GameWindow(127, 489, 290, 522))],
    [Vec2(28, 500), Vec4(GameWindow(127, 540, 290, 573))],
    [Vec2(28, 551), Vec4(GameWindow(127, 591, 290, 624))],
    [Vec2(28, 602), Vec4(GameWindow(127, 642, 290, 675))],
    [Vec2(28, 653), Vec4(GameWindow(127, 693, 290, 726))],
    [Vec2(28, 704), Vec4(GameWindow(127, 744, 290, 777))],
    [Vec2(28, 755), Vec4(GameWindow(127, 795, 290, 828))],
    # 第二排
    [Vec2(79, 296), Vec4(GameWindow(178, 336, 341, 369))],
    [Vec2(79, 347), Vec4(GameWindow(178, 387, 341, 420))],
    [Vec2(79, 398), Vec4(GameWindow(178, 438, 341, 471))],
    [Vec2(79, 449), Vec4(GameWindow(178, 489, 341, 522))],
    [Vec2(79, 500), Vec4(GameWindow(178, 540, 341, 573))],
    [Vec2(79, 551), Vec4(GameWindow(178, 591, 341, 624))],
    [Vec2(79, 602), Vec4(GameWindow(178, 642, 341, 675))],
    [Vec2(79, 653), Vec4(GameWindow(178, 693, 341, 726))],
    [Vec2(79, 704), Vec4(GameWindow(178, 744, 341, 777))],
    [Vec2(79, 755), Vec4(GameWindow(178, 795, 341, 828))],

]
# 一轮POS
ROUND_POS: Vec4 = Vec4(GameWindow(753, 10, 870, 34))
# 第一轮
ROUND_POS_ONE: Vec4 = Vec4(GameWindow(0, 0, 40, 24), use_screen_offset=False)
# 第二轮
ROUND_POS_TWO: Vec4 = Vec4(GameWindow(16, 0, 56, 24), use_screen_offset=False)
# 第三轮
ROUND_POS_THREE: Vec4 = Vec4(GameWindow(71, 0, 110, 24), use_screen_offset=False)
# 圆形相遇图标
ROUND_ENCOUNTER_ICON_POS: list[list[Vec2, Vec4]] = [
    [Vec2(833, 20), Vec4(GameWindow(890, 49, 1218, 75))],
    [Vec2(869, 20), Vec4(GameWindow(926, 49, 1254, 75))],
    [Vec2(905, 20), Vec4(GameWindow(962, 49, 1290, 75))],
    [Vec2(941, 20), Vec4(GameWindow(998, 49, 1326, 75))],
    [Vec2(977, 20), Vec4(GameWindow(1034, 49, 1362, 75))],
    [Vec2(1013, 20), Vec4(GameWindow(1070, 49, 1398, 75))],
    [Vec2(1049, 20), Vec4(GameWindow(1106, 49, 1434, 75))],
    [Vec2(1085, 20), Vec4(GameWindow(1142, 49, 1470, 75))],
]

# 商店
SHOP_POS: Vec4 = Vec4(GameWindow(481, 1039, 1476, 1070))
# 英雄商店截图位置 0-4
CHAMP_NAME_POS: list[Vec4] = [
    Vec4(GameWindow(0, 0, 120, 24), use_screen_offset=False),
    Vec4(GameWindow(201, 0, 320, 24), use_screen_offset=False),
    Vec4(GameWindow(404, 0, 522, 24), use_screen_offset=False),
    Vec4(GameWindow(605, 0, 712, 24), use_screen_offset=False),
    Vec4(GameWindow(805, 0, 912, 24), use_screen_offset=False),
]

# 生命值
HEALTH_POS: Vec4 = Vec4(GameWindow(1777, 200, 1828, 747))
# 每个小小英雄 上10  下8
HEALTH_ITEM_POS: list[Vec4] = [
    Vec4(GameWindow(0, 10, 50, 42), use_screen_offset=False),
    Vec4(GameWindow(0, 82, 50, 115), use_screen_offset=False),
    Vec4(GameWindow(0, 154, 50, 188), use_screen_offset=False),
    Vec4(GameWindow(0, 226, 50, 261), use_screen_offset=False),
    Vec4(GameWindow(0, 298, 50, 334), use_screen_offset=False),
    Vec4(GameWindow(0, 370, 50, 407), use_screen_offset=False),
    Vec4(GameWindow(0, 442, 50, 480), use_screen_offset=False),
    Vec4(GameWindow(0, 514, 50, 553), use_screen_offset=False),
]

# 地区奇遇点击位置
PORTAL_AUGMENT_LOC: Vec2 = Vec2(500, 350)
# 地区奇遇识别位置
PORTAL_AUGMENT_POS: Vec4 = Vec4(GameWindow(660, 285, 845, 340))

# 回合时间
REMAINING_TIME_POS: Vec4 = Vec4(GameWindow(1074, 4, 1112, 62))

# 新赛季异常突变BUFF购买位置
ABNORMAL_POS: Vec4 = Vec4(GameWindow(624, 934, 805, 960))
ABNORMAL_LOC: Vec2 = Vec2(1331, 948)

# 面板名称loc
PANEL_NAME_LOC: Vec4 = Vec4(GameWindow(1707, 320, 1821, 342))
# 钱包位置
GOLD_POS: Vec4 = Vec4(GameWindow(960, 883, 1010, 909))
# 4-6的时候钱包位置
GOLD_ABNORMAL_POS: Vec4 = Vec4(GameWindow(1407, 883, 1457, 907))

# 判断是否是铁砧
ANVIL_MSG_POS: Vec4 = Vec4(GameWindow(818, 838, 932, 859))
# 铁砧装备栏
ANVIL_ITEMS_POS: Vec4 = Vec4(GameWindow(265, 987, 1486, 1026))

# 普通铁砧列表 偏移x +238
ORDINARY_ANVIL_ITEM_POS: list[Vec4] = [
    Vec4(GameWindow(160, 0, 350, 36)),
    Vec4(GameWindow(398, 0, 588, 36)),
    Vec4(GameWindow(639, 0, 826, 36)),
    Vec4(GameWindow(874, 0, 1064, 36)),
]

# 普通铁砧装备位置
ORDINARY_ANVIL_LOC: list[Vec2] = [
    Vec2(520, 980),
    Vec2(758, 980),
    Vec2(996, 980),
    Vec2(1234, 980),

]
# 高级铁砧列表 偏移x +238
DIVINE_ANVIL_ITEM_POS: list[Vec4] = [
    Vec4(GameWindow(40, 0, 230, 36)),
    Vec4(GameWindow(278, 0, 468, 36)),
    Vec4(GameWindow(516, 0, 706, 36)),
    Vec4(GameWindow(754, 0, 944, 36)),
    Vec4(GameWindow(992, 0, 1182, 36)),
]
# 高级铁砧装备位置
DIVINE_ANVIL_LOC: list[Vec2] = [
    Vec2(400, 985),
    Vec2(638, 985),
    Vec2(876, 985),
    Vec2(1114, 985),
    Vec2(1352, 985),

]

# 现在退出
EXIT_NOW_POS: Vec4 = Vec4(GameWindow(910, 560, 1029, 583))

# 强化符文名称位置
AUGMENT_POS: list[Vec4] = [

    Vec4(GameWindow(420, 532, 687, 570)),
    Vec4(GameWindow(825, 532, 1095, 570)),
    Vec4(GameWindow(1233, 532, 1500, 570)),
]
# 强化符文购买位置
AUGMENT_LOC: list[Vec2] = [Vec2(549, 445), Vec2(955, 445), Vec2(1365, 445)]
# 强化符文刷新位置
AUGMENT_ROLL: list[Vec2] = [Vec2(549, 875), Vec2(960, 875), Vec2(1363, 875)]

# 胜利POS
VICTORY_POS: Vec4 = Vec4(GameWindow(906, 560, 1030, 587))
# 买的地方
BUY_LOC: list[Vec2] = [
    Vec2(575, 992),
    Vec2(775, 992),
    Vec2(975, 992),
    Vec2(1175, 992),
    Vec2(1375, 992),
]
# 物品领取箱
# ITEM_PICKUP_LOC: list[Vec2] = [
#     Vec2(1460, 611),
#     Vec2(406, 544),
#     Vec2(1435, 486),
#     Vec2(450, 440),
#     Vec2(1380, 381),
#     Vec2(644, 323),
#     Vec2(1297, 262),
#     Vec2(590, 215),
# ]
ITEM_PICKUP_LOC: list[Vec2] = [
    Vec2(1490, 605),
    Vec2(1293, 313),
    Vec2(1093, 230),
    Vec2(557, 194),
    Vec2(683, 309),
]

# 板凳LOC
BENCH_LOC: list[Vec2] = [
    Vec2(425, 777),
    Vec2(542, 777),
    Vec2(658, 777),
    Vec2(778, 777),
    Vec2(892, 777),
    Vec2(1010, 777),
    Vec2(1128, 777),
    Vec2(1244, 777),
    Vec2(1359, 777),
]

# 这个列表从左下(0)到右上(27) 棋盘位置
BOARD_LOC: list[Vec2] = [
    Vec2(581, 651),
    Vec2(707, 651),
    Vec2(839, 651),
    Vec2(966, 651),
    Vec2(1091, 651),
    Vec2(1222, 651),
    Vec2(1349, 651),
    Vec2(532, 571),
    Vec2(660, 571),
    Vec2(776, 571),
    Vec2(903, 571),
    Vec2(1022, 571),
    Vec2(1147, 571),
    Vec2(1275, 571),
    Vec2(609, 494),
    Vec2(723, 494),
    Vec2(841, 494),
    Vec2(962, 494),
    Vec2(1082, 494),
    Vec2(1198, 494),
    Vec2(1318, 494),
    Vec2(557, 423),
    Vec2(673, 423),
    Vec2(791, 423),
    Vec2(907, 423),
    Vec2(1019, 423),
    Vec2(1138, 423),
    Vec2(1251, 423),
]
# 旋转木马LOC
CAROUSEL_LOC: Vec2 = Vec2(964, 620)
# 立即退出loc
EXIT_NOW_LOC: Vec2 = Vec2(963, 575)
# 购买xp loc
BUY_XP_LOC: Vec2 = Vec2(364, 964)
# 刷新LOC
REFRESH_LOC: Vec2 = Vec2(364, 1039)
# 默认的代码行
DEFAULT_LOC: Vec2 = Vec2(60, 222)
# 健康的地方
HEALTH_LOC: Vec2 = Vec2(1897, 126)
# 投降LOC
SURRENDER_LOC: Vec2 = Vec2(771, 843)
# 交出两枚loc
SURRENDER_TWO_LOC: Vec2 = Vec2(832, 489)
