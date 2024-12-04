from PySide6.QtWidgets import QApplication,QWidget
from ui_233 import Ui_Form


class Window(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(lambda :print(self.comboBox.currentText()))

if __name__=='__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()