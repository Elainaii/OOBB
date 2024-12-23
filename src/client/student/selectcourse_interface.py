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
from src.create_data import course_names


class SelectCourseMessageBox(MessageBoxBase):
    def __init__(self,controller:StudentController,parent=None,course_name = '', sec_id = ''):
        super().__init__(parent)
        self.controller = controller
        self.titleLabel = SubtitleLabel('确认选择课程')

        self.course_nameLabel = CaptionLabel(f"课程名: {course_name}")
        self.section_idLabel = CaptionLabel(f"开课号: {sec_id}")
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.course_nameLabel)
        self.viewLayout.addWidget(self.section_idLabel)

        self.widget.setMinimumWidth(350)

class SelectCourseTableView(TableView):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)
        self.controller = controller
        # self.filter_menu = SelectCourseFilterMenu('过滤',FluentIcon.FILTER,controller)

        controller.init_select_course()
        self.data = controller.select_course_list
        print(self.data)
        self.model = QStandardItemModel()
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['course_id'])))
            self.model.setItem(i, 1, QStandardItem(row['course_name']))
            self.model.setItem(i, 2, QStandardItem(row['building_name'] +" "+ str(row['room_number'])))
            self.model.setItem(i, 3, QStandardItem(row['teacher_name']))
            self.model.setItem(i, 4, QStandardItem(str(row['start_week'])))
            self.model.setItem(i, 5, QStandardItem(str(row['end_week'])))
            self.model.setItem(i, 6, QStandardItem(str(row['course_credit'])))
            self.model.setItem(i, 7, QStandardItem(str('周' + str(row['course_day']) +' '+ str(row['course_start_time']) + "-" + str(row['course_end_time']))))
            self.model.setItem(i, 8, QStandardItem(str(row['rest_number'])))


        self.model.setHorizontalHeaderLabels(['课程号', '课程名', '上课地点', '教师', '开始周', '结束周', '学分', '上课时间', '剩余名额'])
        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        self.agentModel.setFilterKeyColumn(-1)


        self.menu = None
        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setSortingEnabled(False)
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
            self.selectAction = Action(FluentIcon.ACCEPT, '选课', triggered=self.select_course)
            self.menu.addAction(self.selectAction)
            # 批量添加动作
            # 添加分割线
            # 子菜单

            # menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        self.menu.exec(QCursor.pos())

    def select_course(self):
        # 获取选中的课程名字
        course_name = self.data[self.currentIndex().row()]['course_name']
        # 获取选中的开课号
        sec_id = self.data[self.currentIndex().row()]['sec_id']
        self.select_course_message_box = SelectCourseMessageBox(self.controller, self.parent(), course_name, sec_id)
        if self.select_course_message_box.exec() == 1:
            data = {
                'sec_id': sec_id
            }
            status, msg = self.controller.select_course(data)
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
            # 刷新
            self.controller.init_select_course()
            self.reset()

    def reset(self):
        self.data = self.controller.select_course_list
        self.model.removeRows(0, self.model.rowCount())
        self.model.setHorizontalHeaderLabels(['课程号', '课程名', '上课地点', '教师', '开始周', '结束周', '学分', '上课时间'])
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['course_id'])))
            self.model.setItem(i, 1, QStandardItem(row['course_name']))
            self.model.setItem(i, 2, QStandardItem(row['building_name'] +" "+ str(row['room_number'])))
            self.model.setItem(i, 3, QStandardItem(row['teacher_name']))
            self.model.setItem(i, 4, QStandardItem(str(row['start_week'])))
            self.model.setItem(i, 5, QStandardItem(str(row['end_week'])))
            self.model.setItem(i, 6, QStandardItem(str(row['course_credit'])))
            self.model.setItem(i, 7, QStandardItem(str('周' + str(row['course_day']) +' '+ str(row['course_start_time']) + "-" + str(row['course_end_time']))))
            self.model.setItem(i, 8, QStandardItem(str(row['rest_number'])))
        self.resizeColumnsToContents()


class SelectCourseCommandBar(CommandBar):
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

        #self.filterMenu = SelectCourseFilterMenu('过滤',FluentIcon.FILTER,controller)
        #self.addWidget(self.filterMenu)

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)

class SelectCourseInterface(ScrollArea):

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.controller = controller
        self.commandBar = SelectCourseCommandBar(self.controller, self.view)
        self.table = SelectCourseTableView(self.controller, self.view)
        self.commandBar.refresh.triggered.connect(self.refresh)
       # self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("selectCourseInterface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)
        self.enableTransparentBackground()

    def refresh(self):
        self.controller.init_select_course()
        self.table.reset()