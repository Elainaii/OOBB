from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup
from PySide6.QtCore import Qt, QSortFilterProxyModel,QAbstractItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView

from qfluentwidgets import ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
    SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont, RoundMenu, \
    TogglePushButton, CheckableMenu, MenuIndicatorType

from src.client.core.account import Account

class MyCourseInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        self.commandBar = CommandBar(self.view)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        #self.commandBar.addAction(Action(FluentIcon.ADD, "添加课程", self.commandBar))
        #self.commandBar.addSeparator()
        self.commandBar.addAction(Action(FluentIcon.SYNC, "", self.commandBar))
        self.commandBar.addAction(Action(FluentIcon.COPY, "", self.commandBar))
        self.commandBar.addAction(Action(FluentIcon.SHARE, "", self.commandBar))
        self.commandBar.addSeparator()
        self.commandBar.addAction(Action(FluentIcon.UP, "", self.commandBar))
        self.commandBar.addAction(Action(FluentIcon.DOWN, "", self.commandBar))

        self.pageLabel1 = CaptionLabel()
        self.pageLabel1.setText("当前第")
        self.pageEdit = LineEdit()
        self.pageEdit.setFixedWidth(40)#连接时要设置宽度
        self.pageLabel2 = CaptionLabel()
        self.pageLabel2.setText("页,共??页")

        self.commandBar.addWidget(self.pageLabel1)
        self.commandBar.addWidget(self.pageEdit)
        self.commandBar.addWidget(self.pageLabel2)
        self.commandBar.addSeparator()

        self.filterMenu = self.create_filter_menu()
        self.commandBar.addWidget(self.filterMenu)


        #self.commandBar.addSeparator()
        self.search = SearchLineEdit(self.commandBar)
        self.search.setPlaceholderText("搜索")
        self.commandBar.addWidget(self.search)


        from faker import Faker
        self.fake = Faker(locale='zh-CN')

        self.data = [[self.fake.name(), self.fake.address(), self.fake.ascii_free_email(), self.fake.phone_number()] for
                     _ in range(50)]

        self.model = QStandardItemModel()
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                self.model.setItem(i, j, QStandardItem(item))
        self.model.setHorizontalHeaderLabels(['姓名', '地址', 'Email', '电话'])

        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        self.agentModel.setFilterKeyColumn(-1)

        self.table = TableView(self)
        self.table.setModel(self.agentModel)

        # self.table.setHorizontalHeader()
        self.table.verticalHeader().hide()
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.search.textEdited.connect(lambda str1: self.agentModel.setFilterRegularExpression(str1))





        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar,0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)
        #self.vBoxLayout.addWidget(self.appCard, 0, Qt.AlignTop)


        self.enableTransparentBackground()

    def create_filter_menu(self):
        button = TransparentDropDownPushButton('过滤', self, FluentIcon.MENU)
        #button.setFixedHeight(34)
        setFont(button, 12)
        menu = RoundMenu(parent=self)
        #过滤菜单，学期，仅显示挂科课程，显示已完成课程，显示未完成课程等
        submenu1 = CheckableMenu('课程状态',indicatorType=MenuIndicatorType.RADIO)

        self.action1 = Action(FluentIcon.ACCEPT, "已通过课程", checkable=True)
        self.action2 = Action(FluentIcon.CLOSE, "未通过课程", checkable=True)
        self.action3 = Action(FluentIcon.ALIGNMENT, "全部课程", checkable=True)
        self.action3.setChecked(True)
        self.action4 = Action(FluentIcon.REMOVE, "正在进行课程", checkable=True)
        self.actiongroup1 = QActionGroup(submenu1)
        self.actiongroup1.addAction(self.action1)
        self.actiongroup1.addAction(self.action2)
        self.actiongroup1.addAction(self.action3)
        self.actiongroup1.addAction(self.action4)
        submenu1.addActions([self.action1, self.action2, self.action3, self.action4])
        submenu1.setIcon(FluentIcon.CALENDAR)

        #这里请求学期列表，
        submenu2 = CheckableMenu('学期', indicatorType=MenuIndicatorType.RADIO)





        menu.addMenu(submenu1)
        menu.addMenu(submenu2)
        button.setMenu(menu)
        return button


class StudentMainWindow(MSFluentWindow):
    def __init__(self,account:Account = None, parent=None):
        super().__init__(parent)

        self.myCourseInterface = MyCourseInterface(self)

        # add sub interfaces
        self.addSubInterface(self.myCourseInterface, FluentIcon.LIBRARY, "我的课程", FluentIcon.LIBRARY_FILL, isTransparent=True)
        #self.navigationInterface.addItem("editInterface", FluentIcon.EDIT, "编辑", selectable=False)

        self.navigationInterface.addItem(
            "settingInterface", FluentIcon.SETTING, "设置", position=NavigationItemPosition.BOTTOM, selectable=False)

        self.resize(880, 760)
        self.setWindowTitle('Student')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.titleBar.raise_()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    window = StudentMainWindow()
    window.show()
    app.exec()