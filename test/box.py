
from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QRadioButton,QButtonGroup

class Box(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        bt1 = QRadioButton('男')
        bt2 = QRadioButton('女')
        group = QButtonGroup()
        group.addButton(bt1)
        group.addButton(bt2)
        self.layout.addWidget(bt1)
        self.layout.addWidget(bt2)



if __name__=='__main__':
    app = QApplication([])
    window = Box()
    window.show()
    app.exec()