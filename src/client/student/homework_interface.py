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

class SubmitHomeworkMessageBox(MessageBoxBase):
    def __init__(self,controller:StudentController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.titleLabel = SubtitleLabel('提交作业')
        self.homework_nameEdit = LineEdit()
        self.homework_contentEdit = LineEdit()

        self.homework_nameEdit.setPlaceholderText("作业名")
        self.homework_contentEdit.setPlaceholderText("作业内容")

        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addWidget(self.homework_nameEdit)
        self.viewLayout.addWidget(self.homework_contentEdit)
        self.widget.setMinimumWidth(350)

class HomeworkTableView(TableView):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)
        self.controller = controller
       #  self.filter_menu = HomeworkFilterMenu('过滤',FluentIcon.FILTER,controller)
       # print(self.filter_menu.get_status())
        controller.init_homework()
        self.data = controller.homework_list
        print(self.data)
        self.model = QStandardItemModel()
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['course_id'])))
            self.model.setItem(i, 1, QStandardItem(row['course_name']))
            self.model.setItem(i, 2, QStandardItem(row['homework_name']))
            self.model.setItem(i, 3, QStandardItem(row['homework_content']))
            self.model.setItem(i, 4, QStandardItem(str(row['homework_deadline'])))

        self.model.setHorizontalHeaderLabels(['课程号', '课程名', '作业', '作业内容', '截止时间'])
        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        self.agentModel.setFilterKeyColumn(-1)

        self.menu = None
        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_rightmenu)

    def show_rightmenu(self, pos):
        index = self.indexAt(pos)  # 返回点击的index
        if index.isValid():  # 如果有index,则弹出菜单,并且高光选中的行
            self.setCurrentIndex(index)
            self.menu = RoundMenu()
            # self.l.setCurrentIndex(Q)
            # 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标
            # self.copyAction = Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功"))
            # self.deleteAction = Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功"))
            self.homeworkAction = Action(FluentIcon.EDIT, '提交作业', triggered=self.submit_homework)

            self.menu.addAction(self.homeworkAction)
            # 批量添加动作
            # 添加分割线
            # 子菜单

            # menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        self.menu.exec(QCursor.pos())

    def submit_homework(self):
        self.submit_homework_message_box = SubmitHomeworkMessageBox(self.controller, self.parent())
        self.submit_homework_message_box.homework_nameEdit.setText(self.data[self.currentIndex().row()]['homework_name'])

        while self.submit_homework_message_box.exec() == 1:
            homework_name = self.submit_homework_message_box.homework_nameEdit.text()
            homework_content = self.submit_homework_message_box.homework_contentEdit.text()
            if homework_name == '' or homework_content == '':
                InfoBar.error(
                    title='错误',
                    content="请填写完整内容",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
            else:
                data = {
                    'sec_id': self.data[self.currentIndex().row()]['sec_id'],
                    'homework_name': homework_name,
                    'homework_content': homework_content
                }
                print(data)
                status, msg = self.controller.submit_homework(data)
                if status:
                    InfoBar.success(
                        title='成功',
                        content=msg,
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self.parent()
                    )
                else:
                    InfoBar.error(
                        title='错误',
                        content=msg,
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self.parent()
                    )


class HomeworkCommandBar(CommandBar):
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

        #self.filterMenu = HomeworkFilterMenu('过滤',FluentIcon.FILTER,controller)
        #self.addWidget(self.filterMenu)

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)



class HomeworkInterface(ScrollArea):

    def __init__(self,controller ,parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.controller = controller

        self.vBoxLayout = QVBoxLayout(self.view)

        self.commandBar = HomeworkCommandBar(self.controller,self.view)
        self.table = HomeworkTableView(self.controller,self)
        '''
        self.commandBar.refresh.triggered.connect(self.refresh)
        self.commandBar.share.triggered.connect(self.share)
        # 筛选完毕后直接刷新
        self.commandBar.filterMenu.action1.triggered.connect(self.refresh)
        self.commandBar.filterMenu.action2.triggered.connect(self.refresh)
        self.commandBar.filterMenu.action3.triggered.connect(self.refresh)
        self.commandBar.filterMenu.action4.triggered.connect(self.refresh)
        # 筛选学期后直接刷新
        for action in self.commandBar.filterMenu.actionList:
            action.triggered.connect(self.refresh)
'''
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("homework_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar,0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)
        self.enableTransparentBackground()
'''
    def refresh(self):
        print(self.commandBar.filterMenu.get_semester(self.controller.account.curr_semester))
        self.controller.set_my_course_filter(self.commandBar.filterMenu.get_semester(self.controller.account.curr_semester), self.commandBar.filterMenu.get_status(), '')
        self.controller.init_course_list()
        self.table.reset()

    def share(self):
        pass

'''