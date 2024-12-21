import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget,QApplication
from PySide6.QtCore import Qt
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition,setThemeColor

from src.client.core.account import Account, TeacherController
from src.client.public.account_interface import AccountInterface
from src.client.teacher.my_course_interface import MyCourseInterface
from src.client.teacher.add_course_interface import AddCourseInterface
from src.client.public.ai_interface import AiInterface
from src.client.teacher.home_interface import HomeInterface


class TeacherMainWindow(MSFluentWindow):
    def __init__(self,account:Account = None, parent=None):
        super().__init__(parent)

        self.account = account
        self.controller = TeacherController(account)
        self.accountInterface = AccountInterface(self.controller, self)
        self.accountInterface.setObjectName("accountInterface")

        self.aiInterface = AiInterface(account,self)
        self.aiInterface.setObjectName("aiInterface")

        # add sub interfaces
        self.homeInterface = HomeInterface(self.controller)
        self.homeInterface.setObjectName("homeInterface")
        self.myCourseInterface = MyCourseInterface(self.controller)
        self.myCourseInterface.setObjectName("myCourseInterface")
        self.addCourseInterface = AddCourseInterface(self.controller)
        self.addCourseInterface.setObjectName("addCourseInterface")




        setThemeColor('#f18cb9', lazy=True)
        self.setFixedSize(960, 640)
        self.setWindowTitle('Teacher')

        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo = script_dir + '/resource/images/logo2.png'
        self.setWindowIcon(QIcon(logo))

        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "主页", FluentIcon.HOME_FILL, isTransparent=True)
        self.addSubInterface(self.myCourseInterface, FluentIcon.LIBRARY, "我的课程", FluentIcon.LIBRARY_FILL, isTransparent=True)
        self.addSubInterface(self.addCourseInterface, FluentIcon.ADD, "添加课程", FluentIcon.ADD_TO, isTransparent=True)
        self.addSubInterface(self.aiInterface, FluentIcon.ROBOT, "智能助手", FluentIcon.ROBOT, isTransparent=True, position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.accountInterface, FluentIcon.PEOPLE, "账户", FluentIcon.PEOPLE, isTransparent=True, position=NavigationItemPosition.BOTTOM)
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
