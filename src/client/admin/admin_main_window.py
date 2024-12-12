from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition, setThemeColor

from src.client.core.account import *
from src.client.admin.student_interface import StudentInterface
from src.client.admin.teacher_interface import TeacherInterface


class AdminMainWindow(MSFluentWindow):
    def __init__(self, account: Account = None, parent=None):
        super().__init__(parent)
        self.controller = AdminController(account)
        # add sub interfaces.
        self.studentInterface = StudentInterface( self.controller,self)
        self.studentInterface.setObjectName("studentInterface")
        self.teacherInterface = TeacherInterface( self.controller,self)
        self.teacherInterface.setObjectName("teacherInterface")


        self.addSubInterface(self.studentInterface, FluentIcon.PEOPLE, "学生", FluentIcon.PEOPLE, isTransparent=True)
        self.addSubInterface(self.teacherInterface, FluentIcon.PEOPLE, "教师", FluentIcon.PEOPLE, isTransparent=True)

        setThemeColor('#f18cb9', lazy=True)
        self.setFixedSize(960, 640)
        self.setWindowTitle('Admin')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.titleBar.raise_()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    account = Account()
    account.identity = 'A'
    account.account_id = '10001'
    app = QApplication([])
    window = AdminMainWindow(account)
    window.show()
    app.exec()
