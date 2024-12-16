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
    cursor.execute(f"SELECT * FROM student NATURAL JOIN department NATURAL JOIN major limit {size} offset {page*size}")
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
    cursor.execute(f"SELECT * FROM teacher NATURAL JOIN department limit {size} offset {page*size}")
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

def get_major():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM major")
    courses = cursor.fetchall()
    cursor.close()
    return courses

# 获取学生信息，包括学号，姓名，性别，年龄，院系，专业
# 还要返回总学分和平均分（平均分只用算已通过的课程、并且不用加权）
def get_student_info(sid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        # 总学分：已通过的课程的学分之和，需要排除重复的课程
        # 平均分：已经选择过的课程的平均分，需要排除重复的课程，每门课取最高分
        # 先得到每门课的最高分
        # 然后根据最高分和学分计算总学分以及平均分
        "WITH max_score AS ( "
        "   SELECT max(student_section.score) as score, course.credit as credit "
        "    FROM student_section "
        "    JOIN section ON student_section.sec_id = section.sec_id "
        "    JOIN course ON section.cid = course.cid "
        "    WHERE student_section.sid = %s "
        "    AND student_section.score IS NOT NULL "
        "    GROUP BY course.cid "
        "), total_credit AS ( "
        "    SELECT sum(credit) as total_credit "
        "    FROM max_score "
        "    WHERE score >= 60 "
        "), avg_score AS ( "
        "   SELECT avg(score) as avg_score "
        "   FROM max_score "
        ") "
        "SELECT student.sid as student_id, student.student_name as student_name, "
        "student.sex as student_sex, student.birthday as student_birthday, "
        "department.dept_name as department_name, major.major_name as major_name, "
        "total_credit.total_credit as total_credit, avg_score.avg_score as avg_score "
        "FROM student "
        "JOIN department ON student.did = department.did "
        "JOIN major ON student.mid = major.mid "
        "JOIN total_credit ON true "
        "JOIN avg_score ON true "
        "WHERE student.sid = %s "
    )
    cursor.execute(sql, (sid, sid))
    student = cursor.fetchone()
    cursor.close()
    return student

# 获取教师所教课程列表，返回课程id，课程名，学分，学时，上课时间，上课地点
def get_courses(tid, page: int, size: int, filters: dict):
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
        "WHERE teacher.tid = %s "
    )
    params = [tid]

    # 根据学期号过滤
    f1 = filters.get('semester_id')
    if f1:
        sql += "AND section.semester_id = %s "
        params.append(f1)
    # 根据课程名过滤
    f2 = filters.get('course_name')
    if f2:
        sql += "AND course.course_name LIKE %s "
        params.append(f"%{f2}%")
    # 先获取总数
    cursor.execute(sql, params)
    num = cursor.fetchall()
    # 分页
    sql += f"limit %s offset %s"
    params.extend([size, page*size])
    # 获取课程信息
    cursor.execute(sql, params)
    courses = cursor.fetchall()
    cursor.close()
    return courses, len(num)

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
    # 先获取总数
    cursor.execute(sql, (sid, ))
    num = cursor.fetchall()
    # 获取总数
    num = len(num)
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
def get_homework(sid, page: int, size: int):
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
    # 先获取总数
    cursor.execute(sql, (sid, ))
    num = cursor.fetchall()
    # 分页
    sql += f"limit %s offset %s"
    cursor.execute(sql, (sid, size, page*size))
    courses = cursor.fetchall()
    cursor.close()
    return courses, len(num)

# 获取某个课程的学生列表，返回学生的id，姓名
def get_course_students(tid, cid, page: int, size: int, filters: dict):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = (
        "SELECT student.sid as student_id, student.student_name as student_name "
        "FROM student "
        "JOIN student_section ON student.sid = student_section.sid "
        "JOIN section ON student_section.sec_id = section.sec_id "
        "JOIN teacher_section ON section.sec_id = teacher_section.sec_id "
        "where teacher_section.tid = %s and section.cid = %s "
    )
    params = [tid, cid]
    # 根据学期号过滤
    f1 = filters.get('semester_id')
    if f1:
        sql += "AND section.semester_id = %s "
        params.append(f1)
    # 先获取总数
    cursor.execute(sql, params)
    num = cursor.fetchall()
    # 分页
    sql += f"limit %s offset %s"
    params.extend([size, page*size])
    # 获取学生信息
    cursor.execute(sql, params)
    courses = cursor.fetchall()
    cursor.close()
    return courses, len(num)

# 获取学生作业提交情况，返回学生id，姓名，作业id，作业内容，提交时间，可以在前端进行批改
def get_homeworks(tid, cid, page: int, size: int, filters: dict):
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
        "where teacher_section.tid = %s and section.cid = %s "
    )
    params = [tid, cid]
    # 根据学期号过滤
    f1 = filters.get('semester_id')
    if f1:
        sql += "AND section.semester_id = %s "
        params.append(f1)
    # 根据学生姓名过滤
    f2 = filters.get('student_name')
    if f2:
        sql += "AND student.student_name LIKE %s "
        params.append(f"%{f2}%")
    # 根据是否批改过过滤
    f3 = filters.get('status')
    if f3 is not None:
        if f3 == 0:
            # 全部
            pass
        elif f3 == 1:
            # 未批改
            sql += "AND homework_collection.score IS NULL "
        elif f3 == 2:
            # 已批改
            sql += "AND homework_collection.score IS NOT NULL "
    # 先获取总数
    cursor.execute(sql, params)
    num = cursor.fetchall()
    # 分页
    sql += f"limit %s offset %s"
    params.extend([size, page*size])
    # 获取学生信息
    cursor.execute(sql, params)
    courses = cursor.fetchall()
    cursor.close()
    return courses, len(num)

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
    # 检查学生是否存在
    cursor.execute("SELECT sid FROM student WHERE sid = %s", (data['sid'],))
    sid = cursor.fetchone()
    if not sid:
        raise myException('Student id does not exist.')
    # 根据传入的信息修改学生信息，不修改的保持原状，但是要检查
    # 姓名
    if 'student_name' in data and data['student_name']:
        cursor.execute("UPDATE student SET student_name = %s WHERE sid = %s", (data['student_name'], data['sid']))
    # 院系
    if 'did' in data and data['did']:
        # 检查院系是否存在
        cursor.execute("SELECT did FROM department WHERE did = %s", (data['did'],))
        did = cursor.fetchone()
        if not did:
            raise myException('Invalid department id.')
        cursor.execute("UPDATE student SET did = %s WHERE sid = %s", (data['did'], data['sid']))
    # 性别
    if 'sex' in data and data['sex']:
        cursor.execute("UPDATE student SET sex = %s WHERE sid = %s", (data['sex'], data['sid']))
    # 生日
    if 'birthday' in data and data['birthday']:
        cursor.execute("UPDATE student SET birthday = %s WHERE sid = %s", (data['birthday'], data['sid']))
    # 身份证号
    if 'ID_number' in data and data['ID_number']:
        cursor.execute("UPDATE student SET ID_number = %s WHERE sid = %s", (data['ID_number'], data['sid']))
    # 邮箱
    if 'Email' in data and data['Email']:
        cursor.execute("UPDATE student SET Email = %s WHERE sid = %s", (data['Email'], data['sid']))
    # 专业
    if 'mid' in data and data['mid']:
        # 检查专业是否存在
        cursor.execute("SELECT mid FROM major WHERE mid = %s", (data['mid'],))
        mid = cursor.fetchone()
        if not mid:
            raise myException('Invalid major id.')
        cursor.execute("UPDATE student SET mid = %s WHERE sid = %s", (data['mid'], data['sid']))
    db.commit()
    cursor.close()

# 修改教师信息，需要提交教师id，修改后的信息，不修改保持原状
def change_teacher(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查教师是否存在
    cursor.execute("SELECT tid FROM teacher WHERE tid = %s", (data['tid'],))
    tid = cursor.fetchone()
    if not tid:
        raise myException('Teacher id does not exist.')
    # 根据传入的信息修改教师信息，不修改的保持原状，但是要检查
    # 姓名
    if 'teacher_name' in data and data['teacher_name']:
        cursor.execute("UPDATE teacher SET teacher_name = %s WHERE tid = %s", (data['teacher_name'], data['tid']))
    # 院系
    if 'did' in data and data['did']:
        # 检查院系是否存在
        cursor.execute("SELECT did FROM department WHERE did = %s", (data['did'],))
        did = cursor.fetchone()
        if not did:
            raise myException('Invalid department id.')
        cursor.execute("UPDATE teacher SET did = %s WHERE tid = %s", (data['did'], data['tid']))
    # 性别
    if 'sex' in data and data['sex']:
        cursor.execute("UPDATE teacher SET sex = %s WHERE tid = %s", (data['sex'], data['tid']))
    # 生日
    if 'birthday' in data and data['birthday']:
        cursor.execute("UPDATE teacher SET birthday = %s WHERE tid = %s", (data['birthday'], data['tid']))
    # 身份证号
    if 'ID_number' in data and data['ID_number']:
        cursor.execute("UPDATE teacher SET ID_number = %s WHERE tid = %s", (data['ID_number'], data['tid']))
    # 邮箱
    if 'Email' in data and data['Email']:
        cursor.execute("UPDATE teacher SET Email = %s WHERE tid = %s", (data['Email'], data['tid']))
    db.commit()
    cursor.close()

# 修改管理员信息，需要提交管理员id，修改后的信息，不修改保持原状

def change_admin(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查管理员是否存在
    cursor.execute("SELECT manager_id FROM manager WHERE manager_id = %s", (data['manager_id'],))
    manager_id = cursor.fetchone()
    if not manager_id:
        raise myException('Admin id does not exist.')
    # 根据传入的信息修改管理员信息，不修改的保持原状，但是要检查
    # 姓名
    if 'manager_name' in data and data['manager_name']:
        cursor.execute("UPDATE manager SET manager_name = %s WHERE manager_id = %s", (data['manager_name'], data['manager_id']))
    # 邮箱
    if 'Email' in data and data['Email']:
        cursor.execute("UPDATE manager SET Email = %s WHERE manager_id = %s", (data['Email'], data['manager_id']))

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

# 添加院系
def add_department(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查院系是否存在
    cursor.execute("SELECT did FROM department WHERE did = %s", (data['did'],))
    did = cursor.fetchone()
    if did:
        raise myException('Department id already exists.')
    # 添加院系
    cursor.execute("INSERT INTO department VALUES (%s, %s)", (data['did'], data['dept_name']))
    db.commit()
    cursor.close()

# 添加新的学期
def add_semester():
    db = get_db()
    cursor = db.cursor()

    seasons = ['春', '夏', '秋', '冬']

    # 添加学期
    # 获取当前最大学期号，然后加1
    cursor.execute("SELECT max(semester_id) as semester_id FROM semester")
    semester = cursor.fetchone()
    semester_id = semester['semester_id'] + 1
    # 获取要添加的学期的年份
    # 先看最新一个学期的年份，再看季节，如果是冬季则年份加1，否则不变
    cursor.execute("SELECT year, season FROM semester WHERE semester_id = %s", (semester['semester_id'],))
    year_season = cursor.fetchone()
    year = year_season['year']
    season = year_season['season']
    i = 0
    if season == '冬':
        year += 1
        i = 0
    elif season == '春':
        i = 1
    elif season == '夏':
        i = 2
    elif season == '秋':
        i = 3
    # 添加新的学期
    cursor.execute("INSERT INTO semester VALUES (%s, %s, %s)", (semester_id, year, seasons[i]))
    db.commit()
    cursor.close()

# 设置奖惩
def award(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查学生是否存在
    cursor.execute("SELECT sid FROM student WHERE sid = %s", (data['sid'],))
    sid = cursor.fetchone()
    if not sid:
        raise myException('Student id does not exist.')
    # 添加奖惩
    cursor.execute("INSERT INTO award VALUES (%s, %s, %s)", (data['sid'], data['award_name'], data['award_content']))
    db.commit()
    cursor.close()

# 设置学生作业成绩（批改作业）， 需要提交学生id，课程id(sec_id)，作业名，成绩
def set_grade_homework(data:dict):
    db = get_db()
    cursor = db.cursor()
    # 批改作业的前提是能通过上面的找到作业，前端能够返回所有正确的值
    # 检查是否已经批改过，如果批改过则覆盖(其实不检查也可以，直接update)
    sql1 = (
        "UPDATE homework_collection "
        "SET score = %s "
        "WHERE sid = %s "
        "AND sec_id = %s "
        "AND homework_name = %s"
    )
    params = [data['score'], data['sid'], data['sec_id'], data['homework_name']]
    cursor.execute(sql1, params)
    db.commit()
    cursor.close()

# 添加作业
def add_homework(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 添加作业
    cursor.execute("INSERT INTO homework VALUES (%s, %s, %s, %s)", (data['sec_id'], data['homework_name'], data['homework_content'], data['deadline']))
    db.commit()
    cursor.close()

# 设置学生成绩，需要提交学生id，课程id，成绩
def set_grade(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 设置成绩
    cursor.execute("UPDATE student_section SET score = %s WHERE sid = %s AND sec_id = %s", (data['score'], data['sid'], data['sec_id']))
    db.commit()
    cursor.close()

# 添加课程：从已经存在的课程中选择，需要提交课程id，教师id，学期id
# 前端传入的参数：课程id cid, 学期id semester_id， 想要选择的教室id classroom_id， 想要选择的时间段 time_slot_id  还有sec_id  最大人数
def add_course(tid, data: dict):
    db = get_db()
    cursor = db.cursor()

    try:
        # 检查时间和教室是否冲突
        semester_id = data['semester_id']
        timeslot_id = data['timeslot_id']
        classroom_id = data['classroom_id']

        sql0 = (
            "SELECT section.sec_id "
            "FROM section "
            "JOIN timeslot_classroom_section ON section.sec_id = timeslot_classroom_section.sec_id "
            "WHERE section.semester_id = %s AND timeslot_classroom_section.timeslot_id = %s AND timeslot_classroom_section.classroom_id = %s"
        )
        cursor.execute(sql0, (semester_id, timeslot_id, classroom_id))
        timeslot_classroom_section = cursor.fetchone()
        if timeslot_classroom_section:
            raise myException('Time and classroom conflict.')

        # 检查是否已经存在sec_id
        sql1 = "SELECT sec_id FROM section WHERE sec_id = %s"
        cursor.execute(sql1, (data['sec_id'],))
        sec_id = cursor.fetchone()

        if sec_id is None:
            # 插入新的section
            sql2 = (
                "INSERT INTO section (sec_id, cid, start_week, end_week, max_students, semester_id, rest_number) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql2, (
            data['sec_id'], data['cid'], data['start_week'], data['end_week'], data['max_number'], data['semester_id'],
            data['max_number']))

            # 提交事务以使插入的sec_id可见
            db.commit()

            # 插入新的teacher_section
            sql3 = (
                "INSERT INTO teacher_section (tid, sec_id) "
                "VALUES (%s, %s)"
            )
            cursor.execute(sql3, (tid, data['sec_id']))

        # 提交事务以使插入的teacher_section可见
        db.commit()

        # 插入timeslot_classroom_section
        sql4 = (
            "INSERT INTO timeslot_classroom_section (timeslot_id, classroom_id, sec_id) "
            "VALUES (%s, %s, %s)"
        )
        cursor.execute(sql4, (timeslot_id, classroom_id, data['sec_id']))

        # 提交事务
        db.commit()
    except Exception as e:
        # 出现异常时回滚事务
        db.rollback()
        raise e
    finally:
        cursor.close()

# 开一门新课
def new_course(data:dict):
    db = get_db()
    cursor = db.cursor()
    # 检查课程是否存在，不允许同名课程存在
    cursor.execute("SELECT cid FROM course WHERE course_name = %s", (data['course_name'],))
    course = cursor.fetchone()
    if course:
        raise myException('Course already exists.')
    # 直接插入新的课程
    sql = (
        "INSERT INTO course(cid, course_name, did, credit) VALUES(%s, %s, %s, %s)"
    )
    cursor.execute(sql, (data['cid'], data['course_name'], data['did'], data['credit']))
    db.commit()
    cursor.close()

# 修改密码
def change_password(account_id, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE account SET password = %s WHERE account_id = %s", (password, account_id))
    db.commit()
    cursor.close()

# 修改院系名字
def change_department(data: dict):
    db = get_db()
    cursor = db.cursor()
    # 检查院系是否存在
    cursor.execute("SELECT did FROM department WHERE did = %s", (data['did'],))
    did = cursor.fetchone()
    if not did:
        raise myException('Department id does not exist.')
    # 修改院系名字
    cursor.execute("UPDATE department SET dept_name = %s WHERE did = %s", (data['dept_name'], data['did']))
    db.commit()
    cursor.close()