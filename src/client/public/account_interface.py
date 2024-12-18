from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PIL import Image
from qfluentwidgets import FluentIcon, ScrollArea, BodyLabel, GroupHeaderCardWidget, ElevatedCardWidget, CaptionLabel, \
    PasswordLineEdit, PrimaryPushButton, IconWidget, TitleLabel, SubtitleLabel, PushSettingCard, PrimaryPushSettingCard
# from src.client.admin.admin_main_window import *

class ChangePasswordCard(GroupHeaderCardWidget):
    def __init__(self, account_id, parent = None):
        super().__init__(parent)
        self.setTitle("修改密码")
        self.setBorderRadius(8)

        self.hintIcon = IconWidget(FluentIcon.INFO, self)
        # 设置ID:为当前用户的ID
        self.idLabel = BodyLabel(f"ID: {account_id}")
        self.passwordEdit1 = PasswordLineEdit()
        self.passwordEdit2 = PasswordLineEdit()
        self.hintLabel = BodyLabel("点击按钮更改密码 👉")
        self.submitButton = PrimaryPushButton(FluentIcon.ACCEPT_MEDIUM ,"提交")
        self.bottomLayout = QHBoxLayout()
        # 设置底部工具栏布局
        self.bottomLayout.setSpacing(0)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.hintIcon, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.submitButton, 0, Qt.AlignmentFlag.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # 添加组件到分组中
        self.addGroup(FluentIcon.PEOPLE, "ID", "", self.idLabel)
        self.addGroup(FluentIcon.EDIT, "新的密码", "", self.passwordEdit1)
        group = self.addGroup(FluentIcon.EDIT, "再次输入新的密码", "", self.passwordEdit2)
        group.setSeparatorVisible(True)
        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)


class AccountInterface(ScrollArea):
    def     __init__(self, account_id, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.settingLabel = SubtitleLabel(self.view)
        self.settingLabel.setText("设置")
        self.changePasswordCard = ChangePasswordCard(account_id, self.view)
        self.logout = PrimaryPushSettingCard(
                        text="退出",
                        icon=FluentIcon.CLOSE,
                        title="退出登录",
                        content="从当前账户退出登录"
                        )
        #self.changePasswordCard2 = ChangePasswordCard(self.view)
        self.about =  PrimaryPushSettingCard(
                        text="转到Github",
                        icon=FluentIcon.INFO,
                        title="关于",
                        content="版本：0.114.514"
                        )


        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("account_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.settingLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.changePasswordCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.logout, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.about, 0, Qt.AlignmentFlag.AlignTop)
        #self.vBoxLayout.addWidget(self.changePasswordCard2, 0, Qt.AlignmentFlag.AlignTop)