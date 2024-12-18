from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PIL import Image
from qfluentwidgets import FluentIcon, ScrollArea, BodyLabel, GroupHeaderCardWidget, ElevatedCardWidget, CaptionLabel, \
    PasswordLineEdit, PrimaryPushButton, IconWidget, TitleLabel, SubtitleLabel, PushSettingCard, PrimaryPushSettingCard, \
    LineEdit, ComboBox, MessageBoxBase, InfoBar, InfoBarPosition, Dialog, MessageBox, ComboBoxSettingCard, PushButton

from src.client.core.account import AdminController

class AddDepartmentMessageBox(MessageBoxBase):
    def __init__(self,controller:AdminController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.titleLabel = SubtitleLabel('添加院系')
        self.departmentLineEdit = LineEdit()

        self.didLineEdit = LineEdit()
        self.didLineEdit.setPlaceholderText("请输入院系编号")

        self.departmentLineEdit.setPlaceholderText("请输入院系名称")
        self.departmentLineEdit.setClearButtonEnabled(True)



        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.didLineEdit)
        self.viewLayout.addWidget(self.departmentLineEdit)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)


class AddDepartmentCard(PushSettingCard):
    def __init__(self,controller : AdminController,parent = None):
        super().__init__(text="添加", icon=FluentIcon.ADD, title="添加院系",content="添加一个新的院系",parent=parent)
        self.controller = controller
        self.clicked.connect(self.add)

    def add(self):
        self.w = AddDepartmentMessageBox(self.controller,self.parent())
        while self.w.exec():
            department = self.w.departmentLineEdit.text()
            if department != "" and self.w.didLineEdit.text() != "":
                data = {
                    "did":int(self.w.didLineEdit.text()),
                    "dept_name":department
                }
                status ,msg = self.controller.add_department(data)
                if status:
                    InfoBar.success(
                        title='成功',
                        content=msg,
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self.parent()
                    )
                    break
                else:
                    InfoBar.error(
                        title='错误',
                        content=msg,
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self.parent()
                    )
            else:
                InfoBar.error(
                    title='错误',
                    content='院系名称和编号不能为空',
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )



class ChangeDepartmentCard(GroupHeaderCardWidget):
    def __init__(self,controller:AdminController,parent = None):
        super().__init__(parent)
        self.setTitle("修改院系")
        self.setBorderRadius(8)

        self.controller = controller

        self.hintIcon = IconWidget(FluentIcon.INFO, self)

        self.departmentComboBox = ComboBox()
        for d in controller.account.dept_list:
            self.departmentComboBox.addItem(d['dept_name'])

        self.changeEdit = LineEdit()
        self.changeEdit.setPlaceholderText("请输入新的名称")

        self.hintLabel = BodyLabel("点击按钮更改名称 👉")
        self.submitButton = PrimaryPushButton(FluentIcon.ACCEPT_MEDIUM ,"提交")
        self.submitButton.clicked.connect(self.change)
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
        self.addGroup(FluentIcon.PEOPLE,'选择一个院系', "从下拉菜单中选择一个要更改的院系", self.departmentComboBox)
        group = self.addGroup(FluentIcon.EDIT, '更改名称', "", self.changeEdit)
        group.setSeparatorVisible(True)
        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)

    def change(self):
        did = self.controller.account.dept_list[self.departmentComboBox.currentIndex()]['did']
        name = self.changeEdit.text()
        if name == self.departmentComboBox.currentText():
            InfoBar.error(
                title='错误',
                content="新名称不能和原名称相同",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        if name:
            data = {
                "did":did,
                "dept_name":name
            }
            status,msg =  self.controller.change_department(data)
            if status:
                InfoBar.success(
                    title='成功',
                    content=msg,
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
                self.reset()
                return
            else:
                InfoBar.error(
                    title='错误',
                    content=msg,
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
        else:
            InfoBar.error(
                title='错误',
                content="新名称不能为空",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )

    def reset(self):
        self.controller.account.get_dept_list()
        self.departmentComboBox.clear()
        for d in self.controller.account.dept_list:
            self.departmentComboBox.addItem(d['dept_name'])

class SemesterCard(GroupHeaderCardWidget):
    def __init__(self,controller:AdminController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setTitle("学期")
        self.setBorderRadius(8)
        #self.hintIcon = IconWidget(FluentIcon.INFO, self)
        self.semesterComboBox = ComboBox()

        self.addButton = PushButton(FluentIcon.ADD, "添加")
        self.addButton.clicked.connect(self.add)

        for s in controller.account.semester_list:
            self.semesterComboBox.addItem(str(s['year']) + str(s['season']))

        self.addGroup(FluentIcon.BOOK_SHELF, '查看学期', "从下拉菜单中查看学期", self.semesterComboBox)
        group = self.addGroup(FluentIcon.ADD, '添加', "添加一个新学期", self.addButton)



    def add(self):
        w = MessageBox("添加学期", "确定添加一个新的学期吗？操作不可逆", parent=self.parent())
        if w.exec():
            pass
        else:
            pass






class OthersInterface(ScrollArea):
    def __init__(self,controller:AdminController, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.changeDepartmentCard = ChangeDepartmentCard(controller,self.view)
        self.addDepartmentCard = AddDepartmentCard(controller,self.view)
        self.semesterCard = SemesterCard(controller,self.view)



        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("other_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.changeDepartmentCard, 0)
        self.vBoxLayout.addWidget(self.addDepartmentCard, 0)
        self.vBoxLayout.addWidget(self.semesterCard, 0)

