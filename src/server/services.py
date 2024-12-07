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
    cursor.execute(f"SELECT * FROM award WHERE sid = {sid}")
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
    cursor.execute(f"INSERT INTO account VALUES ({data['sid']},'{data['id_number']}','S')")#默认密码为身份证号
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
    cursor.execute(f"INSERT INTO account VALUES ({data['tid']},'{data['id_number']}','T')")#默认密码为身份证号
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