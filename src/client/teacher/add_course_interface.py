from math import copysign

from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QActionGroup, QCursor,QAction
from PySide6.QtCore import Qt, QSortFilterProxyModel, QAbstractItemModel, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView, QSizePolicy, QTableView, QHeaderView, \
    QButtonGroup, QHBoxLayout, QStackedWidget

from qfluentwidgets import (ScrollArea, MSFluentWindow, FluentIcon, NavigationItemPosition, CommandBar, Action, \
                            SearchLineEdit, TableView, CaptionLabel, LineEdit, TransparentDropDownPushButton, setFont,
                            RoundMenu, \
                            TogglePushButton, CheckableMenu, MenuIndicatorType, ElevatedCardWidget, MessageBoxBase,
                            SubtitleLabel, DatePicker,
                            ComboBox, CheckBox, RadioButton, InfoBar, InfoBarPosition, BreadcrumbBar, HeaderCardWidget,
                            GroupHeaderCardWidget, PushButton, IconWidget, InfoBarIcon, PrimaryPushButton, BodyLabel,
                            PrimaryPushSettingCard, SpinBox)

from src.client.core.account import TeacherController

class AddNewCourseMessageBox(MessageBoxBase):
    def __init__(self, controller:TeacherController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.titleLabel = SubtitleLabel('添加课程')
        self.courseIdLineEdit = LineEdit()
        self.courseNameLineEdit = LineEdit()
        self.creditLineEdit = LineEdit()
        self.courseIdLineEdit.setPlaceholderText("请输入课程号")
        self.courseNameLineEdit.setPlaceholderText("请输入课程名称")
        self.departmentComboBox = ComboBox()
        for dept in controller.account.dept_list:
            self.departmentComboBox.addItem(dept['dept_name'])
        self.creditLineEdit.setPlaceholderText("请输入学分")
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.courseIdLineEdit)
        self.viewLayout.addWidget(self.departmentComboBox)
        self.viewLayout.addWidget(self.courseNameLineEdit)
        self.viewLayout.addWidget(self.creditLineEdit)
        self.widget.setMinimumWidth(350)

class AddCourseInfoCard(GroupHeaderCardWidget):

    def __init__(self, controller:TeacherController, parent=None):
        super().__init__(parent)
        self.setTitle("课程信息")
        self.controller = controller
        self.setBorderRadius(8)
        self.setFixedHeight(250)
        # data = controller.home_info
        # 将数据填充到组件中
        # 平均分 = data['avg_score']

        self.courseIdLabel = BodyLabel(f"课程ID：", self)
        self.creditLabel = BodyLabel(f"学分：", self)
        self.semesterLabel = BodyLabel(f"开课学期：", self)

        # 添加组件到分组中
        self.addGroup(FluentIcon.DICTIONARY,"课程ID","",self.courseIdLabel)
        self.addGroup(FluentIcon.CERTIFICATE,"学分","",self.creditLabel)
        self.addGroup(FluentIcon.CERTIFICATE,"开课学期","",self.semesterLabel)

    def updateInfo(self):
        courseId = self.controller.curr_add_course_id
        credit = 0
        for course in self.controller.all_course_list:
            if course['cid'] == courseId:
                credit = course['credit']
                break
        semester = str(self.controller.account.semester_list[0]['year']) + self.controller.account.semester_list[0]['season']
        self.courseIdLabel.setText(f"课程ID：{courseId}")
        self.creditLabel.setText(f"学分：{credit}")
        self.semesterLabel.setText(f"开课学期：{semester}")

class AddClassTimeMessageBox(MessageBoxBase):
    def __init__(self, controller:TeacherController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.titleLabel = SubtitleLabel('添加教室-时间信息')
        self.timeComboBox = ComboBox()
        self.classroomComboBox = ComboBox()
        self.hintLabel = BodyLabel("请输入开始周数和结束周数")
        self.beginWeekLineEdit = SpinBox()
        self.beginWeekLineEdit.setRange(1, 20)
        self.endWeekLineEdit = SpinBox()
        self.endWeekLineEdit.setRange(1, 20)

        for time in controller.time_slot_list:
            self.timeComboBox.addItem( '周' + str(time['day']) + ' ' + str(time['start_time']) + '-' + str(time['end_time']))

        for room in controller.classroom_list:
            self.classroomComboBox.addItem(room['building_name'] + ' ' + str(room['room_number']))

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.timeComboBox)
        self.viewLayout.addWidget(self.classroomComboBox)
        self.viewLayout.addWidget(self.hintLabel)
        self.viewLayout.addWidget(self.beginWeekLineEdit)
        self.viewLayout.addWidget(self.endWeekLineEdit)

        self.widget.setMinimumWidth(350)

class AddCourseTableCard(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('教室-时间信息')
        self.setBorderRadius(8)
        self.setMinimumHeight(300)
        self.setMaximumHeight(350)

        self.hintIcon = IconWidget(InfoBarIcon.INFORMATION)
        self.hintLabel = BodyLabel("点击添加按钮 👉")
        self.addButton = PrimaryPushButton(FluentIcon.ADD, "添加")
        self.bottomLayout = QHBoxLayout()

        self.table = TableView(self)
        self.model = QStandardItemModel()



        self.model.setHorizontalHeaderLabels(['时间', '教室','开始周数','结束周数'])
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.setModel(self.model)

        self.table.customContextMenuRequested.connect(self.show_rightmenu)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)

        self.delAction = Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功"))

        #底部按钮
        self.hintIcon.setFixedSize(16, 16)
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.hintIcon, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.addButton, 0, Qt.AlignmentFlag.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.vBoxLayout.addWidget(self.table, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addLayout(self.bottomLayout)



    def show_rightmenu(self,pos):
        index = self.table.indexAt(pos) # 返回点击的index
        if index.isValid(): # 如果有index,则弹出菜单,并且高光选中的行
            self.table.setCurrentIndex(index)
            self.menu = RoundMenu()


            self.menu.addAction(self.delAction)

        self.menu.exec(QCursor.pos())

class AddCourseCommandBar(CommandBar):
    def __init__(self,controller :TeacherController,parent = None):
        super().__init__(parent)

        self.controller = controller

        self.add = Action(FluentIcon.ADD, "添加", self,triggered = lambda :print("添加"))
        self.copy = Action(FluentIcon.COPY, "", self)
        self.share = Action(FluentIcon.SHARE, "", self)
        self.addAction(self.add)
        self.addAction(self.copy)
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
        self.pageLabel2.setText(f"页,共{self.controller.all_course_total_page}页")

        self.addWidget(self.pageLabel1)
        self.addWidget(self.pageEdit)
        self.addWidget(self.pageLabel2)
        self.addSeparator()

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)


class AddCourseTableView(TableView):
    def __init__(self,controller:TeacherController,parent = None):
        super().__init__(parent)
        self.controller = controller
        controller.get_all_course_list()
        self.data = controller.all_course_list

        self.model = QStandardItemModel()

        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['cid'])))
            self.model.setItem(i, 1, QStandardItem(row['dept_name']))
            self.model.setItem(i, 2, QStandardItem(row['course_name']))
            self.model.setItem(i, 3, QStandardItem(str(row['credit'])))


        self.model.setHorizontalHeaderLabels(['课程号', '开课部门','课程名', '学分'])

        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        #self.agentModel.setFilterKeyColumn(-1)
        self.menu = None


        self.setModel(self.agentModel)
        self.verticalHeader().hide()

        #self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.customContextMenuRequested.connect(self.show_rightmenu)
        self.resizeColumnsToContents()

        self.copyAction = Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功"))

        self.selectAction = Action(FluentIcon.EDIT, '选择课程', triggered=lambda: print("查看作业"))



    def reset(self):
        self.data = self.controller.all_course_list
        self.model.removeRows(0, self.model.rowCount())
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['cid'])))
            self.model.setItem(i, 1, QStandardItem(row['dept_name']))
            self.model.setItem(i, 2, QStandardItem(row['course_name']))
            self.model.setItem(i, 3, QStandardItem(str(row['credit'])))
        self.agentModel.setSourceModel(self.model)
        self.resizeColumnsToContents()

    def show_rightmenu(self,pos):
        index = self.indexAt(pos) # 返回点击的index
        if index.isValid(): # 如果有index,则弹出菜单,并且高光选中的行
            self.setCurrentIndex(index)
            self.menu = RoundMenu()
            #self.l.setCurrentIndex(Q)
            # 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标


            self.menu.addAction(self.copyAction)
            self.menu.addAction(self.selectAction)

        self.menu.exec(QCursor.pos())


class AddCourseInterface(ScrollArea):

    def __init__(self, controller:TeacherController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        # 选择课程界面
        self.select = QWidget(self.view)
        self.select.setObjectName("select")
        self.selectLayout = QVBoxLayout()
        self.commandBar = AddCourseCommandBar(self.controller,self.view)
        self.table = AddCourseTableView(self.controller,self)
        self.selectLayout.addWidget(self.commandBar)
        self.selectLayout.addWidget(self.table)
        self.select.setLayout(self.selectLayout)

        # 课程信息界面：时间槽，教室(messagebox)，容纳人数，学期，cid，sid
        self.add = QWidget(self.view)
        self.add.setObjectName("add")
        self.addLayout = QVBoxLayout()
        self.addCourseInfoCard = AddCourseInfoCard(self.controller,self.add)
        self.addCourseTableCard = AddCourseTableCard(self.add)
        self.submit = PrimaryPushSettingCard(
            text="提交",
            icon=FluentIcon.INFO,
            title="提交",
            content="将课程信息提交到数据库"
        )
        self.addLayout.addWidget(self.addCourseInfoCard, 0, Qt.AlignmentFlag.AlignTop)
        self.addLayout.addWidget(self.addCourseTableCard, 0, Qt.AlignmentFlag.AlignTop)
        self.addLayout.addWidget(self.submit, 0, Qt.AlignmentFlag.AlignTop)
        self.add.setLayout(self.addLayout)

        # 各种链接
        self.table.selectAction.triggered.connect(self.open_create_course)
        self.addCourseTableCard.addButton.clicked.connect(self.open_add_course_time_box)
        self.addCourseTableCard.delAction.triggered.connect(self.del_course_time)
        self.commandBar.add.triggered.connect(self.create_new_course)
        self.commandBar.up.triggered.connect(self.course_list_prev_page)
        self.commandBar.down.triggered.connect(self.course_list_next_page)
        self.commandBar.pageEdit.textEdited.connect(self.course_list_change_page)

        self.commandBar.pageLabel2.setText(f"页,共{self.controller.all_course_total_page}页")

        self.stack = QStackedWidget(self)

        self.stack.addWidget(self.select)
        self.stack.addWidget(self.add)

        self.stack.setCurrentWidget(self.select)

        self.breadcrumbBar = BreadcrumbBar(self)  # 面包屑导航栏
        self.breadcrumbBar.currentItemChanged.connect(self.switchInterface)
        setFont(self.breadcrumbBar, 18)
        self.breadcrumbBar.setSpacing(20)

        self.breadcrumbBar.addItem(self.select.objectName(), "选择待开课的课程")
        # self.breadcrumbBar.addItem(self.t.objectName(), "学生管理")

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("add_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)

        self.vBoxLayout.addWidget(self.breadcrumbBar, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.stack, 0, Qt.AlignmentFlag.AlignTop)

        self.enableTransparentBackground()


    def open_create_course(self):
        self.stack.setCurrentWidget(self.add)
        self.breadcrumbBar.addItem(self.add.objectName(), "填写课程信息")
        self.controller.curr_add_course_id =  self.controller.all_course_list[self.table.currentIndex().row()]['cid']
        self.addCourseInfoCard.updateInfo()

    def open_add_course_time_box(self):
        self.messageBox = AddClassTimeMessageBox(self.controller,self.parent())
        if self.messageBox.exec():
            time_slot_id = self.controller.time_slot_list[self.messageBox.timeComboBox.currentIndex()]['timeslot_id']
            classroom_id = self.controller.classroom_list[self.messageBox.classroomComboBox.currentIndex()]['classroom_id']
            begin_week = self.messageBox.beginWeekLineEdit.value()
            end_week = self.messageBox.endWeekLineEdit.value()
            self.add_course_time(time_slot_id,classroom_id,begin_week,end_week)

    def del_course_time(self):
        time_slot_id = self.controller.time_classroom_list[self.addCourseTableCard.table.currentIndex().row()]['time_slot_id']
        classroom_id = self.controller.time_classroom_list[self.addCourseTableCard.table.currentIndex().row()]['classroom_id']
        begin_week = self.messageBox.beginWeekLineEdit.value()
        end_week = self.messageBox.endWeekLineEdit.value()
        status,msg = self.controller.del_course_time_list(time_slot_id,classroom_id,begin_week,end_week)
        if not status:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        InfoBar.success(
            title='成功',
            content='删除成功',
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent()
        )
        self.addCourseTableCard.model.removeRow(self.addCourseTableCard.table.currentIndex().row())

    def add_course_time(self,time_slot_id,classroom_id,begin_week,end_week):
        status,msg = self.controller.add_course_time_list(time_slot_id,classroom_id,begin_week,end_week)
        if not status:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        InfoBar.success(
            title='成功',
            content='添加成功',
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent()
        )
        self.addCourseTableCard.model.appendRow([
            QStandardItem('周' +
                          str(self.controller.time_slot_list[time_slot_id-1]['day']) +
                          ' ' +
                          str(self.controller.time_slot_list[time_slot_id-1]['start_time']) +
                          '-' +
                          str(self.controller.time_slot_list[time_slot_id-1]['end_time']))
            ,
            QStandardItem(self.controller.classroom_list[classroom_id-1]['building_name'] +
                          ' ' +
                          str(self.controller.classroom_list[classroom_id-1]['room_number']))
            ,QStandardItem(str(begin_week)),QStandardItem(str(end_week))
        ])
        #self.addCourseTableCard.table.resizeColumnsToContents()

    def submit_course(self):
        status,msg = self.controller.submit_course()
        if not status:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        InfoBar.success(
            title='成功',
            content='提交成功',
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent()
        )
        self.controller.reset_course_time_list()
        self.addCourseTableCard.model.removeRows(0, self.addCourseTableCard.model.rowCount())
        self.switchInterface('select')

    def create_new_course(self):#创建新课程,不是section
        self.messageBox = AddNewCourseMessageBox(self.controller,self.parent())
        while self.messageBox.exec():
            data = {
                "cid":self.messageBox.courseIdLineEdit.text(),
                "course_name":self.messageBox.courseNameLineEdit.text(),
                "did":self.controller.account.dept_list[self.messageBox.departmentComboBox.currentIndex()]['did'],
                "credit":self.messageBox.creditLineEdit.text()
            }
            status,msg = self.controller.create_new_course(data)
            if not status:
                InfoBar.error(
                    title='错误',
                    content=msg,
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent()
                )
                continue
            InfoBar.success(
                title='成功',
                content='创建成功',
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            self.controller.get_all_course_list()
            self.table.reset()
            break

    def course_list_next_page(self):
        status,msg = self.controller.course_list_next_page()
        if not status:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        self.table.reset()
        self.commandBar.pageEdit.setText(str(self.controller.all_course_curr_page))

    def course_list_prev_page(self):
        status,msg = self.controller.course_list_prev_page()
        if not status:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        self.table.reset()
        self.commandBar.pageEdit.setText(str(self.controller.all_course_curr_page))

    def course_list_change_page(self):
        text = self.commandBar.pageEdit.text()
        if text =='':
            return
        status,msg = self.controller.course_list_change_page(int(text))
        if not status:
            InfoBar.error(
                title='错误',
                content=msg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent()
            )
            return
        self.table.reset()
        self.commandBar.pageEdit.setText(str(self.controller.all_course_curr_page))


    def switchInterface(self, objectName):
        self.stack.setCurrentWidget(self.findChild(QWidget, objectName))
        if objectName == 'select':
            #清空已选时间等信息
            self.addCourseTableCard.model.removeRows(0, self.addCourseTableCard.model.rowCount())
            #self.addCourseTableCard.table.reset()
            self.controller.reset_course_time_list()
