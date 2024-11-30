# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from qfluentwidgets import (BodyLabel, LineEdit, PushButton)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(364, 345)
        self.account_edit = LineEdit(Form)
        self.account_edit.setObjectName(u"account_edit")
        self.account_edit.setGeometry(QRect(70, 110, 211, 21))
        self.password_edit = LineEdit(Form)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setGeometry(QRect(70, 170, 211, 20))
        self.login_button = PushButton(Form)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setGeometry(QRect(120, 230, 111, 31))
        self.password_label = BodyLabel(Form)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(70, 150, 50, 15))
        self.account_label = BodyLabel(Form)
        self.account_label.setObjectName(u"account_label")
        self.account_label.setGeometry(QRect(70, 90, 50, 15))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.account_edit.setToolTip(QCoreApplication.translate("Form", u"example@example.com", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.password_edit.setToolTip(QCoreApplication.translate("Form", u"password", None))
#endif // QT_CONFIG(tooltip)
        self.login_button.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.password_label.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801", None))
        self.account_label.setText(QCoreApplication.translate("Form", u"\u8d26\u53f7", None))
    # retranslateUi

