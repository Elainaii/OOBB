from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt


from src.client.login.login_window import LoginWindow
from src.client.core.account import Account



if __name__ == '__main__':

    app = QApplication([])
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    account = Account()
    main_window = None
    login_window = LoginWindow(account,main_window)


    login_window.show()
    app.exec()