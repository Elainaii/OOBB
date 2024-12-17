from flask import Blueprint, request, jsonify, make_response
import src.server.services as services
from src.server.exceptions import *
from src.server.routes.route_utils import *

'''
管理员模块：
1. 查看学生/教师列表
2. 添加学生（注册新的号）
3. 添加教师（注册新的号）
4. 修改学生信息：需要提交学生id，修改后的信息，不修改的设为空
5. 修改教师信息：需要提交教师id，修改后的信息，不修改的设为空
'''
admin_bp = Blueprint('admin',__name__)

# 获取学生列表
@admin_bp.route('/admin/students', methods=['GET'])
def fetch_students():
    page_number = request.args.get('page')
    page_size = request.args.get('size')
    if not page_number or not page_size:
        return create_response({}, message='page and size are required,such as /admin/students?size=20&page=0', code=-1)
    page_number = int(page_number)
    page_size = int(page_size)
    data = services.get_students(page_number, page_size)
    num = services.get_student_num()
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

# 获取教师列表
@admin_bp.route('/admin/teachers', methods=['GET'])
def fetch_teachers():
    page_number = request.args.get('page')
    page_size = request.args.get('size')
    if not page_number or not page_size:
        return create_response({}, message='page and size are required,such as /admin/teachers?size=20&page=0', code=-1)
    page_number = int(page_number)
    page_size = int(page_size)
    data = services.get_teachers(page_number, page_size)
    num = services.get_teacher_num()
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

# 获取管理员列表
@admin_bp.route('/admin/admins', methods=['GET'])
def fetch_admins():
    page_number = request.args.get('page')
    page_size = request.args.get('size')
    if not page_number or not page_size:
        return create_response({}, message='page and size are required,such as /admin/admins?size=20&page=0', code=-1)
    page_number = int(page_number)
    page_size = int(page_size)
    data = services.get_admins(page_number, page_size)
    num = services.get_admin_num()
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

#添加学生
@admin_bp.route('/admin/student/add', methods=['POST'])
def add_student():
    data = request.json
    try:
        services.add_student(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#添加教师
@admin_bp.route('/admin/teacher/add', methods=['POST'])
def add_teacher():
    data = request.json
    try:
        services.add_teacher(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

# 添加管理员
@admin_bp.route('/admin/admin/add', methods=['POST'])
def add_admin():
    data = request.json
    try:
        services.add_admin(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#修改学生信息，需要提交学生id，修改后的信息，不修改的设为空
@admin_bp.route('/admin/student/change', methods=['POST'])
def change_student():
    data = request.json
    try:
        services.change_student(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#修改教师信息，需要提交教师id，修改后的信息，不修改保持原状
@admin_bp.route('/admin/teacher/change', methods=['POST'])
def change_teacher():
    data = request.json
    try:
        services.change_teacher(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

#修改管理员信息，需要提交管理员id，修改后的信息，不修改保持原状
@admin_bp.route('/admin/admin/change', methods=['POST'])
def change_admin():
    data = request.json
    try:
        services.change_admin(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

# 添加院系
@admin_bp.route('/admin/department/add', methods=['POST'])
def add_department():
    data = request.json
    try:
        services.add_department(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

# 修改院系名字
@admin_bp.route('/admin/department/change', methods=['POST'])
def change_department():
    # 提交院系id，修改后的院系名字
    data = request.json
    try:
        services.change_department(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})

# 添加一个新学期
@admin_bp.route('/admin/semester/add', methods=['POST'])
def add_semester():
    services.add_semester()
    return jsonify({'code': 0, 'message': 'success'})

# 帮助教师、学生修改密码
# 无需验证旧密码，直接修改
@admin_bp.route('/admin/account/change_password', methods=['POST'])
def change_password_admin():
    data = request.json
    try:
        services.change_password_admin(data)
    except myException as e:
        return jsonify({'code': -1, 'message': str(e)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})
    return jsonify({'code': 0, 'message': 'success','data':data})