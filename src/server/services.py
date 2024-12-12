#负责对数据库进行操作
from db import *
from exceptions import *
from datetime import datetime

#获取用户信息,用于登录
def get_user(id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM account where id = {id}")
    courses = cursor.fetchone()
    cursor.close()
    return courses

# 获取学生数量
def get_student_num():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT count(*) as num FROM student")
    num = cursor.fetchone()
    cursor.close()
    return num['num']

# 获取学生列表
def get_students(page: int, size: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM student limit {size} offset {page*size}")
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取教师数量
def get_teacher_num():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT count(*) as num FROM teacher")
    num = cursor.fetchone()
    cursor.close()
    return num['num']
# 获取教师列表
def get_teachers(page: int, size: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM teacher limit {size} offset {page*size}")
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取管理员数量
def get_admin_num():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT count(*) as num FROM manager")
    num = cursor.fetchone()
    cursor.close()
    return num['num']

# 获取管理员列表
def get_admins(page: int, size: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM manager limit {size} offset {page*size}")
    courses = cursor.fetchall()
    cursor.close()
    return courses

def get_award(sid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT student.sid as sid, student.student_name as student_name, "
        "award.award_name as award_name, award.award_content as award_content "
        "FROM student, award "
        "WHERE student.sid = %s "
    )
    cursor.execute(sql, (sid, ))
    awards = cursor.fetchall()
    cursor.close()
    return awards

#添加学生,应该由前端检查数据合法性
def add_student(data: dict):
    db = get_db()
    cursor = db.cursor()

    # 检查当前学号是否被占用
    cursor.execute(f"SELECT sid FROM student WHERE sid = {data['sid']}")
    sid = cursor.fetchone()
    if sid:
        raise myException('Student id already exists.')
    # 检查院系是否存在
    cursor.execute(f"SELECT did FROM department WHERE did = {data['did']}")
    did = cursor.fetchone()
    if not did:
        raise myException('Invalid department id.')
    # 检查专业是否存在
    cursor.execute(f"SELECT mid FROM major WHERE mid = {data['mid']}")
    mid = cursor.fetchone()
    if not mid:
        raise myException('Invalid major id.')
    sql = (
        "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(sql, (data['sid'], data['student_name'], data['did'], data['sex'], data['birthday'], data['ID_number'], data['Email'], data['mid']))
    cursor.execute(f"INSERT INTO account VALUES ({data['sid']},'666666','S')")#默认密码为666666
    db.commit()
    cursor.close()

#添加教师,应该由前端检查数据合法性
def add_teacher(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查当前教师号是否被占用
    cursor.execute(f"SELECT tid FROM teacher WHERE tid = {data['tid']}")
    tid = cursor.fetchone()
    if tid:
        raise myException('Teacher id already exists.')
    # 检查院系是否存在
    cursor.execute(f"SELECT did FROM department WHERE did = {data['did']}")
    did = cursor.fetchone()
    if not did:
        raise myException('Invalid department id.')
    sql = (
        "INSERT INTO teacher VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(sql, (data['tid'], data['did'], data['teacher_name'], data['sex'], data['birthday'], data['ID_number'], data['Email']))
    cursor.execute(f"INSERT INTO account VALUES ({data['tid']},'666666','T')")#默认密码为666666
    db.commit()
    cursor.close()

# 添加管理员
def add_admin(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查当前管理员号是否被占用
    cursor.execute(f"SELECT manager_id FROM manager WHERE manager_id = {data['manager_id']}")
    manager_id = cursor.fetchone()
    if manager_id:
        raise myException('Admin id already exists.')
    sql = (
        "INSERT INTO manager VALUES (%s, %s, %s)"
    )
    cursor.execute(sql, (data['manager_id'], data['manager_name'], data['Email']))
    cursor.execute(f"INSERT INTO account VALUES ({data['manager_id']},'666666','A')")#默认密码为666666
    db.commit()
    cursor.close()

# 获取院系信息
def get_dept():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM department")
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取学生信息，包括学号，姓名，性别，年龄，院系，专业
def get_student_info(sid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM student WHERE sid = {sid}")
    student = cursor.fetchone()
    cursor.close()
    return student

# 获取教师所教课程列表，返回课程id，课程名，学分，学时，上课时间，上课地点
def get_courses(tid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT course.cid as course_id, course.course_name as course_name, course.credit as course_credit, "
        "timeslot.day as course_day, timeslot.start_time as course_start_time, timeslot.end_time as course_end_time, "
        "classroom.building_name as building_name, classroom.room_number as room_number, "
        "section.start_week as start_week, section.end_week as end_week "
        "FROM teacher "
        "JOIN teacher_section ON teacher.tid = teacher_section.tid "
        "JOIN section ON teacher_section.sec_id = section.sec_id "
        "JOIN course ON section.cid = course.cid "
        "JOIN timeslot_classroom_section ON section.sec_id = timeslot_classroom_section.sec_id "
        "JOIN timeslot ON timeslot_classroom_section.timeslot_id = timeslot.timeslot_id "
        "JOIN classroom ON timeslot_classroom_section.classroom_id = classroom.classroom_id "
        "WHERE teacher.tid = %s"
    )
    cursor.execute(sql, (tid, ))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取学生已选择的课程信息,包括课程名，教师名，学分，学时，上课时间，上课地点
def get_my_course_info(sid , page: int, size: int, filters: dict):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT course.cid as course_id, course.course_name as course_name, course.credit as course_credit, "
        "timeslot.day as course_day, timeslot.start_time as course_start_time, timeslot.end_time as course_end_time, "
        "classroom.building_name as building_name, classroom.room_number as room_number, "
        "section.start_week as start_week, section.end_week as end_week, teacher.teacher_name as teacher_name "
        "FROM course "
        "JOIN section ON course.cid = section.cid "
        "JOIN timeslot_classroom_section ON section.sec_id = timeslot_classroom_section.sec_id "
        "JOIN timeslot ON timeslot_classroom_section.timeslot_id = timeslot.timeslot_id "
        "JOIN classroom ON timeslot_classroom_section.classroom_id = classroom.classroom_id "
        "JOIN teacher_section ON section.sec_id = teacher_section.sec_id "
        "JOIN teacher ON teacher_section.tid = teacher.tid "
        "JOIN student_section ON section.sec_id = student_section.sec_id "
        "WHERE student_section.sid = %s "
    )
    params = [sid]
    # 先获取总数
    cursor.execute(sql, (sid, ))
    num = cursor.fetchall()
    # 获取总数
    num = len(num)
    # 通过学期号过滤
    f1 = filters.get('semester_id')
    if f1:
        sql += "AND section.semester_id = %s "
        params.append(f1)
    # 通过课程状态过滤
    f2 = filters.get('status')
    if f2 is not None:
        if f2 == 0:
            # 全部
            pass
        elif f2 == 1:
            # 正在进行
            sql += "AND student_section.score IS NULL "
        elif f2 == 2:
            # 已通过
            sql += "AND student_section.score >= 60 "
        elif f2 == 3:
            sql += "AND student_section.score < 60 "
    # 通过课程名过滤
    f3 = filters.get('course_name')
    if f3:
        sql += f"AND course.course_name LIKE %s "
        params.append(f"%{f3}%")
    # 分页
    sql += f"limit %s offset %s"
    params.extend([size, page*size])
    # 获取课程信息
    cursor.execute(sql, params)
    courses = cursor.fetchall()
    cursor.close()
    return courses, num

# 获取可以选择的课程列表，包括课程id，院系，课程名，教师名，学分，学时，上课时间，上课地点
# 返回可选课程列表以及总数
def get_course_info(page: int, size: int, sid: int):
    # 能选的课程是先修课及格的课程或者没有先修课的课程、而且是当前学期开的课程
    # 并且人数不超过上限
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # 先获取当前学期，当前学期是已有的学期中最大的
    cursor.execute("SELECT max(semester_id) as semester_id FROM semester")
    semester = cursor.fetchone() # 只选择这个学期的课程

    sql1 = (
        "WITH course1 AS (" # course1 是没有先修课的课程：所有课程减去有先修课的课程
        "   (SELECT cid "
        "   FROM course) "
        "   EXCEPT "
        "   (SELECT DISTINCT cid "
        "   FROM pre_course) "
        "), course2 AS (" # course2 是已经选过的课程，并且有成绩的课程 TODO：需不需要考虑及格？
        "   SELECT DISTINCT cid "
        "   FROM section, student_section "
        "   WHERE student_section.sid = %s " # 学生id
        "   AND student_section.sec_id = section.sec_id " # 学生选的课
        "   AND student_section.score IS NOT NULL" # 有成绩
        "), course3 AS ("
        "   SELECT cid "
        "   FROM course "
        "   WHERE cid IN (SELECT cid FROM course1) "
        "   OR cid IN ("
        "   SELECT distinct cid "
        "   FROM pre_course "
        "   WHERE pre_cid IN (SELECT cid FROM course2) "
        "   ) "
        ") " # course3 是可以选的课程，接下来找出这些课程的信息，必须满足：剩余人数大于0，当前学期开课
        "SELECT course.cid as course_id, course.course_name as course_name, department.dept_name as department_name, "
        "teacher.teacher_name as teacher_name, course.credit as course_credit, classroom.building_name as building_name, classroom.room_number as room_number, "
        "timeslot.day as course_day, timeslot.start_time as course_start_time, timeslot.end_time as course_end_time "
        "FROM course3 "
        "JOIN course ON course3.cid = course.cid "
        "JOIN section ON course.cid = section.cid "
        "JOIN timeslot_classroom_section ON section.sec_id = timeslot_classroom_section.sec_id "
        "JOIN classroom ON timeslot_classroom_section.classroom_id = classroom.classroom_id "
        "JOIN timeslot ON timeslot_classroom_section.timeslot_id = timeslot.timeslot_id "
        "JOIN teacher_section ON section.sec_id = teacher_section.sec_id "
        "JOIN teacher ON teacher_section.tid = teacher.tid "
        "JOIN department ON course.did = department.did "
        "WHERE section.rest_number > 0 "
        "AND section.semester_id = %s"
    )
    cursor.execute(sql1, (sid, semester['semester_id']))
    courses = cursor.fetchall()
    cursor.close()
    return courses, len(courses)

# 获取学生课程的成绩，包括课程名，学分，成绩
def get_selected_course(sid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT course.cid as course_id, course.course_name as course_name, course.credit as course_credit, "
        "student_section.score as score "
        "FROM course, student_section, section "
        "WHERE student_section.sid = %s "
        "AND student_section.sec_id = section.sec_id "
        "AND course.cid = section.cid "
    )
    cursor.execute(sql, (sid, ))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取学生所有课程的作业，包括课程名，作业内容，截止时间
def get_homework(sid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT course.cid as course_id, course.course_name as course_name, "
        "homework.homework_name as homework_name, homework.content as homework_content, homework.deadline as deadline "
        "FROM course, section, homework, student_section "
        "WHERE student_section.sid = %s "
        "AND student_section.sec_id = section.sec_id "
        "AND course.cid = section.cid "
        "AND homework.sec_id = section.sec_id "
    )
    cursor.execute(sql, (sid, ))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取某个课程的学生列表，返回学生的id，姓名
def get_course_students(tid, cid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT student.sid as student_id, student.student_name as student_name "
        "FROM student "
        "JOIN student_section ON student.sid = student_section.sid "
        "JOIN section ON student_section.sec_id = section.sec_id "
        "JOIN teacher_section ON section.sec_id = teacher_section.sec_id "
        "where teacher_section.tid = %s and section.cid = %s"
    )
    cursor.execute(sql, (tid, cid))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取学生作业提交情况，返回学生id，姓名，作业id，作业内容，提交时间，可以在前端进行批改
def get_homeworks(tid, cid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT student.sid as student_id, student.student_name as student_name, "
        "homework_collection.homework_name as homework_name, "
        "homework_collection.content as content, "
        "homework_collection.submit_time as submit_time "
        "FROM student "
        "JOIN homework_collection ON student.sid = homework_collection.sid "
        "JOIN section ON homework_collection.sec_id = section.sec_id "
        "JOIN teacher_section ON section.sec_id = teacher_section.sec_id "
        "where teacher_section.tid = %s and section.cid = %s"
    )
    cursor.execute(sql, (tid, cid))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 学生选课，需要提交课程id
def select_course(sid, sec_id):
    db = get_db()
    cursor = db.cursor()
    # 由于前端已经获得了能够选的课程，所以这里不需要再次检查
    # student_section
    cursor.execute(f"INSERT INTO student_section VALUES ({sid}, {sec_id}, NULL)")
    # section
    cursor.execute(f"UPDATE section SET rest_number = rest_number - 1 WHERE sec_id = {sec_id}")
    db.commit()
    cursor.close()

# 提交作业，需要提交作业的课程id，作业id，作业内容
def submit_homework(sid, data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查是否已经提交过，如果提交过则覆盖
    cursor.execute(f"SELECT * FROM homework_collection WHERE sid = {sid} AND sec_id = {data['sec_id']} AND homework_name = '{data['homework_name']}'")
    homework = cursor.fetchone()
    # 获取当前时间
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if homework:
        cursor.execute(f"UPDATE homework_collection SET content = '{data['homework_content']}' WHERE sid = {sid} AND sec_id = {data['sec_id']} AND homework_name = '{data['homework_name']}'")
        db.commit()
        cursor.close()
        return
    # homework_collection
    sql = {
        "INSERT INTO homework_collection VALUES (%s, %s, %s, %s, %s)"
    }

    cursor.execute(sql, (sid, data['sec_id'], data['homework_name'], data['homework_content'], now))

    db.commit()
    cursor.close()

# 修改学生信息，需要提交学生id，修改后的信息，不修改的保持原状
def change_student(data: dict):
    db = get_db()
    cursor = db.cursor()

    db.commit()
    cursor.close()

# 修改教师信息，需要提交教师id，修改后的信息，不修改保持原状
def change_teacher(data: dict):
    db = get_db()
    cursor = db.cursor()

    db.commit()
    cursor.close()

# 修改管理员信息，需要提交管理员id，修改后的信息，不修改保持原状

def change_admin(data: dict):
    db = get_db()
    cursor = db.cursor()

    db.commit()
    cursor.close()

# 获取学期信息
def get_semester(page: int, size: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # 获取学期总数
    cursor.execute("SELECT count(*) as num FROM semester")
    num = cursor.fetchone()
    # 获取学期信息，降序
    cursor.execute(f"SELECT * FROM semester ORDER BY semester_id DESC limit {size} offset {page*size}")
    courses = cursor.fetchall()
    cursor.close()
    return courses, num['num']