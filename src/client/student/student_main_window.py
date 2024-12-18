from qfluentwidgets import setThemeColor

from src.client.student.award_interface import AwardInterface
from src.client.student.home_interface import *
from src.client.public.account_interface import AccountInterface
from src.client.student.homework_interface import HomeworkInterface
from src.client.student.mycourse_interface import *
from src.client.student.selectcourse_interface import *


class StudentMainWindow(MSFluentWindow):
    def __init__(self,account:Account = None, parent=None):
        super().__init__(parent)
        self.account = account
        self.controller = StudentController(account)
        self.myCourseInterface = MyCourseInterface(controller=self.controller,parent=self)
        self.myCourseInterface.setObjectName("myCourseInterface")
        self.selectCourseInterface = SelectCourseInterface(controller=self.controller, parent=self)
        self.selectCourseInterface.setObjectName("selectCourseInterface")
        self.homeInterface = HomeInterface(controller=self.controller, parent=self)
        self.homeInterface.setObjectName("homeInterface")
        self.awardInterface = AwardInterface(controller=self.controller, parent=self)
        self.awardInterface.setObjectName("awardInterface")
        self.accountInterface = AccountInterface(account.id, self)
        self.accountInterface.setObjectName("accountInterface")
        self.homeworkInterface = HomeworkInterface(controller=self.controller, parent=self)
        self.homeworkInterface.setObjectName("homeworkInterface")



        # add sub interfaces
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "首页", FluentIcon.HOME_FILL, isTransparent=True)
        self.addSubInterface(self.myCourseInterface, FluentIcon.LIBRARY, "我的课程", FluentIcon.LIBRARY_FILL, isTransparent=True)
        self.addSubInterface(self.selectCourseInterface, FluentIcon.ADD, "选课", FluentIcon.ADD_TO, isTransparent=True)
        self.addSubInterface(self.awardInterface, FluentIcon.FLAG, "奖励", FluentIcon.FLAG, isTransparent=True)
        self.addSubInterface(self.homeworkInterface, FluentIcon.DATE_TIME, "作业", FluentIcon.DATE_TIME, isTransparent=True)
        self.addSubInterface(self.accountInterface, FluentIcon.PEOPLE, "账户", FluentIcon.PEOPLE, isTransparent=True, position=NavigationItemPosition.BOTTOM)
        #self.navigationInterface.addItem("editInterface", FluentIcon.EDIT, "编辑", selectable=False)

        setThemeColor('#f18cb9', lazy=True)
        self.setFixedSize(960, 640)
        self.setWindowTitle('Student')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.titleBar.raise_()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    account = Account()
    account.identity = 'S'
    app = QApplication([])
    window = StudentMainWindow(account)
    window.show()
    app.exec()