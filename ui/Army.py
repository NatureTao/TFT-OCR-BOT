"""
阵容页面组件
"""

import json
import os
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QDir
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QGridLayout
from qfluentwidgets import FluentIcon, PrimaryPushButton, PushButton, InfoBar, InfoBarPosition, EditableComboBox, Dialog

# 导入组件
from HeroItem import HeroItem
from CustomFruitMessageBox import CustomFruitMessageBox
from CustomRuneMessageBox import CustomRuneMessageBox
from HomeConsole import HomeConsole
class Army(QFrame):
    def __init__(self, parent=None,rows=4,cols=7):
        super().__init__(parent=parent)

        self.setObjectName("阵容")
        self.basePath = Path(__file__).parent.parent / "squads"  # 阵容存储文件夹

        # 创建主垂直布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(10)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # 添加水平布局（在网格布局上方）
        self.header_layout = QHBoxLayout()
        self.selectItem = EditableComboBox() # 下拉框
        self.selectItem.setPlaceholderText("输入新名称或选择一个配置")
        self.selectItem.setMaxVisibleItems(10)
        # 加载下拉框可用配置
        self.selectItem.addItems(self.loadSquadsList())
        self.selectItem.setCurrentIndex(-1)  # -1 表示无选中项
        self.selectItem.currentIndexChanged.connect(self.onSelectChanged) # 监听事件


        self.saveBtn = PrimaryPushButton(FluentIcon.SAVE,'保存')
        self.saveBtn.clicked.connect(self.saveClicked)

        self.runeBtn = PushButton(QIcon("./icon/强化符文.png"),'编辑符文')
        self.runeBtn.setIconSize(QSize(20,20))
        self.runeBtn.clicked.connect(self.editRuneList)

        self.fruitBtn = PushButton(QIcon("./icon/fruit.png"),'编辑水果')
        self.fruitBtn.setIconSize(QSize(20,20))
        self.fruitBtn.clicked.connect(self.editFruitList)

        self.captureBtn = PushButton(FluentIcon.GLOBE,'抓取阵容')
        # self.captureBtn.clicked.connect()

        self.restBtn = PushButton(FluentIcon.ERASE_TOOL,'重置当前')
        self.restBtn.clicked.connect(self.restClicked)

        self.deleteBtn = PushButton(FluentIcon.DELETE,'删除配置')
        self.deleteBtn.clicked.connect(self.deleteClicked)

        self.header_layout.addWidget(self.selectItem)
        self.header_layout.addWidget(self.saveBtn)
        self.header_layout.addWidget(self.runeBtn)
        self.header_layout.addWidget(self.fruitBtn)
        self.header_layout.addWidget(self.captureBtn)
        self.header_layout.addWidget(self.restBtn)
        self.header_layout.addWidget(self.deleteBtn)
        mainLayout.addLayout(self.header_layout)  # 先添加水平布局

        # 创建网格布局
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(10)  # 设置项目之间的间距
        mainLayout.addLayout(self.grid_layout) # 再添加网格布局

        # 创建 HeroItem 实例并添加到网格中
        self.hero_items:list[HeroItem] = []
        for row in range(rows):
            for col in range(cols):
                hero_item = HeroItem(parent=self, index=(rows - 1 - row) * cols + col)
                self.grid_layout.addWidget(hero_item, row, col)
                self.hero_items.append(hero_item)

    def loadSquadsList(self):
        """加载配置文件"""
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)
            return []
        files = QDir(self.basePath).entryList(["*.json"], QDir.Filter.Files)
        return [os.path.splitext(f)[0] for f in files]  # 去掉.json后缀

    def onSelectChanged(self,index):
        if index >= 0:
            if os.path.exists(self.basePath):
                if os.path.isfile(existing_path := os.path.join(self.basePath, self.selectItem.currentText()+".json")):
                    try:
                        with open(existing_path, "r", encoding="utf-8") as f:
                            existingData = json.load(f)
                            # 读取文件
                        for hero in self.hero_items:
                            hero.resetData()
                        for item in existingData['COMP']:
                            for hero in self.hero_items:

                                if hero.index == existingData['COMP'][item]['board_position']:
                                    hero.isContent = True
                                    hero.heroName = item
                                    hero.iconLabel.setText(item)
                                    hero.items = existingData['COMP'][item]['items']
                                    hero.level = existingData['COMP'][item]['level']
                                    hero.final_comp = existingData['COMP'][item]['final_comp']
                                    hero.center = existingData['COMP'][item]['center']
                                    if hero.center:
                                        newStyle = f"""
                                            {hero._originalStyle}
                                            HeroItem {{
                                                background: qlineargradient(
                                                x1:0, y1:0,
                                                x2:0, y2:1,
                                                stop:0 #F38138,
                                                stop:1 white
                                            );
                                            border-radius: 6px;
                                            }}
                                       """
                                        hero.setStyleSheet(newStyle)
                        print(index)
                        #提示
                        InfoBar.success(
                            title='TFT-OCR-BOT',
                            content="已加载",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=3000,
                            parent=self
                        )

                    except Exception as e:
                        print(e)
                else:
                    print("未找到文件")
            else:
                print("未找到文件夹")




    def saveClicked(self):
        """ 保存阵容配置 先检查是否为更新文件操作,否则创建文件操作 """

        if len(self.selectItem.currentText().strip()) == 0:

            InfoBar.warning(
                title='TFT-OCR-BOT',
                content="请给当前的阵容设置一个名称!",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
        else:
            # COMP 整合
            COMP = {}
            for item in self.hero_items:
                if item.level != 0 and item.heroName != '未输入英雄名称' and item.heroName:
                    COMP[item.heroName] = item.toDict()

            if os.path.exists(self.basePath):
                # 更新
                if os.path.isfile(existing_path := os.path.join(self.basePath, self.selectItem.currentText()+".json")):
                    try:
                        with open(existing_path, "r", encoding="utf-8") as f:
                            existingData = json.load(f)
                            # 读取文件 替换数据
                            existingData["COMP"] = COMP
                            # 写回文件
                        with open(existing_path, "w", encoding="utf-8") as f:
                            json.dump(existingData, f, ensure_ascii=False, indent=4)

                        InfoBar.success(
                            title='TFT-OCR-BOT',
                            content=f"已更新到 {os.path.join(self.basePath, self.selectItem.currentText())}.json",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=5000,
                            parent=self
                        )
                    except Exception as e:
                        InfoBar.error(
                            title='错误',
                            content=f"{e}",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=5000,
                            parent=self
                        )
                # 新建
                else:

                    try:
                        # 默认数据结构
                        defaultData = {"COMP": COMP, "AUGMENTS": [],"AVOID_AUGMENTS": [],
                                       "FRUIT": [],"AVOID_FRUIT": []}
                        # 写入新文件
                        with open(existing_path, "w", encoding="utf-8") as f:
                            json.dump(defaultData, f, ensure_ascii=False, indent=4)

                        InfoBar.success(
                            title='TFT-OCR-BOT',
                            content=f"已保存到 {os.path.join(self.basePath, self.selectItem.currentText())}.json",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=5000,
                            parent=self
                        )
                        self.selectItem.blockSignals(True)  # 阻塞信号
                        self.selectItem.clear()
                        self.selectItem.addItems(self.loadSquadsList())
                        self.selectItem.setCurrentIndex(-1)
                        self.selectItem.blockSignals(False)  # 阻塞信号
                    except Exception as e:
                        InfoBar.error(
                            title='错误',
                            content=f"{e}",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=5000,
                            parent=self
                        )

    def restClicked(self):
        hint = False
        for item in self.hero_items:
            if item.isContent:
                hint = True
                break
        for item in self.hero_items:
            if item.isContent:
                item.resetData()
        if hint:
            InfoBar.new(
                icon=FluentIcon.ERASE_TOOL,
                title='TFT-OCR-BOT',
                content="已重置",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=3000,
                parent=self.parent()
            ).setCustomBackgroundColor('#CCCCCC', '#202020')

    def deleteClicked(self):
        if os.path.exists(self.basePath):
            if os.path.isfile(existing_path := os.path.join(self.basePath, (self.selectItem.currentText() + ".json"))):
                try:
                    deleteWindow = Dialog("删除提示", f"真的要删除{self.selectItem.currentText()}吗？", self.parent())
                    deleteWindow.yesButton.setText("确定")
                    deleteWindow.cancelButton.setText("取消")
                    if deleteWindow.exec():
                        os.remove(existing_path)
                        self.selectItem.blockSignals(True)  # 阻塞信号
                        self.selectItem.clear()
                        self.selectItem.setText('')
                        self.selectItem.addItems(self.loadSquadsList())
                        self.selectItem.setCurrentIndex(-1)
                        self.selectItem.blockSignals(False)  # 阻塞信号
                        InfoBar.success(
                            title='TFT-OCR-BOT',
                            content="删除成功",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=5000,
                            parent=self
                        )

                except Exception as e:
                    InfoBar.error(
                        title='错误',
                        content=f"{e}",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=False,
                        position=InfoBarPosition.BOTTOM,
                        duration=5000,
                        parent=self
                    )
                finally:
                    pass
            else:
                print("不存在")

    def editRuneList(self):
        """设置强化符文名单"""
        w = CustomRuneMessageBox(self)
        w.yesButton.setText("保存")
        w.cancelButton.setText("取消")

        if len(self.selectItem.currentText().strip()) == 0:

            InfoBar.warning(
                title='TFT-OCR-BOT',
                content="请给当前的阵容设置一个名称!",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
        else:
            # 判断是否存在目标文件
            if os.path.exists(self.basePath):
                if os.path.isfile(existing_path := os.path.join(self.basePath, self.selectItem.currentText() + ".json")):
                    # 保存符文信息
                    if w.exec():
                        try:
                            with open(existing_path, "r", encoding="utf-8") as f:
                                existingData = json.load(f)
                                # 读取文件 替换数据
                                existingData["AUGMENTS"] = w.runeTransfer.get_selected_data()
                                existingData["AVOID_AUGMENTS"] = w.avoidRuneTransfer.get_selected_data()

                            with open(existing_path, "w", encoding="utf-8") as f:
                                json.dump(existingData, f, ensure_ascii=False, indent=4)

                            InfoBar.success(
                                title='TFT-OCR-BOT',
                                content=f"已更新到 {os.path.join(self.basePath, self.selectItem.currentText())}.json",
                                orient=Qt.Orientation.Horizontal,
                                isClosable=False,
                                position=InfoBarPosition.BOTTOM,
                                duration=5000,
                                parent=self
                            )

                        except Exception as e:
                          print(e)

                else:
                    InfoBar.warning(
                        title='TFT-OCR-BOT',
                        content="请先保存阵容后在编辑符文",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=False,
                        position=InfoBarPosition.BOTTOM,
                        duration=5000,
                        parent=self
                    )

    def editFruitList(self):
        """设置强化果实名单"""
        w = CustomFruitMessageBox(self.parent())
        w.yesButton.setText("保存")
        w.cancelButton.setText("取消")

        if len(self.selectItem.currentText().strip()) == 0:
            InfoBar.warning(
                title='TFT-OCR-BOT',
                content="请给当前的阵容设置一个名称!",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
        else:
            # 判断是否存在目标文件
            if os.path.exists(self.basePath):
                if os.path.isfile(
                        existing_path := os.path.join(self.basePath, self.selectItem.currentText() + ".json")):
                    # 保存符文信息
                    if w.exec():
                        try:
                            with open(existing_path, "r", encoding="utf-8") as f:
                                existingData = json.load(f)
                                # 读取文件 替换数据
                                existingData["FRUIT"] = w.fruitTransfer.get_selected_data()
                                existingData["AVOID_FRUIT"] = w.avoidFruitTransfer.get_selected_data()

                            with open(existing_path, "w", encoding="utf-8") as f:
                                json.dump(existingData, f, ensure_ascii=False, indent=4)

                            InfoBar.success(
                                title='TFT-OCR-BOT',
                                content=f"已更新到 {os.path.join(self.basePath, self.selectItem.currentText())}.json",
                                orient=Qt.Orientation.Horizontal,
                                isClosable=False,
                                position=InfoBarPosition.BOTTOM,
                                duration=5000,
                                parent=self
                            )

                        except Exception as e:
                            print(e)

                else:
                    InfoBar.warning(
                        title='TFT-OCR-BOT',
                        content="请先保存阵容后在编辑水果",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=False,
                        position=InfoBarPosition.BOTTOM,
                        duration=5000,
                        parent=self
                    )
