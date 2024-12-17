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
                            ComboBox, CheckBox, RadioButton, InfoBar, InfoBarPosition, BreadcrumbBar)

from src.client.core.account import TeacherController



class MyCourseHomeworkCommandBar(CommandBar):
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
        self.pageLabel2.setText("页,共??页")

        self.addWidget(self.pageLabel1)
        self.addWidget(self.pageEdit)
        self.addWidget(self.pageLabel2)
        self.addSeparator()

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)


class MyCourseHomeworkTableView(TableView):
    def __init__(self,controller:TeacherController,parent = None):
        super().__init__(parent)
        self.controller = controller
        controller.get_homework_list()
        self.data = controller.homework_list

        self.model = QStandardItemModel()

        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['student_id'])))
            self.model.setItem(i, 1, QStandardItem(row['student_name']))
            self.model.setItem(i, 2, QStandardItem(row['homework_name']))
            self.model.setItem(i, 3, QStandardItem(row['content']))
            self.model.setItem(i, 4, QStandardItem(str(row['submit_time'])))
            self.model.setItem(i, 5, QStandardItem(str(row['score'])))

        self.model.setHorizontalHeaderLabels(['学生id','姓名', '作业名', '内容','提交时间','分数'])

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
        # self.deleteAction = Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功"))
        self.gradeAction = Action(FluentIcon.EDIT, '设置分数', triggered=lambda: print("查看作业"))
        self.awardAction = Action(FluentIcon.PEOPLE, '设置奖惩', triggered=lambda: print("查看学生"))


    def reset(self):
        self.data = self.controller.homework_list
        self.model.removeRows(0, self.model.rowCount())
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['student_id'])))
            self.model.setItem(i, 1, QStandardItem(row['student_name']))
            self.model.setItem(i, 2, QStandardItem(row['homework_name']))
            self.model.setItem(i, 3, QStandardItem(row['content']))
            self.model.setItem(i, 4, QStandardItem(str(row['submit_time'])))
            self.model.setItem(i, 5, QStandardItem(str(row['score'])))
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
            self.menu.addAction(self.gradeAction)
            self.menu.addAction(self.awardAction)


            #menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        self.menu.exec(QCursor.pos())


class MyCourseStudentCommandBar(CommandBar):
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
        self.pageLabel2.setText("页,共??页")

        self.addWidget(self.pageLabel1)
        self.addWidget(self.pageEdit)
        self.addWidget(self.pageLabel2)
        self.addSeparator()

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)


class MyCourseStudentTableView(TableView):
    def __init__(self,controller:TeacherController,parent = None):
        super().__init__(parent)
        self.controller = controller
        controller.get_course_students()
        self.data = controller.student_list

        self.model = QStandardItemModel()

        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['student_id'])))
            self.model.setItem(i, 1, QStandardItem(row['student_name']))
            self.model.setItem(i, 2, QStandardItem(row['major_name']))
            self.model.setItem(i, 3, QStandardItem(row['dept_name']))
            self.model.setItem(i, 4, QStandardItem(str(row['score'])))

        self.model.setHorizontalHeaderLabels(['学生id','姓名', '专业', '院系','分数'])

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
        # self.deleteAction = Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功"))
        self.gradeAction = Action(FluentIcon.EDIT, '设置分数', triggered=lambda: print("查看作业"))
        self.awardAction = Action(FluentIcon.PEOPLE, '设置奖惩', triggered=lambda: print("查看学生"))


    def reset(self):
        self.data = self.controller.student_list
        self.model.removeRows(0, self.model.rowCount())
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['student_id'])))
            self.model.setItem(i, 1, QStandardItem(row['student_name']))
            self.model.setItem(i, 2, QStandardItem(row['major_name']))
            self.model.setItem(i, 3, QStandardItem(row['dept_name']))
            self.model.setItem(i, 4, QStandardItem(str(row['score'])))
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
            self.menu.addAction(self.gradeAction)
            self.menu.addAction(self.awardAction)


            #menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        self.menu.exec(QCursor.pos())

class MyCourseTableView(TableView):
    def __init__(self,controller:TeacherController,parent = None):
        super().__init__(parent)
        self.controller = controller
        controller.get_course_list()
        self.data = controller.course_list

        self.model = QStandardItemModel()

        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['course_id'])))
            self.model.setItem(i, 1, QStandardItem(row['course_name']))
            self.model.setItem(i, 2, QStandardItem(row['building_name'] + " " + str(row['room_number'])))
            self.model.setItem(i, 3, QStandardItem(str(row['start_week'])))
            self.model.setItem(i, 4, QStandardItem(str(row['end_week'])))
            self.model.setItem(i, 5, QStandardItem(str(row['course_credit'])))
            self.model.setItem(i, 6, QStandardItem(
                str('周' + str(row['course_day']) + ' ' + str(row['course_start_time']) + "-" + str(
                    row['course_end_time']))))

        self.model.setHorizontalHeaderLabels(['课程id','名称', '上课地址', '开始周数','结束周数','学分','时间'])

        self.agentModel = QSortFilterProxyModel()
        self.agentModel.setSourceModel(self.model)
        #self.agentModel.setFilterKeyColumn(-1)
        self.menu = RoundMenu()

        print(self.model.rowCount())
        print(self.model.columnCount())

        self.setModel(self.agentModel)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        #self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.customContextMenuRequested.connect(self.show_rightmenu)

        self.copyAction = Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功"))
        # self.deleteAction = Action(FluentIcon.DELETE, '删除', triggered=lambda: print("删除成功"))
        self.homeworkAction = Action(FluentIcon.EDIT, '查看作业', triggered=lambda: print("查看作业"))
        self.studentAction = Action(FluentIcon.PEOPLE, '查看学生')
        self.infoAction = Action(FluentIcon.LABEL, '修改信息', triggered=lambda: print("修改信息"))


    def reset(self):
        self.data = self.controller.course_list
        self.model.removeRows(0, self.model.rowCount())
        for i, row in enumerate(self.data):
            self.model.setItem(i, 0, QStandardItem(str(row['course_id'])))
            self.model.setItem(i, 1, QStandardItem(row['course_name']))
            self.model.setItem(i, 2, QStandardItem(row['building_name'] + " " + str(row['room_number'])))
            self.model.setItem(i, 3, QStandardItem(str(row['start_week'])))
            self.model.setItem(i, 4, QStandardItem(str(row['end_week'])))
            self.model.setItem(i, 5, QStandardItem(str(row['course_credit'])))
            self.model.setItem(i, 6, QStandardItem(
                str('周' + str(row['course_day']) + ' ' + str(row['course_start_time']) + "-" + str(
                    row['course_end_time']))))
        self.agentModel.setSourceModel(self.model)

    def show_rightmenu(self,pos):
        index = self.indexAt(pos) # 返回点击的index
        if index.isValid(): # 如果有index,则弹出菜单,并且高光选中的行
            self.setCurrentIndex(index)
            self.menu = RoundMenu()
            #self.l.setCurrentIndex(Q)
            # 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标


            self.menu.addAction(self.copyAction)
            self.menu.addAction(self.homeworkAction)
            self.menu.addAction(self.studentAction)
            self.menu.addAction(self.infoAction)




            # 批量添加动作
            # 添加分割线
            # 子菜单

            #menu.addAction(QAction('全选', shortcut='Ctrl+A'))
        self.menu.exec(QCursor.pos())

class MyCourseCommandBar(CommandBar):
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
        self.pageLabel2.setText("页,共??页")

        self.addWidget(self.pageLabel1)
        self.addWidget(self.pageEdit)
        self.addWidget(self.pageLabel2)
        self.addSeparator()

        # self.addSeparator()
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.addWidget(self.search)







class MyCourseInterface(ScrollArea):

    def __init__(self, controller:TeacherController,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)

        #我的课程界面
        self.myCourse = QWidget(self.view)
        self.myCourse.setObjectName("my_course")
        self.myCourseLayout = QVBoxLayout()
        self.commandBar = MyCourseCommandBar(controller,self.view)
        self.table = MyCourseTableView(self.controller,self)
        self.myCourseLayout.addWidget(self.commandBar)
        self.myCourseLayout.addWidget(self.table)
        self.myCourse.setLayout(self.myCourseLayout)

        #学生管理界面
        self.myCourseStudent = QWidget(self.view)
        self.myCourseStudent.setObjectName("student")
        self.myCourseStudentLayout = QVBoxLayout()
        self.commandBarStudent = MyCourseStudentCommandBar(controller,self.view)
        self.tableStudent = MyCourseStudentTableView(controller,self)
        self.myCourseStudentLayout.addWidget(self.commandBarStudent)
        self.myCourseStudentLayout.addWidget(self.tableStudent)
        self.myCourseStudent.setLayout(self.myCourseStudentLayout)

        #作业管理界面
        self.myCourseHomework = QWidget(self.view)
        self.myCourseHomework.setObjectName("homework")
        self.myCourseHomeworkLayout = QVBoxLayout()
        self.commandBarHomework = MyCourseHomeworkCommandBar(controller,self.view)
        self.tableHomework = MyCourseHomeworkTableView(controller,self)
        self.myCourseHomeworkLayout.addWidget(self.commandBarHomework)
        self.myCourseHomeworkLayout.addWidget(self.tableHomework)
        self.myCourseHomework.setLayout(self.myCourseHomeworkLayout)

        self.stack = QStackedWidget(self)

        self.stack.addWidget(self.myCourse)
        self.stack.addWidget(self.myCourseStudent)
        self.stack.addWidget(self.myCourseHomework)


        self.stack.setCurrentWidget(self.myCourse)

        self.breadcrumbBar = BreadcrumbBar(self)#面包屑导航栏
        self.breadcrumbBar.currentItemChanged.connect(self.switchInterface)
        setFont(self.breadcrumbBar, 18)
        self.breadcrumbBar.setSpacing(20)

        self.breadcrumbBar.addItem(self.myCourse.objectName(), "我的课程")
        #self.breadcrumbBar.addItem(self.t.objectName(), "学生管理")




        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("my_course_interface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)

        self.vBoxLayout.addWidget(self.breadcrumbBar, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.stack, 0)

        self.enableTransparentBackground()

        self.bindCourseStudent()
        self.bindCourseHomework()

    def bindCourseStudent(self):
        self.table.studentAction.triggered.connect(self.openCourseStudent)

    def bindCourseHomework(self):
        self.table.homeworkAction.triggered.connect(self.openCourseHomework)

    def switchInterface(self, objectName):
        self.stack.setCurrentWidget(self.findChild(QWidget, objectName))

    def openCourseStudent(self):
        self.stack.setCurrentWidget(self.myCourseStudent)
        self.controller.curr_course_id = self.controller.course_list[self.table.currentIndex().row()]['course_id']
        self.controller.get_course_students()
        self.tableStudent.reset()
        self.breadcrumbBar.addItem(self.myCourseStudent.objectName(), "学生管理")

    def openCourseHomework(self):
        self.stack.setCurrentWidget(self.myCourseHomework)
        self.controller.curr_course_id = self.controller.course_list[self.table.currentIndex().row()]['course_id']
        self.controller.get_homework_list()
        self.tableHomework.reset()
        self.breadcrumbBar.addItem(self.myCourseHomework.objectName(), "作业管理")


