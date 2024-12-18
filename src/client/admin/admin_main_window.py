from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition, setThemeColor

from src.client.core.account import *
from src.client.admin.student_interface import StudentInterface
from src.client.admin.teacher_interface import TeacherInterface
from src.client.admin.admin_interface import AdminInterface
from src.client.public.account_interface import AccountInterface
from src.client.admin.others_interface import OthersInterface
from src.client.public.ai_interface import *

class AdminMainWindow(MSFluentWindow):
    def __init__(self, account: Account = None, parent=None):
        super().__init__(parent)
        self.controller = AdminController(account)
        # add sub interfaces.
        self.studentInterface = StudentInterface( self.controller,self)
        self.studentInterface.setObjectName("studentInterface")
        self.teacherInterface = TeacherInterface( self.controller,self)
        self.teacherInterface.setObjectName("teacherInterface")
        self.adminInterface = AdminInterface( self.controller,self)
        self.adminInterface.setObjectName("adminInterface")
        self.accountInterface = AccountInterface(self.controller, self)
        self.accountInterface.setObjectName("accountInterface")
        self.otherInterface = OthersInterface(self.controller,self)
        self.otherInterface.setObjectName("otherInterface")
        self.AI = AiInterface(account.id, self)
        self.AI.setObjectName("AI")

        self.addSubInterface(self.studentInterface, FluentIcon.PEOPLE, "学生", FluentIcon.PEOPLE, isTransparent=True)
        self.addSubInterface(self.teacherInterface, FluentIcon.PEOPLE, "教师", FluentIcon.PEOPLE, isTransparent=True)
        self.addSubInterface(self.adminInterface, FluentIcon.PEOPLE, "管理员", FluentIcon.PEOPLE, isTransparent=True)
        self.addSubInterface(self.AI, FluentIcon.ROBOT, "AI", FluentIcon.ROBOT, isTransparent=True, position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.accountInterface, FluentIcon.PEOPLE, "账户", FluentIcon.PEOPLE, isTransparent=True, position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.otherInterface, FluentIcon.PEOPLE, "其他", FluentIcon.PEOPLE, isTransparent=True)

        setThemeColor('#f18cb9', lazy=True)
        self.setFixedSize(960, 640)
        self.setWindowTitle('Admin')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.titleBar.raise_()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    account = Account()
    account.identity = 'A'
    # 管理员的ID和姓名从对应的地方获取
    app = QApplication([])
    window = AdminMainWindow(account)
    window.show()
    app.exec()
