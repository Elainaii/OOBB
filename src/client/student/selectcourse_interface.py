from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup
from PySide6.QtCore import Qt, QSortFilterProxyModel,QAbstractItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView,QSizePolicy,QTableView,QHeaderView

from qfluentwidgets import ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
    SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont, RoundMenu, \
    TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget



class SelectCourseFilterMenu(TransparentDropDownPushButton):
    def __init__(self,str,Icon):
        super().__init__()
        self.setText(str)
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

        menu.addMenu(self.submenu1)
        menu.addMenu(self.submenu2)
        self.setMenu(menu)

class SelectCourseInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        #self.commandBar = MyCousreCommandBar(self.view)
        #self.table = MyCourseTableView(self)

       # self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        #self.vBoxLayout.addWidget(self.commandBar, 0, Qt.AlignmentFlag.AlignTop)
        #self.vBoxLayout.addWidget(self.table, 0)
