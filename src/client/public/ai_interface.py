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
    def __init__(self, account, parent=None):
        super().__init__(parent)
        self.account = account
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
        self.teacher_msg = {
            "role": "system",
            "content": "你是一个学生选课管理系统的ai助手，在回答问题时，你必须注意：1.你现在面对的是教师用户。"
                       +"2.你可以回答一些关于选课的问题，但是每次回答不会特别复杂"
                        +"3.系统的教师界面主要有三个子界面：主页（展示用户的姓名，工号，部门以及总课程数目），我的课程，添加课程，还有两个所有账户共有的界面，包括智能助手界面和账户界面，账户界面中可以修改用户自己的密码"
                        +"4.我的课程界面展示该用户（教师）的所有课程，包括课程名称，课程编号等信息，用户可以右键点击课程表格的一个课程，会弹出一个菜单，用户可以选择布置作业，批改作业，查看课程学生等操作"
                        +",查看课程学生操作会展示该课程的所有学生，包括学生的姓名，学号，分数等信息，用户可以右键点击学生表格的一个学生，会弹出一个菜单，用户可以选择设置分数、奖惩操作"
                        +"5.添加课程界面用户可以添加课程，包括课程名称，课程编号等信息，在添加课程时，用户需要先选择一门课程，然后再在这个基础上开课，开课时需要选择上课时间，上课地点等信息"

        }
        self.student_msg = {
            "role": "system",
            "content": "你是一个学生选课管理系统的ai助手，在回答问题时，你必须注意：1.你现在面对的是学生用户。"
                       +"2.你可以回答一些关于选课的问题，但是每次回答不会特别复杂"
                        +"3.系统的学生界面主要有三个子界面：主页（展示用户的平均分，总学分，=以及选课数目），我的课程，选课，奖励，作业，还有两个所有账户共有的界面，包括智能助手界面和账户界面，账户界面中可以修改用户自己的密码"
                        +"4.我的课程界面展示该用户（学生）的所有课程，包括课程名称，课程编号，授课教师，成绩等信息，"
                        +"5.选课界面用户可以选择课程，包括课程名称，课程编号等信息，用户可以右键点击一门课程，然后会弹出一个菜单，用户可以选择选课操作"
                        +"6.奖励界面用户可以查看自己的奖励，包括奖励名称，奖励内容等信息"
                        +"7.作业界面用户可以查看自己的作业，包括作业名称，作业内容，截止时间等信息，用户可以右键点击一份作业，然后会弹出一个菜单，用户可以选择提交作业操作"
                        +"8.你也可以回答一些学生关于课程价值、生涯发展等问题"

        }

        self.admin_msg = {
            "role": "system",
            "content": "你是一个学生选课管理系统的ai助手，在回答问题时，你必须注意：1.你现在面对的是管理员用户。"
        }
        if self.account.identity == "T":
            system_msg = self.teacher_msg
        elif self.account.identity == "S":
            system_msg = self.student_msg
        else:
            system_msg = self.admin_msg



        message = [
            system_msg,
            {"role": "user", "content": self.input.textEdit.toPlainText()}
        ]

        self.thread = WorkerThread(message)
        self.thread.result_ready.connect(self.display_answer)
        self.output.inProgressBar.show()
        self.thread.start()

    def display_answer(self, result):
        self.output.answer.setMarkdown(result)
        self.output.inProgressBar.hide()