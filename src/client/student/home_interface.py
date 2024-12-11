from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PIL import Image
from qfluentwidgets import FluentIcon, ScrollArea, BodyLabel, GroupHeaderCardWidget
import numpy as np


class InfoCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("个人信息")
        self.setBorderRadius(8)

        self.avgScoreLabel = BodyLabel("平均分数", self)
        self.totalCreditLabel = BodyLabel("总学分", self)
        self.totalCourseLabel = BodyLabel("总课程", self)

        # 添加组件到分组中
        self.addGroup(FluentIcon.DICTIONARY,"平均分数","你的平均分数",self.avgScoreLabel)
        self.addGroup(FluentIcon.CERTIFICATE,"学分","你的总学分",self.totalCreditLabel)
        self.addGroup(FluentIcon.CERTIFICATE,"课程","你的总课程数目",self.totalCourseLabel)


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(320)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = BodyLabel(f'学生账号 \nStudent Course', self)
        self.galleryLabel.setStyleSheet("color: white;font-size: 30px; font-weight: 600;")

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.GlobalColor.black)  # 阴影颜色
        shadow.setOffset(1.4, 1.4)     # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)

        self.img = Image.open("C:/Users/Elaina/Pictures/1700456291734.png")
        self.banner = None
        self.path = None



        self.galleryLabel.setObjectName('galleryLabel')

        # Create a horizontal layout for the linkCardView with bottom alignment and margin
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(20, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)

        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)

        if not self.banner or not self.path:
            image_height = self.img.width * self.height() // self.width()
            crop_area = (0, 0, self.img.width, image_height)  # (left, upper, right, lower)
            cropped_img = self.img.crop(crop_area)
            img_data = np.array(cropped_img)  # Convert PIL Image to numpy array
            height, width, channels = img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

            path = QPainterPath()
            path.addRoundedRect(0, 0, width + 50, height + 50, 10, 10)  # 10 is the radius for corners
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.infoCard = InfoCard(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.addWidget(self.infoCard)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    demo = HomeInterface()
    demo.show()
    sys.exit(app.exec())