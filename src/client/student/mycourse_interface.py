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
import pandas as pd



class MyCourseTableView(TableView):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)
        self.controller = controller
        self.filter_menu = MyCourseFilterMenu('过滤',FluentIcon.FILTER,controller)
        print(self.filter_menu.get_status())
        controller.set_my_course_filter(controller.account.curr_semester, 0, '')
        controller.init_course_list()
        self.data = controller.course_list

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
            self.model.setItem(i, 8, QStandardItem(str(row['score'])))


        self.model.setHorizontalHeaderLabels(['课程号', '课程名', '上课地点', '教师', '开始周', '结束周', '学分', '上课时间', '成绩'])
        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        self.agentModel.setFilterKeyColumn(-1)


        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def reset(self):
        self.data = self.controller.course_list
        print(self.data)
        self.model.removeRows(0, self.model.rowCount())
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['course_id'])))
            self.model.setItem(i, 1, QStandardItem(row['course_name']))
            self.model.setItem(i, 2, QStandardItem(row['building_name'] +" "+ str(row['room_number'])))
            self.model.setItem(i, 3, QStandardItem(row['teacher_name']))
            self.model.setItem(i, 4, QStandardItem(str(row['start_week'])))
            self.model.setItem(i, 5, QStandardItem(str(row['end_week'])))
            self.model.setItem(i, 6, QStandardItem(str(row['course_credit'])))
            self.model.setItem(i, 7, QStandardItem(str('周' + str(row['course_day']) +' '+ str(row['course_start_time']) + "-" + str(row['course_end_time']))))
            self.model.setItem(i, 8, QStandardItem(str(row['score'])))
        self.agentModel.setSourceModel(self.model)

class MyCourseFilterMenu(TransparentDropDownPushButton):
    def __init__(self,text,Icon,controller:StudentController):
        super().__init__()
        self.setText(text)
        self.setIcon(Icon)
        setFont(self, 12)
        menu = RoundMenu(parent=self)
        # 过滤菜单，学期，仅显示挂科课程，显示已完成课程，显示未完成课程等
        self.submenu1 = CheckableMenu('课程状态', indicatorType=MenuIndicatorType.RADIO)

        self.action1 = Action(FluentIcon.ACCEPT, "已通过课程", checkable=True)
        self.action2 = Action(FluentIcon.CLOSE, "未通过课程", checkable=True)
        self.action3 = Action(FluentIcon.ALIGNMENT, "全部课程", checkable=True)
        self.action3.setChecked(True)
        self.action4 = Action(FluentIcon.REMOVE, "正在进行课程", checkable=True)
        self.actiongroup1 = QActionGroup(self.submenu1)
        self.actiongroup1.addAction(self.action1)
        self.actiongroup1.addAction(self.action2)
        self.actiongroup1.addAction(self.action3)
        self.actiongroup1.addAction(self.action4)
        self.submenu1.addActions([self.action1, self.action2, self.action3, self.action4])
        self.submenu1.setIcon(FluentIcon.CALENDAR)

        # 这里请求学期列表，
        self.submenu2 = CheckableMenu('学期', indicatorType=MenuIndicatorType.RADIO)
        self.actionList = []
        self.actiongroup2 = QActionGroup(self.submenu2)
        # 只显示20个学期
        for i,semester in enumerate(controller.account.semester_list):
            self.actionList.append(Action(FluentIcon.CALENDAR, str(semester['year']) + str(semester['season']),checkable=True))
            self.submenu2.addAction(self.actionList[i])
            self.actiongroup2.addAction(self.actionList[i])
            if(i == 19):
                break
        self.actionList[0].setChecked(True)

        menu.addMenu(self.submenu1)
        menu.addMenu(self.submenu2)
        self.setMenu(menu)


    def get_status(self):
        if self.action1.isChecked():
            return '2'
        elif self.action2.isChecked():
            return '3'
        elif self.action3.isChecked():
            return '0'
        elif self.action4.isChecked():
            return '1'

    def get_semester(self, num):
        for i, action in enumerate(self.actionList):
            if action.isChecked():
                # 因为这是倒序的，所以要取反
                return num - i


class MyCousreCommandBar(CommandBar):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)

        self.controller = controller

        self.refresh = Action(FluentIcon.SYNC, "刷新", self)
        self.addAction(self.refresh)
        # self.addAction(Action(FluentIcon.COPY, "", self))
        self.share = Action(FluentIcon.SHARE, "导出", self)
        self.addAction(self.share)
        self.addSeparator()
        self.up = Action(FluentIcon.UP, "")
        self.down = Action(FluentIcon.DOWN, "")
        self.addAction(self.up)
        self.addAction(self.down)

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

        self.filterMenu = MyCourseFilterMenu('过滤',FluentIcon.FILTER,controller)
        self.addWidget(self.filterMenu)

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)



class MyCourseInterface(ScrollArea):

    def __init__(self,controller ,parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.controller = controller

        self.vBoxLayout = QVBoxLayout(self.view)

        self.commandBar = MyCousreCommandBar(self.controller,self.view)
        self.table = MyCourseTableView(self.controller,self)
        self.commandBar.up.triggered.connect(self.prev_page)
        self.commandBar.down.triggered.connect(self.next_page)
        self.commandBar.refresh.triggered.connect(self.refresh)
        self.commandBar.share.triggered.connect(self.share)
        self.commandBar.pageEdit.textEdited.connect(self.change_page)
        self.commandBar.pageLabel2.setText("页,共" + str(self.controller.course_total_page) + "页")
        # 筛选完毕后直接刷新
        self.commandBar.filterMenu.action1.triggered.connect(self.refresh)
        self.commandBar.filterMenu.action2.triggered.connect(self.refresh)
        self.commandBar.filterMenu.action3.triggered.connect(self.refresh)
        self.commandBar.filterMenu.action4.triggered.connect(self.refresh)
        # 筛选学期后直接刷新
        for action in self.commandBar.filterMenu.actionList:
            action.triggered.connect(self.refresh)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar,0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)
        self.enableTransparentBackground()

    def prev_page(self):
        status, msg = self.controller.mycourse_prev_page()
        if status:
            self.table.reset()
            self.commandBar.pageEdit.setText(str(self.controller.course_curr_page))
        else:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
        return

    def next_page(self):
        status, msg = self.controller.mycourse_next_page()
        if status:
            self.table.reset()
            self.commandBar.pageEdit.setText(str(self.controller.course_curr_page))
        else:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
        return

    def refresh(self):
        print(self.commandBar.filterMenu.get_semester(self.controller.account.curr_semester))
        print(self.commandBar.filterMenu.get_status())
        self.controller.set_my_course_filter(self.commandBar.filterMenu.get_semester(self.controller.account.curr_semester), self.commandBar.filterMenu.get_status(), '')
        self.controller.init_course_list()
        self.table.reset()
        return

    def share(self):
        # 先获取数据
        a, b, data = self.controller.get_all_my_course_list()
        df = pd.DataFrame(data)
        # 选择保存路径
        path = QFileDialog.getSaveFileName(self, '保存文件', '', 'Excel files (*.xlsx)')
        if path[0] == '':
            return
        df.to_excel(path[0], index=False)
        InfoBar.success(
            title='成功',
            content='导出成功',
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )
        return

    def change_page(self):
        if self.commandBar.pageEdit.text() == '':
            return
        page_number = int(self.commandBar.pageEdit.text())
        if page_number<0 or page_number>self.controller.course_total_page-1:
            InfoBar.error(
                title='错误',
                content="页数超出范围",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
            return
        self.controller.course_curr_page = page_number
        self.controller.init_course_list()
        self.table.reset()
        return