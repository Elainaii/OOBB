from math import copysign
from msilib.schema import ComboBox, CheckBox

from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup, QCursor,QAction
from PySide6.QtCore import Qt, QSortFilterProxyModel, QAbstractItemModel, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView, QSizePolicy, QTableView, QHeaderView, \
    QButtonGroup, QHBoxLayout, QFileDialog

from qfluentwidgets import (ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
                            SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont,
                            RoundMenu, \
                            TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget, MessageBoxBase,
                            SubtitleLabel, DatePicker,
                            ComboBox, CheckBox, RadioButton, InfoBar, InfoBarPosition)
from src.client.core.account import *


class AwardTableView(TableView):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)
        self.controller = controller
        # self.filter_menu = MyCourseFilterMenu('过滤',FluentIcon.FILTER,controller)
        # controller.set_my_course_filter(controller.account.curr_semester, 0, '')
        controller.init_award()
        self.data = controller.award_list
        print(self.data)
        self.model = QStandardItemModel()
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['award_name'])))
            self.model.setItem(i, 1, QStandardItem(row['award_content']))

        self.model.setHorizontalHeaderLabels(['奖励名', '奖励内容'])
        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        self.agentModel.setFilterKeyColumn(-1)


        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


class AwardCommandBar(CommandBar):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)

        self.controller = controller

        self.refresh = Action(FluentIcon.SYNC, "刷新", self)
        self.addAction(self.refresh)
        # self.addAction(Action(FluentIcon.COPY, "", self))
        self.share = Action(FluentIcon.SHARE, "导出", self)
        self.addAction(self.share)
        self.addSeparator()
        self.addAction(Action(FluentIcon.UP, "", self))
        self.addAction(Action(FluentIcon.DOWN, "", self))

        self.pageLabel1 = CaptionLabel()
        self.pageLabel1.setText("当前第")
        self.pageEdit = LineEdit()
        self.pageEdit.setFixedWidth(40)  # 连接时要设置宽度
        self.pageLabel2 = CaptionLabel()
        self.pageLabel2.setText("页,共??页")

        self.addWidget(self.pageLabel1)
        self.addWidget(self.pageEdit)
        self.addWidget(self.pageLabel2)
        self.addSeparator()

        # self.filterMenu = MyCourseFilterMenu('过滤',FluentIcon.FILTER,controller)
        # self.addWidget(self.filterMenu)

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)


class AwardInterface(ScrollArea):

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        self.commandBar = AwardCommandBar(controller, self.view)
        self.table = AwardTableView(controller, self)

        #self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("award_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)

        self.enableTransparentBackground()