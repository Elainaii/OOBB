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


#获取学生已选择的课程信息,包括课程名，教师名，学分，学时，上课时间，上课地点    注意，这里的课程信息是学生正在上的课程
@student_bp.route('/student/<int:sid>/courses', methods=['GET'])
def get_my_course_info(sid):
    data = services.get_my_course_info(sid)
    return create_response(data, message='success', code=0)

#获取学生课程的成绩，包括课程名，学分，成绩
@student_bp.route('/student/<int:sid>/courses/select', methods=['GET'])
def selected_course(sid):
    data = services.get_selected_course(sid)
    return create_response(data, message='success', code=0)
    pass # TODO

#获取学生所有课程的作业，包括课程名，作业内容，截止时间
@student_bp.route('/student/<int:sid>/courses/homework', methods=['GET'])
def get_homework(sid):
    data = services.get_homework(sid)
    return create_response(data, message='success', code=0)

#提交作业，需要提交作业的课程id，作业id，作业内容
@student_bp.route('/student/<int:sid>/courses/homework/submit', methods=['POST'])
def submit_homework(sid):
    pass # TODO

#获取可以选择的课程列表，包括课程id，院系，课程名，教师名，学分，学时，上课时间，上课地点
@student_bp.route('/student/<int:sid>/courses/info', methods=['GET'])
def get_course_info(sid):
    page_number = request.args.get('page')
    page_size = request.args.get('size')
    if not page_number or not page_size:
        return create_response({}, message='page and size are required,such as /admin/students?size=20&page=0', code=-1)
    page_number = int(page_number)
    page_size = int(page_size)
    data = services.get_course_info(page_number, page_size, sid)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'data': data}
    pass

#学生选课，需要提交课程id
@student_bp.route('/student/<int:sid>/courses/select', methods=['POST'])
def select_course(sid):
    pass

#获取学生的个人信息，包括学号，姓名，性别，年龄，院系，专业，班级
@student_bp.route('/student/<int:sid>/info', methods=['GET'])
def get_student_info(sid):
    data = services.get_student_info(sid)
    return create_response(data, message='success', code=0)

