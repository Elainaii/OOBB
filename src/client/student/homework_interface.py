from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PIL import Image
from qfluentwidgets import FluentIcon, ScrollArea, BodyLabel, GroupHeaderCardWidget, ElevatedCardWidget, CaptionLabel, \
    PasswordLineEdit, PrimaryPushButton, IconWidget, TitleLabel, SubtitleLabel, PushSettingCard, PrimaryPushSettingCard



class HomeworkInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)



        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
