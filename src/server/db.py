#负责数据库连接操作
import mysql.connector
from flask import current_app,g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(#TODO：改成从配置文件导入
            host='127.0.0.1',
            user='root',
            password='123456',
            database='campus'
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()