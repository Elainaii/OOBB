from flask import jsonify, make_response

def create_response(data, message='success', code=0):
    response = {
        'code': code,
        'message': message,
        'data': data
    }
    return make_response(jsonify(response), code)
