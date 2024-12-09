import requests
from src.client.core.config import *
class Account:
    id = int()
    identity = str()

    def __init__(self):
        self.id = 0
        self.identity = ""

    def login(self, user_id, password):
        r = requests.post(Config.API_BASE_URL + "/login", json={"id": user_id, "password": password})
        if r.status_code != 200:
            print("Login failed.Cannot connect to server.")
            return False
        if r.json()['code'] == 0:
            self.id = id
            self.identity = r.json()['identity']
            print("Login success.")
            return True
        else:
            print(r.json()['message'])