from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QPushButton
from ui_calc import Ui_Form

class MyWindow(QWidget,Ui_Form):
    op = ''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton0.clicked.connect(lambda :self.addOp('0'))
        self.pushButton1.clicked.connect(lambda :self.addOp('1'))
        self.pushButton2.clicked.connect(lambda :self.addOp('2'))
        self.pushButton3.clicked.connect(lambda :self.addOp('3'))
        self.pushButton4.clicked.connect(lambda :self.addOp('4'))
        self.pushButton5.clicked.connect(lambda :self.addOp('5'))
        self.pushButton6.clicked.connect(lambda :self.addOp('6'))
        self.pushButton7.clicked.connect(lambda :self.addOp('7'))
        self.pushButton8.clicked.connect(lambda :self.addOp('8'))
        self.pushButton9.clicked.connect(lambda :self.addOp('9'))
        self.pushButtonEqe.clicked.connect(self.calc)
        self.pushButtonCE.clicked.connect(self.ce)

        self.pushButtonPlus.clicked.connect(lambda :self.addOp('+'))
        self.pushButtonMin.clicked.connect(lambda :self.addOp('-'))
        self.pushButtonMul.clicked.connect(lambda :self.addOp('*'))
        self.pushButtonDiv.clicked.connect(lambda :self.addOp('/'))

        self.comboBox.addItems(['Science','Program','Math'])
        self.comboBox.currentIndexChanged.connect(self.showi)

        self.checkBox.clicked.connect(lambda :print(self.checkBox.isChecked()))

    def addOp(self,op):
        self.lineEdit.clear()
        self.op = self.op + op
        self.lineEdit.setText(self.op)

    def calc(self):
        num = 0
        try:
            num = eval(self.op)
        except:
            self.textEdit.setMarkdown(' **Invalid Syntax: {}** '.format(self.op))
            self.op = ''
            self.lineEdit.setText(str(num))
            return


        self.lineEdit.setText(str(num))
        self.op = str(num)

    def ce(self):
        self.op = ''
        self.lineEdit.clear()

    def showi(self,index):
        print(index)

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
