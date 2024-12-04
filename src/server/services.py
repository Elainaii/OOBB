#负责对数据库进行操作
from db import *


def get_students():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    courses = cursor.fetchall()
    cursor.close()
    return courses
