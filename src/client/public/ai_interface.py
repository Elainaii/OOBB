from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PIL import Image
from qfluentwidgets import FluentIcon, ScrollArea, BodyLabel, GroupHeaderCardWidget, ElevatedCardWidget, CaptionLabel, \
    PasswordLineEdit, PrimaryPushButton, IconWidget, TitleLabel, SubtitleLabel, PushSettingCard, PrimaryPushSettingCard, \
    PlainTextEdit, TextEdit, IndeterminateProgressBar, MessageBoxBase, IndeterminateProgressRing

from openai import OpenAI

from PySide6.QtCore import QThread, Signal

from src.client.core.config import Config

class WorkerThread(QThread):
    result_ready = Signal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        # 在这里执行耗时操作
        client = OpenAI(
            api_key=Config.GPT_SECRET_KEY,
            base_url="https://api.moonshot.cn/v1",
        )

        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.message,
            temperature=0.3,
            max_tokens=500
        )
        result = completion.choices[0].message.content
        self.result_ready.emit(result)

class AiOutputCard(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(350)
        self.setTitle("AI回答")
        self.inProgressBar = IndeterminateProgressBar(self)
        self.inProgressBar.setFixedWidth(900)
        self.inProgressBar.hide()
        self.setBorderRadius(8)
        self.setMaximumHeight(200)
        self.answer = TextEdit()
        self.answer.setPlaceholderText("AI回答")
        self.answer.setMinimumWidth(700)

        self.addGroup(FluentIcon.EDIT, "AI回答", "", self.answer)

class InputCard(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("输入")
        self.setBorderRadius(8)
        self.setMaximumHeight(200)
        self.hintIcon = IconWidget(FluentIcon.INFO, self)
        self.hintLabel = BodyLabel("点击按钮提交输入👉")
        self.submitButton = PrimaryPushButton(FluentIcon.ACCEPT_MEDIUM ,"提交")

        self.textEdit = PlainTextEdit()
        self.textEdit.setPlaceholderText("请输入文本")
        self.textEdit.setMinimumWidth(500)
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
        self.addGroup(FluentIcon.EDIT, "输入", "", self.textEdit)
        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)


        self.vBoxLayout.addLayout(self.bottomLayout)

class AiInterface(ScrollArea):
    def __init__(self, account_id, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)


        self.input = InputCard(self.view)
        self.output = AiOutputCard(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("account_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.input,0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.output,0, Qt.AlignmentFlag.AlignTop)

        self.input.submitButton.clicked.connect(self.get_answer)

    def get_answer(self):
        message = [
            {"role": "system",
             "content": "你是一个学生选课管理系统的ai助手，你可以回答一些关于选课的问题，但是每次回答不会特别复杂"},
            {"role": "user", "content": self.input.textEdit.toPlainText()}
        ]

        self.thread = WorkerThread(message)
        self.thread.result_ready.connect(self.display_answer)
        self.output.inProgressBar.show()
        self.thread.start()

    def display_answer(self, result):
        self.output.answer.setMarkdown(result)
        self.output.inProgressBar.hide()