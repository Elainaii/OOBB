# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calc.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QWidget)

from qfluentwidgets import (CheckBox, ComboBox, LineEdit, PushButton,
    TextEdit)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(482, 540)
        self.lineEdit = LineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(30, 110, 311, 111))
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setReadOnly(True)
        self.comboBox = ComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(356, 20, 101, 31))
        self.checkBox = CheckBox(Form)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(390, 100, 78, 19))
        self.textEdit = TextEdit(Form)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(30, 10, 311, 81))
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(26, 415, 320, 52))
        self.horizontalLayout_4 = QHBoxLayout(self.widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton0 = PushButton(self.widget)
        self.pushButton0.setObjectName(u"pushButton0")
        self.pushButton0.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_4.addWidget(self.pushButton0)

        self.pushButtonCE = PushButton(self.widget)
        self.pushButtonCE.setObjectName(u"pushButtonCE")
        self.pushButtonCE.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_4.addWidget(self.pushButtonCE)

        self.pushButtonEqe = PushButton(self.widget)
        self.pushButtonEqe.setObjectName(u"pushButtonEqe")
        self.pushButtonEqe.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_4.addWidget(self.pushButtonEqe)

        self.pushButtonDiv = PushButton(self.widget)
        self.pushButtonDiv.setObjectName(u"pushButtonDiv")
        self.pushButtonDiv.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_4.addWidget(self.pushButtonDiv)

        self.widget1 = QWidget(Form)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(26, 357, 320, 52))
        self.horizontalLayout_3 = QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton1 = PushButton(self.widget1)
        self.pushButton1.setObjectName(u"pushButton1")
        self.pushButton1.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_3.addWidget(self.pushButton1)

        self.pushButton2 = PushButton(self.widget1)
        self.pushButton2.setObjectName(u"pushButton2")
        self.pushButton2.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_3.addWidget(self.pushButton2)

        self.pushButton3 = PushButton(self.widget1)
        self.pushButton3.setObjectName(u"pushButton3")
        self.pushButton3.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_3.addWidget(self.pushButton3)

        self.pushButtonMul = PushButton(self.widget1)
        self.pushButtonMul.setObjectName(u"pushButtonMul")
        self.pushButtonMul.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_3.addWidget(self.pushButtonMul)

        self.widget2 = QWidget(Form)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(26, 241, 320, 52))
        self.horizontalLayout = QHBoxLayout(self.widget2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton7 = PushButton(self.widget2)
        self.pushButton7.setObjectName(u"pushButton7")
        self.pushButton7.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.pushButton7)

        self.pushButton8 = PushButton(self.widget2)
        self.pushButton8.setObjectName(u"pushButton8")
        self.pushButton8.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.pushButton8)

        self.pushButton9 = PushButton(self.widget2)
        self.pushButton9.setObjectName(u"pushButton9")
        self.pushButton9.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.pushButton9)

        self.pushButtonPlus = PushButton(self.widget2)
        self.pushButtonPlus.setObjectName(u"pushButtonPlus")
        self.pushButtonPlus.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.pushButtonPlus)

        self.pushButton6 = PushButton(Form)
        self.pushButton6.setObjectName(u"pushButton6")
        self.pushButton6.setGeometry(QRect(189, 300, 75, 50))
        self.pushButton6.setMinimumSize(QSize(0, 50))
        self.pushButton6.setCheckable(False)
        self.pushButton4 = PushButton(Form)
        self.pushButton4.setObjectName(u"pushButton4")
        self.pushButton4.setGeometry(QRect(27, 300, 75, 50))
        self.pushButton4.setMinimumSize(QSize(0, 50))
        self.pushButton5 = PushButton(Form)
        self.pushButton5.setObjectName(u"pushButton5")
        self.pushButton5.setGeometry(QRect(108, 300, 75, 50))
        self.pushButton5.setMinimumSize(QSize(0, 50))
        self.pushButtonMin = PushButton(Form)
        self.pushButtonMin.setObjectName(u"pushButtonMin")
        self.pushButtonMin.setGeometry(QRect(270, 300, 75, 50))
        self.pushButtonMin.setMinimumSize(QSize(0, 50))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"114", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"514", None))

        self.checkBox.setText(QCoreApplication.translate("Form", u"\u66fc\u6ce2", None))
        self.pushButton0.setText(QCoreApplication.translate("Form", u"0", None))
        self.pushButtonCE.setText(QCoreApplication.translate("Form", u"CE", None))
        self.pushButtonEqe.setText(QCoreApplication.translate("Form", u"=", None))
        self.pushButtonDiv.setText(QCoreApplication.translate("Form", u"/", None))
        self.pushButton1.setText(QCoreApplication.translate("Form", u"1", None))
        self.pushButton2.setText(QCoreApplication.translate("Form", u"2", None))
        self.pushButton3.setText(QCoreApplication.translate("Form", u"3", None))
        self.pushButtonMul.setText(QCoreApplication.translate("Form", u"*", None))
        self.pushButton7.setText(QCoreApplication.translate("Form", u"7", None))
        self.pushButton8.setText(QCoreApplication.translate("Form", u"8", None))
        self.pushButton9.setText(QCoreApplication.translate("Form", u"9", None))
        self.pushButtonPlus.setText(QCoreApplication.translate("Form", u"+", None))
        self.pushButton6.setText(QCoreApplication.translate("Form", u"6", None))
        self.pushButton4.setText(QCoreApplication.translate("Form", u"4", None))
        self.pushButton5.setText(QCoreApplication.translate("Form", u"5", None))
        self.pushButtonMin.setText(QCoreApplication.translate("Form", u"-", None))
    # retranslateUi

