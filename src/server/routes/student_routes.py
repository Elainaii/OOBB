from flask import Blueprint, request, jsonify, make_response
import src.server.services as services
from src.server.exceptions import *
from src.server.routes.route_utils import *


'''
学生模块：
1. 奖惩：获取学生奖惩信息
2. 查看课程表：获取学生已选择的课程信息,包括课程名，教师名，学分，学时，上课时间，上课地点
3. 成绩单：获取学生课程的成绩，包括课程名，学分，成绩
4. 作业1：获取学生所有课程的作业，包括课程名，作业内容，截止时间
5. 作业2：提交作业，需要提交作业的课程id，作业id，作业内容
6. 选课1：获取可以选择的课程列表，包括课程id，院系，课程名，教师名，学分，学时，上课时间，上课地点
7. 选课2：学生选课，需要提交课程id
'''


student_bp = Blueprint('student', __name__)

#获取学生奖惩信息
@student_bp.route('/student/<int:sid>/awards', methods=['GET'])
def get_awards(sid):
    data = services.get_award(sid)
    return create_response(data, message='success', code=0)


#获取学生已选择的课程信息,包括课程名，教师名，学分，学时，上课时间，上课地点
@student_bp.route('/student/<int:sid>/courses', methods=['GET'])
def get_my_course_info(sid):
    pass # TODO

#获取学生课程的成绩，包括课程名，学分，成绩
@student_bp.route('/student/<int:sid>/courses/select', methods=['POST'])
def selected_course(sid):
    pass # TODO

#获取学生所有课程的作业，包括课程名，作业内容，截止时间
@student_bp.route('/student/<int:sid>/courses/homework', methods=['GET'])
def get_homework(sid):
    pass # TODO

#提交作业，需要提交作业的课程id，作业id，作业内容
@student_bp.route('/student/<int:sid>/courses/homework/submit', methods=['POST'])
def submit_homework(sid):
    pass # TODO

#获取可以选择的课程列表，包括课程id，院系，课程名，教师名，学分，学时，上课时间，上课地点
@student_bp.route('/student/<int:sid>/courses/info', methods=['GET'])
def get_course_info(sid):
    pass

#学生选课，需要提交课程id
@student_bp.route('/student/<int:sid>/courses/select', methods=['POST'])
def select_course(sid):
    pass

#获取学生的个人信息，包括学号，姓名，性别，年龄，院系，专业，班级
@student_bp.route('/student/<int:sid>/info', methods=['GET'])
def get_student_info(sid):
    pass
