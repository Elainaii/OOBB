from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup
from PySide6.QtCore import Qt, QSortFilterProxyModel,QAbstractItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView,QSizePolicy,QTableView,QHeaderView

from qfluentwidgets import ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
    SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont, RoundMenu, \
    TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget


class AwardInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        #self.commandBar = MyCousreCommandBar(self.view)
        #self.table = MyCourseTableView(self)

        #self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        #self.vBoxLayout.addWidget(self.commandBar, 0, Qt.AlignmentFlag.AlignTop)
        #self.vBoxLayout.addWidget(self.table, 0)
