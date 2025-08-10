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
    # [Vec2(28, 296), Vec4(GameWindow(127, 336, 290, 369))], 1
    # [Vec2(28, 347), Vec4(GameWindow(127, 387, 290, 420))], 2
    [Vec2(28, 296), Vec4(GameWindow(127, 336, 390, 379))],
    [Vec2(28, 347), Vec4(GameWindow(127, 387, 390, 430))],
    [Vec2(28, 398), Vec4(GameWindow(127, 438, 390, 481))],
    [Vec2(28, 449), Vec4(GameWindow(127, 489, 390, 532))],
    [Vec2(28, 500), Vec4(GameWindow(127, 540, 390, 583))],
    [Vec2(28, 551), Vec4(GameWindow(127, 591, 390, 634))],
    [Vec2(28, 602), Vec4(GameWindow(127, 642, 390, 685))],
    [Vec2(28, 653), Vec4(GameWindow(127, 693, 390, 736))],
    [Vec2(28, 704), Vec4(GameWindow(127, 744, 390, 787))],
    [Vec2(28, 755), Vec4(GameWindow(127, 795, 390, 838))],
    # 第二排
    [Vec2(79, 296), Vec4(GameWindow(178, 336, 441, 379))],
    [Vec2(79, 347), Vec4(GameWindow(178, 387, 441, 430))],
    [Vec2(79, 398), Vec4(GameWindow(178, 438, 441, 481))],
    [Vec2(79, 449), Vec4(GameWindow(178, 489, 441, 532))],
    [Vec2(79, 500), Vec4(GameWindow(178, 540, 441, 583))],
    [Vec2(79, 551), Vec4(GameWindow(178, 591, 441, 634))],
    [Vec2(79, 602), Vec4(GameWindow(178, 642, 441, 685))],
    [Vec2(79, 653), Vec4(GameWindow(178, 693, 441, 736))],
    [Vec2(79, 704), Vec4(GameWindow(178, 744, 441, 787))],
    [Vec2(79, 755), Vec4(GameWindow(178, 795, 441, 838))],

]
#回合位置
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
    Vec4(GameWindow(605, 0, 750, 24), use_screen_offset=False),
    Vec4(GameWindow(806, 0, 950, 24), use_screen_offset=False),
]

# 生命值
HEALTH_POS: Vec4 = Vec4(GameWindow(1760, 200, 1828, 747))
# 每个小小英雄
HEALTH_ITEM_POS: list[Vec4] = [
    Vec4(GameWindow(0, 10, 68, 42), use_screen_offset=False),
    Vec4(GameWindow(0, 82, 68, 115), use_screen_offset=False),
    Vec4(GameWindow(0, 154, 68, 188), use_screen_offset=False),
    Vec4(GameWindow(0, 226, 68, 261), use_screen_offset=False),
    Vec4(GameWindow(0, 298, 68, 334), use_screen_offset=False),
    Vec4(GameWindow(0, 370, 68, 407), use_screen_offset=False),
    Vec4(GameWindow(0, 442, 68, 480), use_screen_offset=False),
    Vec4(GameWindow(0, 514, 68, 553), use_screen_offset=False),
]

# 地区奇遇点击位置
PORTAL_AUGMENT_LOC: Vec2 = Vec2(809, 11)
# 地区奇遇识别位置
PORTAL_AUGMENT_POS: Vec4 = Vec4(GameWindow(712, 60, 1177, 95))

# 回合时间
REMAINING_TIME_POS: Vec4 = Vec4(GameWindow(1124, 4, 1162, 62))

# 新赛季异常突变BUFF购买位置
ABNORMAL_POS: Vec4 = Vec4(GameWindow(624, 934, 805, 960))
ABNORMAL_LOC: Vec2 = Vec2(1331, 948)

# 面板名称loc
PANEL_NAME_LOC: Vec4 = Vec4(GameWindow(1707, 320, 1821, 342))

# 钱包位置
GOLD_POS: Vec4 = Vec4(GameWindow(950, 883, 1010, 909))

# 4-6的时候钱包位置
GOLD_ABNORMAL_POS: Vec4 = Vec4(GameWindow(1317, 883, 1367, 907))

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
# 高级铁砧识别列表 偏移x +238
DIVINE_ANVIL_ITEM_POS: list[Vec4] = [
    Vec4(GameWindow(40, 0, 230, 36)),
    Vec4(GameWindow(278, 0, 468, 36)),
    Vec4(GameWindow(516, 0, 706, 36)),
    Vec4(GameWindow(754, 0, 944, 36)),
    Vec4(GameWindow(992, 0, 1182, 36)),
]
# 高级铁砧装备点击位置
DIVINE_ANVIL_LOC: list[Vec2] = [
    Vec2(400, 985),
    Vec2(638, 985),
    Vec2(876, 985),
    Vec2(1114, 985),
    Vec2(1352, 985),

]

# 现在退出
EXIT_NOW_POS: Vec4 = Vec4(GameWindow(910, 560, 1029, 583))

# 强化果实识别名称坐标
FRUITS_POS: list[Vec4] = [
    Vec4(GameWindow(449, 913, 667, 943)),
    Vec4(GameWindow(817, 919, 990, 942)),
    Vec4(GameWindow(1160, 918, 1338, 943)),
]
# 强化果实购买位置
FRUITS_LOC: list[Vec2] = [
    Vec2(550, 971),
    Vec2(890, 971),
    Vec2(1236, 971),
    ]

# 强化符文名称位置
AUGMENT_POS: list[Vec4] = [
    Vec4(GameWindow(420, 532, 687, 570)),
    Vec4(GameWindow(825, 532, 1095, 570)),
    Vec4(GameWindow(1233, 532, 1500, 570)),
]
# 强化符文购买位置
AUGMENT_LOC: list[Vec2] = [
    Vec2(549, 445),
    Vec2(955, 445),
    Vec2(1365, 445),
    ]

# 强化符文刷新位置
AUGMENT_ROLL: list[Vec2] = [Vec2(549, 875),
                            Vec2(960, 875),
                            Vec2(1363, 875),
                            # Vec2(1218, 860)
                            ]

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

# 拾取战利品坐标组
ITEM_PICKUP_LOC: list[Vec2] = [
    Vec2(1460, 611),
    Vec2(406, 544),
    Vec2(1435, 486),
    Vec2(450, 440),
    Vec2(1380, 381),
    Vec2(644, 323),
    Vec2(1297, 262),
    Vec2(590, 215),
]
# ITEM_PICKUP_LOC: list[Vec2] = [
#     Vec2(1490, 605),
#     Vec2(1293, 313),
#     Vec2(1093, 230),
#     Vec2(557, 194),
#     Vec2(683, 309),
# ]

# 备战区点击坐标
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
# 旋转木马拿装备点击坐标
CAROUSEL_LOC: Vec2 = Vec2(964, 610)

# 立即退出按钮坐标
EXIT_NOW_LOC: Vec2 = Vec2(963, 575)
# 购买经验按钮坐标
BUY_XP_LOC: Vec2 = Vec2(364, 964)
# 刷新商店按钮坐标
REFRESH_LOC: Vec2 = Vec2(364, 1039)

# 鼠标待机坐标
DEFAULT_LOC: Vec2 = Vec2(96, 222)

# 健康的地方
HEALTH_LOC: Vec2 = Vec2(1897, 126)

# 投降按钮坐标
SURRENDER_LOC: Vec2 = Vec2(771, 843)
# 投降按钮坐标2
SURRENDER_TWO_LOC: Vec2 = Vec2(832, 489)
