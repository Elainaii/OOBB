import requests

'''
r = requests.post("http://127.0.0.1:5000/admin/student/add", json = {
    'sid': '202400004',
    'student_name': '一一四',
    'did': '1060',
    'sex': 'F',
    'birthday': '2000-01-01',
    'ID_number': '127756200001016781',
    'Email': 'a7d@af.cm',
    'mid': '1176'
})
'''
'''
r = requests.post("http://127.0.0.1:5000/login", json = {
    'id': '202400001',
    'password': '666666'
})
'''

'''
r = requests.post("http://127.0.0.1:5000/admin/teacher/add", json = {
    'tid': '20241145',
    'teacher_name': '孙笑川',
    'did': '1060',
    'sex': 'F',
    'birthday': '1000-01-01',
    'ID_number': '127756100001016781',
    'Email': 'a7151651d@af.cm'
})
'''

'''
r = requests.post("http://127.0.0.1:5000/admin/admin/add", json = {
    'manager_id': '2024000',
    'manager_name': '孙笑川',
    'Email': 'a7151651d@af.cm'
})
'''

print(r.text)