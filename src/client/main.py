from PySide6.QtWidgets import QApplication
from src.client.login.login_window import LoginWindow



if __name__ == '__main__':

    app = QApplication([])
    login_window = LoginWindow()

    def show_main_window(user_id, identity):
        if identity == 'A':
            print("Admin")  # 这里之后改成展示界面
        elif identity == 'T':
            print("Teacher")
        else:
            print("Student")


    login_window.show()
    app.exec()