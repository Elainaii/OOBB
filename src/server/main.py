from flask import Flask
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.pubilc_routes import public_bp

app = Flask(__name__)

#with app.app_context():
    #from . import routes
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(public_bp)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)