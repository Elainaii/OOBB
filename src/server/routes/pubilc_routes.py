from Demos.mmapfile_demo import page_size
from flask import Blueprint, request, jsonify, make_response
import src.server.services as services
from src.server.exceptions import *
from src.server.routes.route_utils import *


'''
公共模块：
1. 登录：需要提交用户id和密码
2. 修改密码：需要提交用户id，旧密码，新密码

TODO：把登录/修改密码都放到个人信息模块中，并且新增功能：查看个人信息、修改个人信息
'''
public_bp = Blueprint('public',__name__)

@public_bp.route('/login', methods=['POST'])
def login():
    userid = request.json.get('id')
    password = request.json.get('password')
    user = services.get_user(userid)
    if user and user['password'] == password:
        return jsonify({'code': 0, 'message': 'success','identity':user['identity']})
    return jsonify({'code': -1, 'message': 'Invalid username or password.'})

#修改密码，需要提交用户id，旧密码，新密码
@public_bp.route('/account/change_password', methods=['POST'])
def change_password():
    userid = request.json.get('id')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    user = services.get_user(userid)
    if user and user['password'] == old_password:
        services.change_password(userid, new_password)
        return jsonify({'code': 0, 'message': 'success'})
    return jsonify({'code': -1, 'message': 'Invalid username or password.'})

# 获取院系信息
@public_bp.route('/departments', methods=['GET'])
def get_department():
    data = services.get_dept()
    return jsonify({'code': 0, 'message': 'success', 'data': data})

# 获取所有学期，分页
@public_bp.route('/semester', methods=['GET'])
def get_semester():
    page_size = request.args.get('size')
    page_number = request.args.get('page')
    if not page_size or not page_number:
        return create_response({}, message='page and size are required,such as /semester?size=20&page=0', code=-1)
    page_size = int(page_size)
    page_number = int(page_number)
    data, num = services.get_semester(page_number, page_size)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

@public_bp.route('/major', methods=['GET'])
def fetch_major():
    data = services.get_major()
    return jsonify({'code': 0, 'message': 'success', 'data': data})

# 获取所有教室，分页
@public_bp.route('/classroom', methods=['GET'])
def get_classroom():
    page_size = request.args.get('size')
    page_number = request.args.get('page')
    if not page_size or not page_number:
        return create_response({}, message='page and size are required,such as /classroom?size=20&page=0', code=-1)
    page_size = int(page_size)
    page_number = int(page_number)
    data, num = services.get_classroom(page_number, page_size)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}

# 获取所有时间段
@public_bp.route('/time_slot', methods=['GET'])
def get_time_slot():
    data = services.get_time_slot()
    return jsonify({'code': 0, 'message': 'success', 'data': data})

# 获取所有课程，分页
@public_bp.route('/course', methods=['GET'])
def get_course():
    page_size = request.args.get('size')
    page_number = request.args.get('page')
    if not page_size or not page_number:
        return create_response({}, message='page and size are required,such as /course?size=20&page=0', code=-1)
    page_size = int(page_size)
    page_number = int(page_number)
    data, num = services.get_course(page_number, page_size)
    return {'code': 0, 'message': 'success','page':page_number,'size':page_size , 'total_num': num ,'data': data}