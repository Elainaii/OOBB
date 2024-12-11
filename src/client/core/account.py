import requests
from src.client.core.config import *
class Account:
    id = int()
    identity = str()
    dept_list = list()
    semester_list = list()
    curr_semester = str()


    def __init__(self):
        self.id = 0
        self.identity = ""

    def login(self, user_id, password):
        try:
            r = requests.post(Config.API_BASE_URL + "/login", json={"id": user_id, "password": password}, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"Login failed. An error occurred: {e}"

        if r.json()['code'] == 0:
            self.id = user_id
            self.identity = r.json()['identity']
            return True,"Login success."
        else:
            return False,r.json()['message']

    def get_dept_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + "/departments", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.dept_list = r.json()['data']
            return True,"Get dept list success."
        else:
            return False,r.json()['message']
