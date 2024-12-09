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