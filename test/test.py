from PySide6.QtWidgets import QApplication,QWidget
from ui_calc import Ui_Form


class Window(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__=='__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()