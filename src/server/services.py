#负责对数据库进行操作
from db import *
from exceptions import *

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
    cursor.execute(f"SELECT did FROM department WHERE did = {data['department']}")
    did = cursor.fetchone()
    if not did:
        raise myException('Invalid department id.')
    cursor.execute(f"INSERT INTO student VALUES ({data['sid']},'{data['name']}',{did},'{data['sex']}','{data['birthday']}','{data['id_number']}','{data['email']}')")
    cursor.execute(f"INSERT INTO account VALUES ({data['sid']},'{data['id_number']}','S')")#默认密码为666666
    db.commit()
    cursor.close()

#添加教师,应该由前端检查数据合法性
def add_teacher(data: dict):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT did FROM department WHERE did = {data['department']}")
    did = cursor.fetchone()
    if not did:
        raise myException('Invalid department id.')
    cursor.execute(f"INSERT INTO teacher VALUES ({data['tid']},'{data['name']}',{did},'{data['sex']}','{data['birthday']}','{data['id_number']}','{data['email']}',{data['is_admin']})")
    cursor.execute(f"INSERT INTO account VALUES ({data['tid']},'{data['id_number']}','T')")#默认密码为666666
    db.commit()
    cursor.close()

def get_dept():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM department")
    courses = cursor.fetchall()
    cursor.close()
    return courses

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
        "FROM section, classroom, timeslot, teacher, course, timeslot_classroom_section, teacher_section "
        "WHERE teacher.tid = %s "
        "AND teacher_section.tid = teacher.tid "
        "AND teacher_section.sec_id = section.sec_id "
        "AND course.cid = section.cid "
        "AND timeslot_classroom_section.sec_id = section.sec_id "
        "AND timeslot_classroom_section.classroom_id = classroom.classroom_id "
        "AND timeslot_classroom_section.timeslot_id = timeslot.timeslot_id "
    )
    cursor.execute(sql, (tid, ))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取学生已选择的课程信息,包括课程名，教师名，学分，学时，上课时间，上课地点
def get_my_course_info(sid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT course.cid as course_id, course.course_name as course_name, course.credit as course_credit, "
        "timeslot.day as course_day, timeslot.start_time as course_start_time, timeslot.end_time as course_end_time, "
        "classroom.building_name as building_name, classroom.room_number as room_number, "
        "section.start_week as start_week, section.end_week as end_week, teacher.teacher_name as teacher_name "
        "FROM section, classroom, timeslot, student, course, timeslot_classroom_section, student_section, teacher, teacher_section "
        "WHERE student.sid = %s "
        "AND student_section.sid = student.sid "
        "AND student_section.sec_id = section.sec_id "
        "AND course.cid = section.cid "
        "AND timeslot_classroom_section.sec_id = section.sec_id "
        "AND timeslot_classroom_section.classroom_id = classroom.classroom_id "
        "AND timeslot_classroom_section.timeslot_id = timeslot.timeslot_id "
        "AND teacher.tid = teacher_section.tid "
        "AND teacher_section.sec_id = section.sec_id "
    )
    cursor.execute(sql, (sid, ))
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取可以选择的课程列表，包括课程id，院系，课程名，教师名，学分，学时，上课时间，上课地点
def get_course_info(page: int, size: int, sid: int):
    # 能选的课程是未选过的课程、并且先修课及格的课程、而且是当前学期开的课程
    # 或者是已经选过的课程，但是是重修的课程
    # 先获取当前学期，当前学期是已有的学期中最大的
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT max(semester_id) as semester_id FROM semester")
    semester = cursor.fetchone()

    sql = (
        "SELECT course.cid as course_id, department.department_name as department_name, course.course_name as course_name, "
        "teacher.teacher_name as teacher_name, course.credit as course_credit, course.hours as course_hours, "
        "timeslot.day as course_day, timeslot.start_time as course_start_time, timeslot.end_time as course_end_time, "
        "classroom.building_name as building_name, classroom.room_number as room_number "
        "FROM course, department, teacher, section, classroom, timeslot, timeslot_classroom_section "
        "WHERE course.did = department.did "
        "AND course.cid = section.cid "
        "AND section.sec_id = timeslot_classroom_section.sec_id "
        "AND timeslot_classroom_section.classroom_id = classroom.classroom_id "
        "AND timeslot_classroom_section.timeslot_id = timeslot.timeslot_id "
        "AND section.sec_id NOT IN (SELECT sec_id FROM student_section WHERE sid = %s) "
        "AND teacher.tid = section.tid "
        "LIMIT %s OFFSET %s "
    )
    cursor.execute(sql, (sid, size, page*size))
    courses = cursor.fetchall()
    cursor.close()
    return courses

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

'''
TODO:

# 修改学生信息，需要提交学生id，修改后的信息，不修改的保持原状
def change_student(data: dict):
    db = get_db()
    cursor = db.cursor()
    # json数据中的key必须和数据库中的字段名一致
    # 先从json中提取出sid
    sid = data['sid']
    # 查找数据库中是否有这个学生
    cursor.execute(f"SELECT * FROM student WHERE sid = {sid}")
    student = cursor.fetchone()
    if not student:
        raise myException('Invalid student id.')
    # 从json中提取出的key和value
    for key, value in data.items():
        if value == '':
            continue
        if key == 'sid':
            continue
        # 如果key是department，需要检查value是否是合法的did
        if key == 'department':
            cursor.execute(f"SELECT did FROM department WHERE did = {value}")
            did = cursor.fetchone()
            if not did:
                raise myException('Invalid department id.')
        # 如果key是mid，需要检查value是否是合法的mid
        elif key == 'mid':
            cursor.execute(f"SELECT mid FROM major WHERE mid = {value}")
            mid = cursor.fetchone()
            if not mid:
                raise myException('Invalid major id.')
        # 如果key是sex，需要检查value是否是合法的性别，性别只能是M或F，没有其他性别，也不可能有其他性别
        elif key == 'sex':
            if value not in ['M', 'F']:
                raise myException('Invalid sex.')
        # 如果key是birthday，需要检查value是否是合法的日期

        # 如果value不为空，则更新数据库中的字段

        cursor.execute(f"UPDATE student SET {key} = '{value}' WHERE sid = {sid}")

    db.commit()
    cursor.close()

'''