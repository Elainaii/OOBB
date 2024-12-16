from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget,QApplication
from PySide6.QtCore import Qt
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition,setThemeColor

from src.client.core.account import Account

class TeacherMainWindow(MSFluentWindow):
    def __init__(self,account:Account = None, parent=None):
        super().__init__(parent)





        # add sub interfaces

        setThemeColor('#f18cb9', lazy=True)
        self.setFixedSize(960, 640)
        self.setWindowTitle('Teacher')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.titleBar.raise_()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    window = TeacherMainWindow()
    window.show()
    app.exec()
