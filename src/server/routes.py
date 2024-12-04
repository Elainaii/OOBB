#负责处理api
from flask import Blueprint, request, jsonify
import services
from src.server.services import *

bp = Blueprint('main', __name__)

@bp.route('/students', methods=['GET'])
def fetch_students():
    courses = get_students()
    return jsonify(courses)
