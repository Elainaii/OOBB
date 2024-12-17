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

# 获取教师所教课程列表，返回课程id，课程名，学分，学时，上课时间，上课地点
# 可以使用学期筛选
@teacher_bp.route('/teacher/<int:tid>/courses', methods=['GET'])
def get_courses(tid):
    semester_id = request.args.get('semester_id')
    course_name = request.args.get('course_name')
    page_size = request.args.get('size')
    page_number = request.args.get('page')
    if not page_size or not page_number:
        return create_response({}, message='page and size are required,such as /teacher/201011919/courses?size=20&page=0', code=-1)
    filters = {
        'semester_id': semester_id,
        'course_name': course_name
    }
    page_size = int(page_size)
    page_number = int(page_number)
    data, num = services.get_courses(tid, page_number, page_size, filters)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

#添加一门课程    ：在已经存在的课程中选择一个在这个学期开课
@teacher_bp.route('/teacher/<int:tid>/courses/add', methods=['POST'])
def add_course(tid):
    # 前端传入的参数：课程id cid, 学期id semester_id， 想要选择的教室id classroom_id， 想要选择的时间段 time_slot_id 还有sec_id
    data = request.json
    try:
        services.add_course(tid, data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#获取某个课程的学生列表，返回学生的id，姓名
@teacher_bp.route('/teacher/<int:tid>/courses/<int:sec_id>/students', methods=['GET'])
def get_course_students(tid, sec_id):
    # 增加对学期的筛选
    semester_id = request.args.get('semester_id')
    # 分页
    page_size = request.args.get('size')
    page_number = request.args.get('page')
    if(not page_size or not page_number):
        return create_response({}, message='page and size are required,such as /teacher/201011919/courses/1/students?size=20&page=0', code=-1)
    page_size = int(page_size)
    page_number = int(page_number)
    filters = {
        'semester_id': semester_id
    }
    data, num = services.get_course_students(tid, sec_id, page_number, page_size, filters)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

#添加作业
@teacher_bp.route('/teacher/<int:tid>/courses/<int:sec_id>/homework/add', methods=['POST'])
def add_homework(tid, sec_id):
    # 前端传入的参数：sec_id 作业名字 作业内容 截止时间
    data = request.json
    try:
        services.add_homework(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})


#查看学生作业提交情况，返回学生id，姓名，作业id，作业内容，提交时间，可以在前端进行批改
@teacher_bp.route('/teacher/<int:tid>/courses/<int:sec_id>/homeworks', methods=['GET'])
def get_homeworks(tid, sec_id):
    # 前端传入的参数：学期、学生姓名，是否批改，分页信息
    semester_id = request.args.get('semester_id')
    student_name = request.args.get('student_name')
    status = request.args.get('status') # 是否批改 0 全部 1 未批改 2 已批改
    page_size = request.args.get('size')
    page_number = request.args.get('page')
    if not page_size or not page_number:
        return create_response({}, message='page and size are required,such as /teacher/201011919/courses/1/homeworks?size=20&page=0', code=-1)
    page_size = int(page_size)
    page_number = int(page_number)
    filters = {
        'semester_id': semester_id,
        'student_name': student_name,
        'status': status
    }
    data, num = services.get_homeworks(tid, sec_id, page_number, page_size, filters)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

# 批改作业，需要提交学生id，作业名字，分数
# URL的参数中包含了教师id和课程id（注意，这个是sec_id）
@teacher_bp.route('/teacher/<int:tid>/courses/<int:sec_id>/homeworks/grade', methods=['POST'])
def set_grade_homework(tid, sec_id):
    # 前端传入的参数：学生id，作业id，分数,学期
    data = request.json
    try:
        services.set_grade_homework(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#设置学生成绩，需要提交学生id，课程id，分数
@teacher_bp.route('/teacher/<int:tid>/courses/<int:sec_id>/student/grade', methods=['POST'])
def set_grade(tid, sec_id):
    # 前端传入的参数：学生id，sec_id，分数
    data = request.json
    try:
        services.set_grade(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#设置学生奖惩, 需要提交学生id，奖惩内容
@teacher_bp.route('/teacher/award', methods=['POST'])
def award():
    data = request.json
    try:
        services.award(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

# TODO：开一门全新的课程
# 开一门新课程，需要提交课程名，学分
@teacher_bp.route('/teacher/courses/new', methods=['POST'])
def new_course():
    data = request.json
    # 前端传入的参数：课程id cid，课程名course_name，学分credit，开课学院did
    try:
        services.new_course(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#查看所有课程
@teacher_bp.route('/teacher/courses', methods=['GET'])
def get_all_courses():
    data = services.get_course(0,10000)
    return create_response(data, message='success', code=0)

#删除一门课程
@teacher_bp.route('/teacher/courses/delete/<int:section_id>', methods=['DELETE'])
def delete_course(section_id):
    try:
        services.delete_course(section_id)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success'})

#取消学生选课
@teacher_bp.route('/teacher/courses/<int:section_id>/student/<int:sid>/delete', methods=['DELETE'])
def delete_student(section_id, sid):
    try:
        services.delete_student_course(section_id, sid)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success'})