from math import copysign
from msilib.schema import ComboBox, CheckBox

from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup, QCursor,QAction
from PySide6.QtCore import Qt, QSortFilterProxyModel, QAbstractItemModel, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView, QSizePolicy, QTableView, QHeaderView, \
    QButtonGroup, QHBoxLayout, QFileDialog

from qfluentwidgets import (ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
                            SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont,
                            RoundMenu, \
                            TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget, MessageBoxBase,
                            SubtitleLabel, DatePicker,
                            ComboBox, CheckBox, RadioButton, InfoBar, InfoBarPosition)


from src.client.core.account import Account, AdminController
import pandas as pd

class ChangePasswordMessageBox(MessageBoxBase):
    def __init__(self,controller:AdminController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.titleLabel = SubtitleLabel('修改密码')
        self.nameEdit = LineEdit()
        self.idEdit = LineEdit()
        #self.oldPasswordEdit = LineEdit()
        self.newPasswordEdit = LineEdit()
        self.confirmPasswordEdit = LineEdit()

        self.nameEdit.setPlaceholderText('输入姓名')
        self.idEdit.setPlaceholderText('输入id')
        # self.oldPasswordEdit.setPlaceholderText('输入旧密码')
        self.newPasswordEdit.setPlaceholderText('输入新密码')
        self.confirmPasswordEdit.setPlaceholderText('确认新密码')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameEdit)
        self.viewLayout.addWidget(self.idEdit)
        #self.viewLayout.addWidget(self.oldPasswordEdit)
        self.viewLayout.addWidget(self.newPasswordEdit)
        self.viewLayout.addWidget(self.confirmPasswordEdit)

        self.widget.setMinimumWidth(350)


class AddStudentMessageBox(MessageBoxBase):
    """ Custom message box """
    '''data['sid'], data['student_name'], data['did'], data['sex'], data['birthday'], data['ID_number'], data['Email'], data['mid']'''
    def __init__(self, controller:AdminController,parent=None):
        super().__init__(parent)
        self.controller = controller

        self.titleLabel = SubtitleLabel('添加学生')
        self.sidLineEdit = LineEdit()
        self.nameLineEdit = LineEdit()
        self.didEdit = ComboBox()
        self.w = QWidget()
        self.manRadioButton = RadioButton('男')
        self.womanRadioButton = RadioButton('女')
        self.buttonGroup = QButtonGroup(self.w)
        self.buttonGroup.addButton(self.manRadioButton)
        self.buttonGroup.addButton(self.womanRadioButton)
        self.sexLayout = QHBoxLayout()
        self.sexLayout.addWidget(self.manRadioButton)
        self.sexLayout.addWidget(self.womanRadioButton)
        self.sexLineEdit = RadioButton()
        self.birthEdit = DatePicker()
        self.midEdit = ComboBox()
        self.EmailLineEdit = LineEdit()
        self.IDnumberLineEdit = LineEdit()

        self.sidLineEdit.setPlaceholderText('输入学号')
        self.sidLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.setPlaceholderText('输入姓名')
        self.nameLineEdit.setClearButtonEnabled(True)
        self.didEdit.setPlaceholderText('选择院系')
        self.midEdit.setPlaceholderText('选择专业')
        self.EmailLineEdit.setPlaceholderText('输入邮箱')
        self.EmailLineEdit.setClearButtonEnabled(True)
        self.IDnumberLineEdit.setPlaceholderText('输入身份证号')

        #添加院系，专业
        for i in self.controller.account.dept_list:
            self.didEdit.addItem(i['dept_name'])
        for i in self.controller.account.major_list:
            self.midEdit.addItem(i['major_name'])


        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.sidLineEdit)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.didEdit)
        self.viewLayout.addLayout(self.sexLayout)
        self.viewLayout.addWidget(self.birthEdit)
        self.viewLayout.addWidget(self.midEdit)
        self.viewLayout.addWidget(self.EmailLineEdit)
        self.viewLayout.addWidget(self.IDnumberLineEdit)


        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)


class ChangeStudentInfoMessageBox(MessageBoxBase):
    """ Custom message box """
    '''data['sid'], data['student_name'], data['did'], data['sex'], data['birthday'], data['ID_number'], data['Email'], data['mid']'''
    def __init__(self, controller:AdminController,parent=None):
        super().__init__(parent)
        self.controller = controller

        self.titleLabel = SubtitleLabel('修改信息')
        self.sidLineEdit = LineEdit()
        self.nameLineEdit = LineEdit()
        self.didEdit = ComboBox()
        self.w = QWidget()
        self.manRadioButton = RadioButton('男')
        self.womanRadioButton = RadioButton('女')
        self.buttonGroup = QButtonGroup(self.w)
        self.buttonGroup.addButton(self.manRadioButton)
        self.buttonGroup.addButton(self.womanRadioButton)
        self.sexLayout = QHBoxLayout()
        self.sexLayout.addWidget(self.manRadioButton)
        self.sexLayout.addWidget(self.womanRadioButton)
        self.sexLineEdit = RadioButton()
        self.birthEdit = DatePicker()
        self.midEdit = ComboBox()
        self.EmailLineEdit = LineEdit()
        self.IDnumberLineEdit = LineEdit()

        self.sidLineEdit.setPlaceholderText('输入学号')
        self.sidLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.setPlaceholderText('输入姓名')
        self.nameLineEdit.setClearButtonEnabled(True)
        self.didEdit.setPlaceholderText('选择院系')
        self.midEdit.setPlaceholderText('选择专业')
        self.EmailLineEdit.setPlaceholderText('输入邮箱')
        self.EmailLineEdit.setClearButtonEnabled(True)
        self.IDnumberLineEdit.setPlaceholderText('输入身份证号')

        #添加院系，专业
        for i in self.controller.account.dept_list:
            self.didEdit.addItem(i['dept_name'])
        for i in self.controller.account.major_list:
            self.midEdit.addItem(i['major_name'])


        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.sidLineEdit)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.didEdit)
        self.viewLayout.addLayout(self.sexLayout)
        self.viewLayout.addWidget(self.birthEdit)
        self.viewLayout.addWidget(self.midEdit)
        self.viewLayout.addWidget(self.EmailLineEdit)
        self.viewLayout.addWidget(self.IDnumberLineEdit)


        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)

class StudentTableView(TableView):
    def __init__(self,controller:AdminController,parent = None):
        super().__init__(parent)
        self.controller = controller
        controller.get_student_list()
        self.data = controller.student_list

        self.model = QStandardItemModel()
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['sid'])))
            self.model.setItem(i, 1, QStandardItem(row['student_name']))
            self.model.setItem(i, 2, QStandardItem(row['sex']))
            self.model.setItem(i, 3, QStandardItem(row['dept_name']))
            self.model.setItem(i, 4, QStandardItem(row['major_name']))
            self.model.setItem(i, 5, QStandardItem(row['birthday']))
            self.model.setItem(i, 6, QStandardItem(row['ID_number']))
            self.model.setItem(i, 7, QStandardItem(row['Email']))


        self.model.setHorizontalHeaderLabels(['id','姓名', '性别','部门', '专业', '生日','身份证','Email'])

        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        #self.agentModel.setFilterKeyColumn(-1)
        self.menu = None



        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        #self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_rightmenu)


    def reset(self):
        self.data = self.controller.student_list
        self.model.removeRows(0, self.model.rowCount())
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['sid'])))
            self.model.setItem(i, 1, QStandardItem(row['student_name']))
            self.model.setItem(i, 2, QStandardItem(row['sex']))
            self.model.setItem(i, 3, QStandardItem(row['dept_name']))
            self.model.setItem(i, 4, QStandardItem(row['major_name']))
            self.model.setItem(i, 5, QStandardItem(row['birthday']))
            self.model.setItem(i, 6, QStandardItem(row['ID_number']))
            self.model.setItem(i, 7, QStandardItem(row['Email']))
        self.agentModel.setSourceModel(self.model)

    def show_rightmenu(self,pos):
        index = self.indexAt(pos) # 返回点击的index
        if index.isValid(): # 如果有index,则弹出菜单,并且高光选中的行
            self.setCurrentIndex(index)
            self.menu = RoundMenu()
            #self.l.setCurrentIndex(Q)
            # 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标
            self.copyAction = Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功"))
            # self.deleteAction = Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功"))
            self.passwordAction = Action(FluentIcon.EDIT,'修改密码',triggered= self.changePassword)
            self.infoAction = Action(FluentIcon.LABEL,'修改信息',triggered =self.changeInfo)
            self.menu.addAction(self.copyAction)
            # self.menu.addAction(self.deleteAction)
            self.menu.addAction(self.passwordAction)
            self.menu.addAction(self.infoAction)


            # 批量添加动作
            # 添加分割线
            # 子菜单

            #menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        self.menu.exec(QCursor.pos())

    def changePassword(self):
        self.changePasswordBox = ChangePasswordMessageBox(self.controller,self.parent())
        self.changePasswordBox.nameEdit.setText(self.data[self.currentIndex().row()]['student_name'])
        self.changePasswordBox.idEdit.setText(str(self.data[self.currentIndex().row()]['sid']))

        while self.changePasswordBox.exec():
            name = self.changePasswordBox.nameEdit.text()
            sid = self.changePasswordBox.idEdit.text()
            # oldPassword = self.changePasswordBox.oldPasswordEdit.text()
            newPassword = self.changePasswordBox.newPasswordEdit.text()
            confirmPassword = self.changePasswordBox.confirmPasswordEdit.text()
            if name == '' or sid == '' or newPassword == '' or confirmPassword == '':
                InfoBar.error(
                    title='错误',
                    content="请填写完整内容",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
            else:
                data = {
                    'account_id':sid,
                    # 'old_password':oldPassword,
                    'password':newPassword,
                }
                status,msg = self.controller.change_password(data)
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

    def changeInfo(self):
        self.changeInfoBox = ChangeStudentInfoMessageBox(self.controller,self.parent())
        self.changeInfoBox.sidLineEdit.setText(str(self.data[self.currentIndex().row()]['sid']))
        self.changeInfoBox.nameLineEdit.setText(self.data[self.currentIndex().row()]['student_name'])
        self.changeInfoBox.didEdit.setCurrentText(self.data[self.currentIndex().row()]['dept_name'])
        self.changeInfoBox.midEdit.setCurrentText(self.data[self.currentIndex().row()]['major_name'])
        self.changeInfoBox.EmailLineEdit.setText(self.data[self.currentIndex().row()]['Email'])
        self.changeInfoBox.IDnumberLineEdit.setText(self.data[self.currentIndex().row()]['ID_number'])
        while self.changeInfoBox.exec():
            name = self.changeInfoBox.nameLineEdit.text()
            sid = self.changeInfoBox.sidLineEdit.text()
            did = self.controller.account.dept_list[self.changeInfoBox.didEdit.currentIndex()]['did']
            sex = self.changeInfoBox.buttonGroup.checkedButton()
            birth = self.changeInfoBox.birthEdit.date.toString("yyyy-MM-dd")
            mid = self.controller.account.major_list[self.changeInfoBox.midEdit.currentIndex()]['mid']
            email = self.changeInfoBox.EmailLineEdit.text()
            id_number = self.changeInfoBox.IDnumberLineEdit.text()

            if name == '' or sid == '' or did == -1 or mid == -1 or email == '' or birth == '' or sex is None or id_number == '':
                InfoBar.error(
                    title='错误',
                    content="请填写完整内容",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
            else:
                data = {
                    'sid':sid,
                    'student_name':name,
                    'did':did,
                    'mid':mid,
                    'Email':email,
                    'sex':sex.text(),
                    'birthday':birth,
                    'ID_number':id_number
                }
                if data['sex'] == '男':
                    data['sex'] = 'M'
                else:
                    data['sex'] = 'F'
                status,msg = self.controller.change_student_info(data)
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



class StudentCommandBar(CommandBar):
    def __init__(self,controller :AdminController,parent = None):
        super().__init__(parent)

        self.pageSignal = Signal(int)
        self.controller = controller

        self.add = Action(FluentIcon.ADD, "添加", self,triggered = self.addStudent)
        self.refresh = Action(FluentIcon.SYNC, "刷新", self) # TODO: 刷新学生列表
        self.share = Action(FluentIcon.SHARE, "导出", self)
        self.addAction(self.add)
        self.addAction(self.refresh)
        self.addAction(self.share)
        self.addSeparator()
        self.up = Action(FluentIcon.UP, "")
        self.down = Action(FluentIcon.DOWN, "")
        self.addAction(self.up)
        self.addAction(self.down)


        self.pageLabel1 = CaptionLabel()
        self.pageLabel1.setText("当前第")
        self.pageEdit = LineEdit()
        self.pageEdit.setText('0')
        self.pageEdit.setFixedWidth(50)  # 连接时要设置宽度
        self.pageLabel2 = CaptionLabel()
        self.pageLabel2.setText("页,共??页")

        self.addWidget(self.pageLabel1)
        self.addWidget(self.pageEdit)
        self.addWidget(self.pageLabel2)
        self.addSeparator()

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)



    def addStudent(self):
        print("添加学生")
        self.addStudentMessageBox = AddStudentMessageBox(self.controller,self.parent())
        while self.addStudentMessageBox.exec():
            name = self.addStudentMessageBox.nameLineEdit.text()
            sid = self.addStudentMessageBox.sidLineEdit.text()
            did = self.controller.account.dept_list[self.addStudentMessageBox.didEdit.currentIndex()]['did']
            sex = self.addStudentMessageBox.buttonGroup.checkedButton()
            birth = self.addStudentMessageBox.birthEdit.date.toString("yyyy-MM-dd")
            mid = self.controller.account.major_list[self.addStudentMessageBox.midEdit.currentIndex()]['mid']
            email = self.addStudentMessageBox.EmailLineEdit.text()
            id_number = self.addStudentMessageBox.IDnumberLineEdit.text()

            if name == '' or sid == '' or did == -1 or mid == -1 or email == '' or birth == '' or sex is None or id_number == '':
                InfoBar.error(
                    title='错误',
                    content="请填写完整内容",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
            else:
                data = {
                    'sid':sid,
                    'student_name':name,
                    'did':did,
                    'mid':mid,
                    'Email':email,
                    'sex':sex.text(),
                    'birthday':birth,
                    'ID_number':id_number
                }
                if data['sex'] == '男':
                    data['sex'] = 'M'
                else:
                    data['sex'] = 'F'
                status,msg = self.controller.add_student(data)
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


class StudentInterface(ScrollArea):

    def __init__(self, controller:AdminController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        self.commandBar = StudentCommandBar(controller,self.view)
        self.table = StudentTableView(controller,self)
        self.commandBar.up.triggered.connect(self.prev_page)
        self.commandBar.down.triggered.connect(self.next_page)
        self.commandBar.share.triggered.connect(self.share)
        self.commandBar.refresh.triggered.connect(self.refresh)
        self.commandBar.pageEdit.textEdited.connect(self.change_page)

        self.commandBar.search.textEdited.connect(lambda str1: self.table.agentModel.setFilterRegularExpression(str1))
        self.commandBar.pageLabel2.setText("页,共" + str(self.controller.student_total_page) + "页")

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.commandBar,0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.table, 0)



        self.enableTransparentBackground()

    def prev_page(self):
        status, msg = self.controller.student_prev_page()
        if status:
            self.table.reset()
            self.commandBar.pageEdit.setText(str(self.controller.student_curr_page))
        else:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
        return

    def next_page(self):
        status, msg = self.controller.student_next_page()
        if status:
            self.table.reset()
            self.commandBar.pageEdit.setText(str(self.controller.student_curr_page))

        else:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
        return

    def change_page(self):
        if self.commandBar.pageEdit.text() == '':
            return
        page_number = int(self.commandBar.pageEdit.text())
        if page_number<0 or page_number>self.controller.student_total_page-1:
            InfoBar.error(
                title='错误',
                content="页数超出范围",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
            return
        self.controller.student_curr_page = page_number
        self.controller.get_student_list()
        self.table.reset()
        return

    def refresh(self):
        self.controller.get_student_list()
        self.table.reset()
        return
    def share (self):
        # 先获取数据
        a, b, data = self.controller.get_all_student_list()
        df = pd.DataFrame(data)
        # 选择保存路径
        path = QFileDialog.getSaveFileName(self, '保存文件', '', 'Excel files (*.xlsx)')
        if path[0] == '':
            return
        df.to_excel(path[0], index=False)
        InfoBar.success(
            title='成功',
            content='导出成功',
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )
        return


