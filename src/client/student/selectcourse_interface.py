from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup
from PySide6.QtCore import Qt, QSortFilterProxyModel,QAbstractItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView,QSizePolicy,QTableView,QHeaderView

from qfluentwidgets import ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
    SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont, RoundMenu, \
    TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget

from src.client.core.account import *

class SelectCourseTableView(TableView):
    def __init__(self,controller:StudentController,parent = None):
        super().__init__(parent)
        self.controller = controller
        self.filter_menu = SelectCourseFilterMenu('过滤',FluentIcon.FILTER,controller)

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


        self.model.setHorizontalHeaderLabels(['课程号', '课程名', '上课地点', '教师', '开始周', '结束周', '学分', '上课时间'])
        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        self.agentModel.setFilterKeyColumn(-1)


        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

class SelectCourseFilterMenu(TransparentDropDownPushButton):
    def __init__(self,text,Icon, controller:StudentController):
        super().__init__()
        self.setText(text)
        self.setIcon(Icon)
        setFont(self, 12)
        menu = RoundMenu(parent=self)
        #开课单位，
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

        self.filterMenu = SelectCourseFilterMenu('过滤',FluentIcon.FILTER,controller)
        self.addWidget(self.filterMenu)

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

       # self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("selectCourseInterface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)
