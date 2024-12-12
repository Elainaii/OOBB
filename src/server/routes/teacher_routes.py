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
# TODO： 增加对学期的过滤条件、支持搜索课程名字 返回课程信息、分页
@teacher_bp.route('/teacher/<int:tid>/courses', methods=['GET'])
def get_courses(tid):
    data = services.get_courses(tid)
    return create_response(data, message='success', code=0)


#添加一门课程    ：在已经存在的课程中选择一个在这个学期开课
# TODO：   判断是否会冲突（时间冲突、教室冲突）
@teacher_bp.route('/teacher/<int:tid>/courses/add', methods=['POST'])
def add_course(tid):
    pass

#获取某个课程的学生列表，返回学生的id，姓名
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/students', methods=['GET'])
def get_course_students(tid, cid):
    data = services.get_course_students(tid, cid)
    return create_response(data, message='success', code=0)

#添加作业
# TODO： 先找本学期的课程，再对某个课程添加作业
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/homework/add', methods=['POST'])
def add_homework(tid, cid):
    pass

# TODO： 先找到本学期教的课程，看某个课程对应的作业的提交情况 搜索学生名字 过滤 是否批改/all   -》批改
#查看学生作业提交情况，返回学生id，姓名，作业id，作业内容，提交时间，可以在前端进行批改
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/homeworks', methods=['GET'])
def get_homeworks(tid, cid):
    data = services.get_homeworks(tid, cid)
    return create_response(data, message='success', code=0)

# TODO：批改作业，需要提交学生id，作业id，分数
#批改作业，需要提交学生id，作业id，分数,应该是一个列表，包含多个学生的作业分数
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/homeworks/grade', methods=['POST'])
def set_grade_homework(tid, cid):
    pass

#设置学生成绩，需要提交学生id，课程id，分数
# TODO： 先找到本学期教的课程，再对某个课程的某个学生设置成绩
@teacher_bp.route('/teacher/<int:tid>/courses/<int:cid>/student/grade', methods=['GET'])
def set_grade(tid, cid):
    pass

#设置学生奖惩
@teacher_bp.route('/teacher/award', methods=['POST'])
def award():
    pass


# TODO：开一门全新的课程