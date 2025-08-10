"""
设置页面组件
"""
import os
from pathlib import Path

from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon, BodyLabel, ComboBoxSettingCard, \
    QConfig, qconfig, OptionsConfigItem, OptionsValidator, SwitchSettingCard, ConfigItem, BoolValidator, \
    RangeSettingCard, RangeConfigItem, RangeValidator, SingleDirectionScrollArea

from ColorSettingCard import ColorSettingCard, ColorValidator
from MultiSelectSettingCard import MultiSelectSettingCard


class Config(QConfig):
    # 系统设置
    GAME_HWND_NAME = OptionsConfigItem('系统设置','游戏窗口','League of Legends (TM) Client',OptionsValidator(['League of Legends (TM) Client']))
    UI_FONT = OptionsConfigItem('系统设置','标记字体','微软雅黑',OptionsValidator(['微软雅黑','等线','幼圆','黑体','楷体','宋体','梦源黑体 CN W16','梦源黑体 SC W16']))
    UI_COLOR =  ConfigItem("系统设置", "标记颜色", [255, 255, 255, 255], ColorValidator())


    # 引擎设置
    USE_GPG = ConfigItem("引擎设置", "调用显卡", False, BoolValidator())
    USE_MP = ConfigItem("引擎设置", "多进程", False, BoolValidator())
    TOTAL_PROCESS_NUM = RangeConfigItem("引擎设置", "多进程数", 2, RangeValidator(1, 10))
    DET_DB_SCORE_MODE = OptionsConfigItem('引擎设置','模型','fast',OptionsValidator(['fast','slow']))

    # 挂机设置
    QUEUE_ID = OptionsConfigItem('挂机设置','游戏模式',1090,OptionsValidator([1090,1100]))
    FORFEIT = ConfigItem("挂机设置", "主动投降", False, BoolValidator())
    FORFEIT_TIME = RangeConfigItem("挂机设置", "投降时间", 600, RangeValidator(600, 30000))
    AUTO_POWER_OFF = ConfigItem("挂机设置", "自动关机", False, BoolValidator())
    NUMBER_OF_HANGING_UP_GAMES = RangeConfigItem("挂机设置", "对局次数", 5, RangeValidator(1, 100))

    # 游戏运营
    MIN_GOLD = RangeConfigItem("游戏运营", "最小金币", 6, RangeValidator(0, 200))
    MAX_GOLD = RangeConfigItem("游戏运营", "最大金币", 56, RangeValidator(0, 200))
    RANDOM_MAX_ITEM = ConfigItem("游戏运营", "随机上装备", False, BoolValidator())
    MAX_ITEM = RangeConfigItem("游戏运营", "装备阈值", 18, RangeValidator(1, 20))
    RANDOM_ITEM = ConfigItem("游戏运营", "生命值低随机上装备", False, BoolValidator())
    HEALTH = RangeConfigItem("游戏运营", "生命阈值", 25, RangeValidator(1, 150))
    UPGRADE_LEVEL = ConfigItem("游戏运营", "不买经验等级", [1, 2, 3])
    BUY_EXP_REFRESH_STORE = ConfigItem("游戏运营", "购买经验刷新商店", False, BoolValidator())
    SELECTED_SQUAD = ConfigItem("游戏运营", "选择阵容", "", "")

cfg = Config()
qconfig.load(os.path.join(Path(__file__).parent.parent / "config","setting.json"), cfg)



class Setting(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName("设置")

        # 1. 创建主滚动区域
        scroll = SingleDirectionScrollArea(self)
        scroll.setWidgetResizable(True)  # 关键设置！
        scroll.setFrameShape(QFrame.Shape.NoFrame)  # 去除边框
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 禁用水平滚动


        # 2. 创建内容容器
        content_widget = QWidget()
        self.mainLayout = QVBoxLayout(content_widget)  # 注意：布局绑定到content_widget
        self.mainLayout.setSpacing(10)
        self.mainLayout.setContentsMargins(15, 10, 15, 15)  # 左,上,右,下


        font = QFont()
        font.setFamilies(["楷体","微软雅黑"])
        font.setPointSize(14)

        box1 = QVBoxLayout()
        box1.setContentsMargins(0, 0, 0, 0)
        self.subtitleLabel = BodyLabel("系统设置", self)
        self.subtitleLabel.setFixedHeight(30)  # 精确控制高度
        self.subtitleLabel.setFont(font)

        box1.addWidget(self.subtitleLabel)

        # 设置卡 游戏窗口
        self.windowNameCard = ComboBoxSettingCard(
            configItem=cfg.GAME_HWND_NAME,
            icon=FluentIcon.FIT_PAGE,
            title="游戏窗口",
            content="检测游戏加载窗口名",
            texts=['League of Legends (TM) Client'],
            parent=self
        )
        box1.addWidget(self.windowNameCard)


        # 设置卡 标记字体
        self.uiFontCard = ComboBoxSettingCard(
            configItem=cfg.UI_FONT,
            icon=FluentIcon.FONT,
            title="标记字体",
            content="游戏对局中标记英雄名称在屏幕上的字体",
            texts=['微软雅黑','等线','幼圆','黑体','楷体','宋体','梦源黑体CN','梦源黑体SC'],
            parent=self
        )
        box1.addWidget(self.uiFontCard)

        #设置卡 标记颜色
        self.uiColorCard = ColorSettingCard(
            icon=FluentIcon.PALETTE,
            title="标记颜色",
            content="游戏对局中标记在屏幕上的字体颜色",
            configItem=cfg.UI_COLOR,
            parent=self
        )
        box1.addWidget(self.uiColorCard)

        self.mainLayout.addLayout(box1)

        box2 = QVBoxLayout()
        box2.setContentsMargins(0, 0, 0, 0)  # 左, 上, 右, 下
        self.subtitleLabel = BodyLabel("引擎设置", self)
        self.subtitleLabel.setFixedHeight(30)  # 精确控制高度
        self.subtitleLabel.setFont(font)
        box2.addWidget(self.subtitleLabel)
        # 设置卡 得分模型
        self.scoreModeCard = ComboBoxSettingCard(
            configItem=cfg.DET_DB_SCORE_MODE,
            icon=FluentIcon.LEAF,
            title="模型",
            content="计算平均得分模型",
            texts=['效率','精准'],
            parent=self
        )
        box2.addWidget(self.scoreModeCard)

        # 设置卡 调用显卡
        self.useGpuCard = SwitchSettingCard(
            icon=FluentIcon.SPEED_MEDIUM,
            title="显卡加速",
            content="NVIDIA 启用 | AMD 禁用 | Intel 禁用 | 摩尔线程 禁用",
            configItem=cfg.USE_GPG
        )
        self.useGpuCard.setValue = setValue.__get__(self.useGpuCard)
        self.useGpuCard.switchButton.setText(
            self.tr('启用') if cfg.USE_GPG.value else self.tr('禁用'))
        box2.addWidget(self.useGpuCard)

        # 设置卡 多进程
        self.useMPCard = SwitchSettingCard(
            icon=FluentIcon.ROBOT,
            title="多进程",
            content="使用多进程预测结果",
            configItem=cfg.USE_MP
        )
        self.useMPCard.setValue = setValue.__get__(self.useMPCard)
        self.useMPCard.switchButton.setText(
            self.tr('启用') if cfg.USE_MP.value else self.tr('禁用'))
        box2.addWidget(self.useMPCard)

        self.processNumCard = RangeSettingCard(
                cfg.TOTAL_PROCESS_NUM,
                FluentIcon.IOT,
                title="进程数",
                content="使用多进程的数量"
            )
        box2.addWidget(self.processNumCard)
        self.mainLayout.addLayout(box2)

        box3 = QVBoxLayout()
        self.subtitleLabel = BodyLabel("挂机设置", self)
        self.subtitleLabel.setFixedHeight(30)  # 精确控制高度
        self.subtitleLabel.setFont(font)
        box3.addWidget(self.subtitleLabel)

        # 设置卡 游戏模式
        self.gameModeCard = ComboBoxSettingCard(
            configItem=cfg.QUEUE_ID,
            icon=FluentIcon.GAME,
            title="对局模式",
            content="游玩云顶之奕对局模式",
            texts=['匹配模式','排位模式'],
            parent=self
        )
        box3.addWidget(self.gameModeCard)

        # 设置卡 主动投降
        self.forfeitCard = SwitchSettingCard(
            icon=FluentIcon.FLAG,
            title="主动投降",
            content="达到可投降时间后执行",
            configItem=cfg.FORFEIT
        )
        self.forfeitCard.setValue = setValue.__get__(self.forfeitCard)
        self.forfeitCard.switchButton.setText(
            self.tr('启用') if cfg.FORFEIT.value else self.tr('禁用'))
        box3.addWidget(self.forfeitCard)

        # 设置卡 投降时间
        self.forfeitTimeCard = RangeSettingCard(
            cfg.FORFEIT_TIME,
            FluentIcon.STOP_WATCH,
            title="投降时间(秒)",
            content="设置多少秒后投降"
        )
        box3.addWidget(self.forfeitTimeCard)

        # 设置卡 自动关机
        self.autoPowerOffCard = SwitchSettingCard(
            icon=FluentIcon.POWER_BUTTON,
            title="自动关机",
            content="达到可指定对局后执行",
            configItem=cfg.AUTO_POWER_OFF
        )
        self.autoPowerOffCard.setValue = setValue.__get__(self.autoPowerOffCard)
        self.autoPowerOffCard.switchButton.setText(
            self.tr('启用') if cfg.AUTO_POWER_OFF.value else self.tr('禁用'))
        box3.addWidget(self.autoPowerOffCard)

        # 设置卡 达到多少对局后关机
        self.numberOfHangingUpGamesCard = RangeSettingCard(
            cfg.NUMBER_OF_HANGING_UP_GAMES,
            FluentIcon.DATE_TIME,
            title="对局次数",
            content="设置多少次对局后关机"
        )
        box3.addWidget(self.numberOfHangingUpGamesCard)
        self.mainLayout.addLayout(box3)

        box4 = QVBoxLayout()
        self.subtitleLabel = BodyLabel("游戏运营", self)
        self.subtitleLabel.setFixedHeight(30)  # 精确控制高度
        self.subtitleLabel.setFont(font)

        box4.addWidget(self.subtitleLabel)

        #设置卡 最小金币
        self.minGoldCard = RangeSettingCard(
            cfg.MIN_GOLD,
            FluentIcon.CALORIES,
            title="最小预留金币",
            content="游戏对局中预留最小的金币数量"
        )
        box4.addWidget(self.minGoldCard)

        self.maxGoldCard = RangeSettingCard(
            cfg.MAX_GOLD,
            FluentIcon.CALORIES,
            title="最大预留金币",
            content="游戏对局中预留最大的金币数量"
        )
        box4.addWidget(self.maxGoldCard)

        # 设置卡 随机装备开关
        self.randomMaxItemCard = SwitchSettingCard(
            icon=FluentIcon.QUESTION,
            title="装备太多随机给",
            content="",
            configItem=cfg.RANDOM_MAX_ITEM
        )
        self.randomMaxItemCard.setValue = setValue.__get__(self.randomMaxItemCard)
        self.randomMaxItemCard.switchButton.setText(
            self.tr('启用') if cfg.RANDOM_MAX_ITEM.value else self.tr('禁用'))
        box4.addWidget(self.randomMaxItemCard)

        # 设置卡 装备数量阈值
        self.maxItemCard = RangeSettingCard(
            cfg.MAX_ITEM,
            FluentIcon.QUESTION,
            title="装备数量阈值",
            content="装备太多随机给的阈值"
        )
        box4.addWidget(self.maxItemCard)

        # 设置卡 生命随机装备开关
        self.randomItemCard = SwitchSettingCard(
            icon=FluentIcon.HEART,
            title="生命值太低装备随机给",
            content="",
            configItem=cfg.RANDOM_ITEM
        )
        self.randomItemCard.setValue = setValue.__get__(self.randomItemCard)
        self.randomItemCard.switchButton.setText(
            self.tr('启用') if cfg.RANDOM_ITEM.value else self.tr('禁用'))
        box4.addWidget(self.randomItemCard)

        # 设置卡 生命值阈值
        self.healthCard = RangeSettingCard(
            cfg.HEALTH,
            FluentIcon.HEART,
            title="生命值阈值",
            content="生命值太多就随机给装备"
        )
        box4.addWidget(self.healthCard)

        # 设置卡 跳过等级

        self.upgradeLevelCard = MultiSelectSettingCard(
            configItem=cfg.UPGRADE_LEVEL,
            icon=FluentIcon.MARKET,
            title="不买经验等级",
            content="在选择的这些等级回合中不会自己购买经验",
        )
        box4.addWidget(self.upgradeLevelCard)

        # 设置卡 买经验刷新商店
        self.buyExpRefreshStoreCard = SwitchSettingCard(
            icon=FluentIcon.SYNC,
            title="刷新商店",
            content="在买经验的时候顺手刷新商店吗？",
            configItem=cfg.BUY_EXP_REFRESH_STORE
        )
        self.buyExpRefreshStoreCard.setValue = setValue.__get__(self.buyExpRefreshStoreCard)
        self.buyExpRefreshStoreCard.switchButton.setText(
            self.tr('启用') if cfg.BUY_EXP_REFRESH_STORE.value else self.tr('禁用'))
        box4.addWidget(self.buyExpRefreshStoreCard)

        self.mainLayout.addLayout(box4)




        # 5. 设置滚动区域内容
        scroll.setWidget(content_widget)

        # 6. 设置主窗口布局
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)


# 新开关按钮方法
def setValue(self, isChecked: bool):
    if self.configItem:
        qconfig.set(self.configItem, isChecked)

    self.switchButton.setChecked(isChecked)
    self.switchButton.setText(
        self.tr('启用') if isChecked else self.tr('禁用'))


