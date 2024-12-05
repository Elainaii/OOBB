from flask import Blueprint, request, jsonify, make_response
import src.server.services as services
from src.server.exceptions import *
from src.server.routes.route_utils import *

'''
管理员模块：
1. 查看学生列表
2. 添加学生（注册新的号）
3. 添加教师（注册新的号）
4. 修改学生信息：需要提交学生id，修改后的信息，不修改的设为空
5. 修改教师信息：需要提交教师id，修改后的信息，不修改的设为空
TODO：
6. 授权：增加为教师增加/取消权限的功能
7. 查看教师
8. 查看学生
9. 注销账号（包括学生和教师）
'''
admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/admin/students', methods=['GET'])
def fetch_students():
    data = services.get_students()
    return create_response(data, message='success', code=0)


#添加学生
@admin_bp.route('/admin/student/add', methods=['POST'])
def add_student():
    data = request.json
    try:
        services.add_student(data)
    except myException as e:
        return create_response({}, message=str(e), code=-1)
    except Exception as e:
        return create_response({}, message=str(e), code=-1)
    return create_response(data, message='success', code=0)

#添加教师
@admin_bp.route('/admin/teacher/add', methods=['POST'])
def add_teacher():
    pass

#修改学生信息，需要提交学生id，修改后的信息，不修改的设为空
@admin_bp.route('/admin/student/change', methods=['POST'])
def change_student():
    pass

#修改教师信息，需要提交教师id，修改后的信息，不修改的设为空
@admin_bp.route('/admin/teacher/change', methods=['POST'])
def change_teacher():
    pass

#添加classroom
@admin_bp.route('/admin/classroom/add', methods=['GET'])
def add_classroom():
    pass

#添加院系
@admin_bp.route('/admin/department/add', methods=['GET'])
def add_department():
    pass




