from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup, QAction, QCursor
from PySide6.QtCore import Qt, QSortFilterProxyModel,QAbstractItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView,QSizePolicy,QTableView,QHeaderView

from qfluentwidgets import ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
    SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont, RoundMenu, \
    TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget

from src.client.core.account import Account, AdminController


class TeacherController():
    def __init__(self,account:Account):
        data = account.get_my_course()
        #TODO


class TeacherTableView(TableView):
    def __init__(self,parent = None):
        super().__init__(parent)
        from faker import Faker
        fake = Faker(locale='zh-CN')

        data = [[fake.name(), fake.address(), fake.ascii_free_email(), fake.phone_number()] for
                _ in range(50)]

        model = QStandardItemModel()
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                model.setItem(i, j, QStandardItem(item))
        model.setHorizontalHeaderLabels(['课程id','名称', '上课地址', '教师', '开始周数','结束周数','学分','成绩'])

        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(model)
        self.agentModel.setFilterKeyColumn(-1)


        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_rightmenu)

    def create_rightmenu(self,pos):
        menu = RoundMenu()
        #self.l.setCurrentIndex(Q)
        # 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标
        menu.addAction(Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功")))
        menu.addAction(Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功")))
        menu.addAction(Action(FluentIcon.EDIT,'修改密码',triggered= lambda :print("修改密码")))
        menu.addAction(Action(FluentIcon.LABEL,'修改信息',triggered = lambda :print("修改信息")))


        # 批量添加动作
        # 添加分割线
        # 子菜单

        #menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        menu.exec(QCursor.pos())


class TeacherFilterMenu(TransparentDropDownPushButton):
    def __init__(self,str,Icon):
        super().__init__()
        self.setText(str)
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

        menu.addMenu(self.submenu1)
        menu.addMenu(self.submenu2)
        self.setMenu(menu)





class TeacherCommandBar(CommandBar):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.addAction(Action(FluentIcon.SYNC, "", self))
        self.addAction(Action(FluentIcon.COPY, "", self))
        self.addAction(Action(FluentIcon.SHARE, "", self))
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

        self.filterMenu = TeacherFilterMenu('过滤',FluentIcon.FILTER)
        self.addWidget(self.filterMenu)

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)



class TeacherInterface(ScrollArea):

    def __init__(self,controller :AdminController, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        self.commandBar = TeacherCommandBar(self.view)
        self.table = TeacherTableView(self)

        self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar,0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)



        self.enableTransparentBackground()

