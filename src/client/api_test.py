import requests


r = requests.post("http://127.0.0.1:5000/student/add",json={"id":10001,"password":"123456"})

print(r.text)