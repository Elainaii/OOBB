from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QPushButton
from ui_login import Ui_Form

class MyWindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.login_button.clicked.connect(self.login)

    def hello(self):
        print("欧码吉利曼波")

    def login(self):
        account = self.account_edit.text()
        pwd = self.password_edit.text()
        print(account)
        print(pwd)
        if account == '114' and pwd == '514':
            print("登录成功")
        else:
            print("登录失败")


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
