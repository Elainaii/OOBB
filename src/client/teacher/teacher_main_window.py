from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget,QApplication
from PySide6.QtCore import Qt
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition,setThemeColor

from src.client.core.account import Account, TeacherController
from src.client.public.account_interface import AccountInterface
from src.client.teacher.my_course_interface import MyCourseInterface


class TeacherMainWindow(MSFluentWindow):
    def __init__(self,account:Account = None, parent=None):
        super().__init__(parent)

        self.account = account
        self.controller = TeacherController(account)
        self.accountInterface = AccountInterface(self)
        self.accountInterface.setObjectName("accountInterface")

        # add sub interfaces
        self.myCourseInterface = MyCourseInterface(self.controller)
        self.myCourseInterface.setObjectName("myCourseInterface")

        setThemeColor('#f18cb9', lazy=True)
        self.setFixedSize(960, 640)
        self.setWindowTitle('Teacher')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.addSubInterface(self.accountInterface, FluentIcon.PEOPLE, "账户", FluentIcon.PEOPLE, isTransparent=True, position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.myCourseInterface, FluentIcon.LIBRARY, "我的课程", FluentIcon.LIBRARY_FILL, isTransparent=True)
        self.titleBar.raise_()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    account = Account()
    account.id = '20240001'
    account.identity = 'T'

    app = QApplication([])
    window = TeacherMainWindow(account)

    window.show()
    app.exec()
