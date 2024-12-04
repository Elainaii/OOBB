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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

from qfluentwidgets import PushButton

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(429, 449)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton5 = PushButton(Form)
        self.pushButton5.setObjectName(u"pushButton5")
        self.pushButton5.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton5, 3, 1, 1, 1)

        self.textEdit = QTextEdit(Form)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setCursorWidth(0)
        self.textEdit.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 4)

        self.pushButton6 = PushButton(Form)
        self.pushButton6.setObjectName(u"pushButton6")
        self.pushButton6.setMinimumSize(QSize(0, 50))
        self.pushButton6.setCheckable(False)

        self.gridLayout.addWidget(self.pushButton6, 3, 2, 1, 1)

        self.pushButtonDiv = PushButton(Form)
        self.pushButtonDiv.setObjectName(u"pushButtonDiv")
        self.pushButtonDiv.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButtonDiv, 5, 2, 1, 1)

        self.pushButtonMul = PushButton(Form)
        self.pushButtonMul.setObjectName(u"pushButtonMul")
        self.pushButtonMul.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButtonMul, 4, 3, 1, 1)

        self.pushButton1 = PushButton(Form)
        self.pushButton1.setObjectName(u"pushButton1")
        self.pushButton1.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton1, 4, 0, 1, 1)

        self.pushButton9 = PushButton(Form)
        self.pushButton9.setObjectName(u"pushButton9")
        self.pushButton9.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton9, 2, 2, 1, 1)

        self.pushButtonMin = PushButton(Form)
        self.pushButtonMin.setObjectName(u"pushButtonMin")
        self.pushButtonMin.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButtonMin, 3, 3, 1, 1)

        self.pushButtonCE = PushButton(Form)
        self.pushButtonCE.setObjectName(u"pushButtonCE")
        self.pushButtonCE.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButtonCE, 5, 1, 1, 1)

        self.pushButton0 = PushButton(Form)
        self.pushButton0.setObjectName(u"pushButton0")
        self.pushButton0.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton0, 5, 0, 1, 1)

        self.pushButton8 = PushButton(Form)
        self.pushButton8.setObjectName(u"pushButton8")
        self.pushButton8.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton8, 2, 1, 1, 1)

        self.pushButton2 = PushButton(Form)
        self.pushButton2.setObjectName(u"pushButton2")
        self.pushButton2.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton2, 4, 1, 1, 1)

        self.pushButtonPlus = PushButton(Form)
        self.pushButtonPlus.setObjectName(u"pushButtonPlus")
        self.pushButtonPlus.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButtonPlus, 2, 3, 1, 1)

        self.pushButton3 = PushButton(Form)
        self.pushButton3.setObjectName(u"pushButton3")
        self.pushButton3.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton3, 4, 2, 1, 1)

        self.pushButton4 = PushButton(Form)
        self.pushButton4.setObjectName(u"pushButton4")
        self.pushButton4.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton4, 3, 0, 1, 1)

        self.pushButtonEqe = PushButton(Form)
        self.pushButtonEqe.setObjectName(u"pushButtonEqe")
        self.pushButtonEqe.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButtonEqe, 5, 3, 1, 1)

        self.pushButton7 = PushButton(Form)
        self.pushButton7.setObjectName(u"pushButton7")
        self.pushButton7.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton7, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton5.setText(QCoreApplication.translate("Form", u"5", None))
        self.pushButton6.setText(QCoreApplication.translate("Form", u"6", None))
        self.pushButtonDiv.setText(QCoreApplication.translate("Form", u"/", None))
        self.pushButtonMul.setText(QCoreApplication.translate("Form", u"*", None))
        self.pushButton1.setText(QCoreApplication.translate("Form", u"1", None))
        self.pushButton9.setText(QCoreApplication.translate("Form", u"9", None))
        self.pushButtonMin.setText(QCoreApplication.translate("Form", u"-", None))
        self.pushButtonCE.setText(QCoreApplication.translate("Form", u"CE", None))
        self.pushButton0.setText(QCoreApplication.translate("Form", u"0", None))
        self.pushButton8.setText(QCoreApplication.translate("Form", u"8", None))
        self.pushButton2.setText(QCoreApplication.translate("Form", u"2", None))
        self.pushButtonPlus.setText(QCoreApplication.translate("Form", u"+", None))
        self.pushButton3.setText(QCoreApplication.translate("Form", u"3", None))
        self.pushButton4.setText(QCoreApplication.translate("Form", u"4", None))
        self.pushButtonEqe.setText(QCoreApplication.translate("Form", u"=", None))
        self.pushButton7.setText(QCoreApplication.translate("Form", u"7", None))
    # retranslateUi

