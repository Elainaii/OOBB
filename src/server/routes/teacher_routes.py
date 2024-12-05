from flask import Blueprint, request, jsonify, make_response
import src.server.services as services
from src.server.exceptions import *
from src.server.routes.route_utils import *


'''
教师模块：
1. 查看所教课程列表：返回课程id，课程名，学分，学时，上课时间，上课地点
2. 添加一门课程
3. 查看课程的学生列表：返回学生的id，姓名，成绩,(作业完成情况(学生的每次作业分数总和+分数上限))
4. 添加作业
5. 查看学生作业提交情况：返回学生id，姓名，作业id，作业内容，提交时间，可以在前端进行批改
6. 批改作业：需要提交学生id，作业id，分数
7. 设置学生成绩：需要提交学生id，课程id，分数
'''
teacher_bp = Blueprint('teacher',__name__)

#获取教师所教课程列表，返回课程id，课程名，学分，学时，上课时间，上课地点
@teacher_bp.route('/teacher/<int:tid>/courses', methods=['GET'])
def get_courses(tid):
    pass

#添加一门课程
@teacher_bp.route('/teacher/<int:tid>/courses/add', methods=['POST'])
def add_course(tid):
    pass

#获取某个课程的学生列表，返回学生的id，姓名，成绩,(作业完成情况(学生的每次作业分数总和+分数上限))
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/students', methods=['GET'])
def get_course_students(tid, cid):
    pass

#添加作业
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/homework/add', methods=['POST'])
def add_homework(tid, cid):
    pass

#查看学生作业提交情况，返回学生id，姓名，作业id，作业内容，提交时间，可以在前端进行批改
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/homeworks', methods=['GET'])
def get_homeworks(tid, cid):
    pass

#批改作业，需要提交学生id，作业id，分数
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/homeworks/grade', methods=['POST'])
def set_grade_homework(tid, cid):
    pass

#设置学生成绩，需要提交学生id，课程id，分数
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/student/grade', methods=['GET'])
def set_grade(tid, cid):
    pass

#设置学生奖惩
@teacher_bp.route('/teacher/award', methods=['POST'])
def award():
    pass

