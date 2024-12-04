from flask import Flask
from routes import bp
app = Flask(__name__)

#with app.app_context():
    #from . import routes
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)