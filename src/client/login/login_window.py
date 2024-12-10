import sys

from PySide6.QtCore import Qt, QTranslator, QLocale, QRect
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, isDarkTheme, \
    InfoBarPosition, InfoBar
from src.client.login.ui_LoginWindow import Ui_Form
from src.client.student.student_main_window import *

from src.client.core.account import *


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


def show_main_window(account: Account, mainWindow=None):
    if account.identity == 'A':
        print("Admin")  # 这里之后改成展示界面
    elif account.identity == 'T':
        print("Teacher")
    else:
        mainWindow = StudentMainWindow(account)
        mainWindow.show()
        print("Student")


class LoginWindow(Window, Ui_Form):
    account: Account
    def __init__(self,account_:Account,mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('Student Management System-login')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
        if not isWin11():
            color = QColor(25, 33, 42) if isDarkTheme() else QColor(240, 244, 249)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        if sys.platform == "darwin":
            self.setSystemTitleBarButtonVisible(True)
            self.titleBar.minBtn.hide()
            self.titleBar.maxBtn.hide()
            self.titleBar.closeBtn.hide()

        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.instance().screens()[0].size()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.account = account_
        self.bind()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/background.jpg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def bind(self):#绑定事件
        self.pushButtonLogin.clicked.connect(self.login)



    def login(self):#处理登录
        account = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        if account == "" or password == "":
            InfoBar.error(
                title='错误',
                content="用户名或密码不能为空",
                orient=Qt.Vertical,  # 内容太长时可使用垂直布局
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        status,msg = self.account.login(account,password)
        if status:
            show_main_window(self.account,self.mainWindow)
            self.close()
        else:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,  # 内容太长时可使用垂直布局
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )



if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    #QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    #QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = LoginWindow()
    w.show()
    app.exec_()