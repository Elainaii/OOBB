import requests
from src.client.core.config import *
class Account:
    id = int()
    identity = str()
    dept_list = list()
    semester_list = list()
    major_list = list()
    curr_semester = 0


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
            print(f"An error occurred: {e}")
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.dept_list = r.json()['data']
            print("Get dept list success.")
            return True,"Get dept list success."
        else:
            print(r.json()['message'])
            return False,r.json()['message']

    def get_semester_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + "/semester?size=100&page=0", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.semester_list = r.json()['data']
            self.curr_semester = self.semester_list[0]['semester_id']
            return True,"Get semester list success."
        else:
            return False,r.json()['message']

    def get_major_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + "/major", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.major_list = r.json()['data']
            return True,"Get major list success."
        else:
            return False,r.json()['message']


class StudentController():
    def __init__(self,account:Account):
        self.account = account
        self.course_list = list()
        self.course_total_size = -1
        self.course_curr_page = 0
        self.course_total_page = 0
        self.page_size = 12
        self.my_course_filter = dict()
        self.select_course_list = list()

        self.account.get_semester_list()
        self.account.get_dept_list()

    def init_course_list(self,page = 0):
        if self.course_total_size == -1 :
            try:
                r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/courses?semester_id={self.my_course_filter['semester_id']}&status={self.my_course_filter['status']}&course_name={self.my_course_filter['course_name']}&size=12&page={self.course_curr_page}", timeout=2)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                return False,"连接超时"
            except requests.exceptions.RequestException as e:
                return False,f"An error occurred: {e}"

            if r.json()['code'] == 0:
                self.course_list = r.json()['data']
                return True,"Get course list success."
            else:
                return False,r.json()['message']

    def course_next_page(self):
        if self.course_curr_page + 1 < self.course_total_page:
            self.course_curr_page += 1
            return self.init_course_list(self.course_curr_page)
        else:
            return False,"已经是最后一页了"

    def course_prev_page(self):
        if self.course_curr_page - 1 >= 0:
            self.course_curr_page -= 1
            return self.init_course_list(self.course_curr_page)
        else:
            return False,"已经是第一页了"

    def set_my_course_filter(self,semester_id,status,course_name):
        self.my_course_filter = {
            'semester_id': semester_id,
            'status': status,
            'course_name': course_name
        }


class AdminController:
    def __init__(self, account: Account):
        self.account = account
        self.curr_semester = 0

        self.student_list = list()
        self.student_total_size = -1
        self.student_curr_page = 0
        self.student_total_page = 0
        self.page_size = 12

        self.teacher_list = list()
        self.teacher_total_size = -1
        self.teacher_curr_page = 0
        self.teacher_total_page = 0

        self.account.get_semester_list()
        self.account.get_dept_list()
        self.account.get_major_list()

    def get_student_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/admin/students?size=12&page={self.student_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.student_list = r.json()['data']
            self.student_total_size = r.json()['total_num']
            self.student_total_page = self.student_total_size // self.page_size + 1
            return True,"Get student list success."
        else:
            return False,r.json()['message']
    def student_next_page(self):
        if self.student_curr_page + 1 < self.student_total_page:
            self.student_curr_page += 1
            self.get_student_list()
            return True,'Get student list success.'
        else:
            return False,"已经是最后一页了"

    def student_prev_page(self):
        if self.student_curr_page - 1 >= 0:
            self.student_curr_page -= 1
            self.get_student_list()
            return True,'Get student list success.'
        else:
            return False,"已经是第一页了"

    def get_teacher_list(self):
        if self.teacher_total_size == -1:
            try:
                r = requests.get(Config.API_BASE_URL + f"/admin/teachers?size=12&page={self.teacher_curr_page}", timeout=2)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                return False,"连接超时"
            except requests.exceptions.RequestException as e:
                return False,f"An error occurred: {e}"

            if r.json()['code'] == 0:
                self.teacher_list = r.json()['data']
                return True,"Get teacher list success."
            else:
                return False,r.json()['message']

    def teacher_next_page(self):
        if self.teacher_curr_page + 1 < self.teacher_total_page:
            self.teacher_curr_page += 1
            return self.get_teacher_list()
        else:
            return False,"已经是最后一页了"

    def teacher_prev_page(self):
        if self.teacher_curr_page - 1 >= 0:
            self.teacher_curr_page -= 1
            return self.get_teacher_list()
        else:
            return False,"已经是第一页了"


    def add_student(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/student/add", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Add student success."
        else:
            return False,r.json()['message']

