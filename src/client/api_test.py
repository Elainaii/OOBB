import requests


r = requests.post("http://127.0.0.1:5000//login",json={"id":20240001,"password":"666666"})

print(r.text)