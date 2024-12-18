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
        self.home_info = dict()

        self.course_list = list()
        self.course_total_size = -1
        self.course_curr_page = 0
        self.course_total_page = 0
        self.page_size = 12
        self.my_course_filter = dict()

        self.select_course_total_size = -1
        self.select_course_list = list()

        self.award_total_size = -1
        self.award_list = list()

        self.homework_total_size = -1
        self.homework_list = list()

        self.account.get_semester_list()
        self.account.get_dept_list()

    # 首页的一些信息
    def init_home(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/info", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            print(e)
            return False,f"An error occurred: {e}"
        response_json = r.json()
        if r.json()['code'] == 0:
            self.home_info = r.json()['data']
            return True,r.json()['data']
        else:
            return False,r.json()['message']

    def init_course_list(self,page = 0):
        try:
            r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/courses?semester_id={self.my_course_filter['semester_id']}&status={self.my_course_filter['status']}&size=12&page={self.course_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.course_list = r.json()['data']
            self.course_total_size = r.json()['total_num']
            self.course_total_page = self.course_total_size // self.page_size + 1
            return True,"Get course list success."
        else:
            return False,r.json()['message']

    def mycourse_next_page(self):
        if self.course_curr_page + 1 < self.course_total_page:
            self.course_curr_page += 1
            return self.init_course_list(self.course_curr_page)
        else:
            return False,"已经是最后一页了"

    def mycourse_prev_page(self):
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

    def init_select_course(self):
        print(1919810)
        if self.select_course_total_size == -1:
            try:
                r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/courses/info?size=12&page=0", timeout=2)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                return False,"连接超时"
            except requests.exceptions.RequestException as e:
                return False,f"An error occurred: {e}"

            if r.json()['code'] == 0:
                self.select_course_list = r.json()['data']
                return True,"Get select course list success."
            else:
                return False,r.json()['message']

    def get_all_my_course_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/courses?size={10000}&page=0", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时",[]
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}",[]
        if r.json()['code'] == 0:
            res = r.json()['data']
            return True,"Get my course list success.",res
        else:
            return False,r.json()['message'],[]

    def select_course(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + f"/student/{self.account.id}/courses/select", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Select course success."
        else:
            return False,r.json()['message']

    def init_award(self):
        if self.award_total_size == -1:
            try:
                r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/awards?size=12&page=0", timeout=2)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                return False,"连接超时"
            except requests.exceptions.RequestException as e:
                print(e)
                return False,f"An error occurred: {e}"

            if r.json()['code'] == 0:
                self.award_list = r.json()['data']
                return True,"Get award list success."
            else:
                return False,r.json()['message']

    def init_homework(self):
        if self.homework_total_size == -1:
            try:
                r = requests.get(Config.API_BASE_URL + f"/student/{self.account.id}/courses/homework?size=12&page=0", timeout=2)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                return False,"连接超时"
            except requests.exceptions.RequestException as e:
                return False,f"An error occurred: {e}"

            if r.json()['code'] == 0:
                self.homework_list = r.json()['data']
                return True,"Get homework list success."
            else:
                return False,r.json()['message']

    def submit_homework(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + f"/student/{self.account.id}/courses/homework/submit", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Submit homework success."
        else:
            return False,r.json()['message']

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

        self.admin_list = list()
        self.admin_total_size = -1
        self.admin_curr_page = 0
        self.admin_total_page = 0

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

    def get_all_student_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/admin/students?size={self.student_total_size}&page=0", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时",[]
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}",[]
        if r.json()['code'] == 0:
            res = r.json()['data']
            return True,"Get student list success.",res
        else:
            return False,r.json()['message'],[]

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
        try:
            r = requests.get(Config.API_BASE_URL + f"/admin/teachers?size=12&page={self.teacher_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.teacher_list = r.json()['data']
            self.teacher_total_size = r.json()['total_num']
            self.teacher_total_page = self.teacher_total_size // self.page_size + 1
            return True,"Get teacher list success."
        else:
            return False,r.json()['message']

    def get_all_teacher_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/admin/teachers?size={self.teacher_total_size}&page=0", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时",[]
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}",[]
        if r.json()['code'] == 0:
            res = r.json()['data']
            return True,"Get teacher list success.",res
        else:
            return False,r.json()['message'],[]

    def teacher_next_page(self):
        if self.teacher_curr_page + 1 < self.teacher_total_page:
            self.teacher_curr_page += 1
            self.get_teacher_list()
            return True,'Get teacher list success.'
        else:
            return False,"已经是最后一页了"

    def teacher_prev_page(self):
        if self.teacher_curr_page - 1 >= 0:
            self.teacher_curr_page -= 1
            self.get_teacher_list()
            return True,'Get teacher list success.'
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

    def change_student_info(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/student/change", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.get_student_list()
            return True,"Change student info success."
        else:
            return False,r.json()['message']

    def add_teacher(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/teacher/add", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Add teacher success."
        else:
            return False,r.json()['message']

    def change_teacher_info(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/teacher/change", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.get_teacher_list()
            return True,"Change teacher info success."
        else:
            return False,r.json()['message']

    def add_admin(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/admin/add", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Add admin success."
        else:
            return False,r.json()['message']


    def get_admin_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/admin/admins?size=12&page={self.admin_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.admin_list = r.json()['data']
            self.admin_total_size = r.json()['total_num']
            self.admin_total_page = self.admin_total_size // self.page_size + 1
            return True,"Get admin list success."
        else:
            return False,r.json()['message']

    def get_all_admin_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/admin/admins?size={self.admin_total_size}&page=0", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时",[]
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}",[]
        if r.json()['code'] == 0:
            res = r.json()['data']
            return True,"Get admin list success.",res
        else:
            return False,r.json()['message'],[]

    def admin_next_page(self):
        if self.admin_curr_page + 1 < self.admin_total_page:
            self.admin_curr_page += 1
            self.get_admin_list()
            return True,'Get admin list success.'
        else:
            return False,"已经是最后一页了"

    def admin_prev_page(self):
        if self.admin_curr_page - 1 >= 0:
            self.admin_curr_page -= 1
            self.get_admin_list()
            return True,'Get admin list success.'
        else:
            return False,"已经是第一页了"

    def change_admin_info(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/admin/change", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            self.get_admin_list()
            return True,"Change admin info success."
        else:
            return False,r.json()['message']


class TeacherController():
    def __init__(self,account:Account):
        self.account = account

        self.course_list = list()
        self.course_total_size = -1
        self.course_curr_page = 0
        self.course_total_page = 0
        self.page_size = 12

        self.curr_course_id = -1
        self.student_list = list()
        self.student_curr_page = 0
        self.student_total_page = 0
        self.student_total_size = -1

        self.homework_list = list()
        self.homework_curr_page = 0
        self.homework_total_page = 0
        self.homework_total_size = -1

        self.all_course_list = list()
        self.all_course_total_size = -1
        self.all_course_curr_page = 0
        self.all_course_total_page = 0

        self.curr_add_course_id = -1

        self.time_slot_list = list()
        self.classroom_list = list()

        self.time_classroom_list = list()



        self.account.get_semester_list()
        self.account.get_dept_list()
        self.get_time_slot_list()
        self.get_classroom_list()


    def get_course_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/teacher/{self.account.id}/courses?size=12&page={self.course_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.course_list = r.json()['data']
            self.course_total_size = r.json()['total_num']
            self.course_total_page = self.course_total_size // self.page_size + 1
            return True,"Get course list success."
        else:
            return False,r.json()['message']

    def get_homework_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/teacher/{self.account.id}/courses/{self.curr_course_id}/homeworks?size=12&page={self.homework_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.homework_list = r.json()['data']
            self.homework_total_size = r.json()['total_num']
            self.homework_total_page = self.homework_total_size // self.page_size + 1
            return True,"Get homework list success."
        else:
            return False,r.json()['message']

    def get_course_students(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/teacher/{self.account.id}/courses/{self.curr_course_id}/students?size=12&page={self.course_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.student_list = r.json()['data']
            self.student_total_size = r.json()['total_num']
            self.student_total_page = self.student_total_size // self.page_size + 1
            return True,"Get course students success."
        else:
            return False,r.json()['message']


    def change_password(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/account/change_password", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Change password success."
        else:
            return False,r.json()['message']

    def add_department(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/department/add", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Add department success."
        else:
            return False,r.json()['message']

    def change_department(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + "/admin/department/change", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Change department success."
        else:
            return False,r.json()['message']

    def get_all_course_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + f"/course?size=12&page={self.all_course_curr_page}", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.all_course_list = r.json()['data']
            self.all_course_total_size = r.json()['total_num']
            self.all_course_total_page = self.all_course_total_size // self.page_size + 1
            return True,"Get course list success."
        else:
            return False,r.json()['message']

    def get_classroom_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + "/classroom?size=10000&page=0", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.classroom_list = r.json()['data']
            return True,"Get classroom list success."
        else:
            return False,r.json()['message']

    def get_time_slot_list(self):
        try:
            r = requests.get(Config.API_BASE_URL + "/time_slot", timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"
        if r.json()['code'] == 0:
            self.time_slot_list = r.json()['data']
            return True,"Get time slot list success."
        else:
            return False,r.json()['message']
    def reset_course_time_list(self):
        self.time_classroom_list = list()

    def add_course_time_list(self,time_slot_id,classroom_id):
        time_slot_ids = [entry['time_slot_id'] for entry in self.time_classroom_list]
        if time_slot_id  in time_slot_ids:
            return False,"Time slot exists."
        # 然后检查教室、时间段是否冲突
        self.time_classroom_list.append({
            'time_slot_id':time_slot_id,
            'classroom_id':classroom_id
        })
        return True,"Add course time success."

    def del_course_time_list(self, time_slot_id, classroom_id):
        if {'time_slot_id':time_slot_id,'classroom_id':classroom_id} in self.time_classroom_list:
            self.time_classroom_list.remove({'time_slot_id':time_slot_id,'classroom_id':classroom_id})
            return True,"Delete course time success."
        else:
            return False,"Course time not exists."

    def submit_course(self):
        data = {
            'cid':self.curr_add_course_id,
            'time_classroom':self.time_classroom_list
        }
        try:
            r = requests.post(Config.API_BASE_URL + f"/teacher/{self.account.id}/courses/add", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Submit course success."
        else:
            return False,r.json()['message']

    def create_new_course(self, data):
        try:
            r = requests.post(Config.API_BASE_URL + "/teacher/courses/new", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Create course success."
        else:
            return False,r.json()['message']

    def set_homework_grade(self,data):
        try:
            r = requests.post(Config.API_BASE_URL + f"/teacher/{self.account.id}/courses/{self.curr_course_id}/homeworks/grade", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Set homework grade success."
        else:
            return False,r.json()['message']

    def set_course_grade(self,data):
        try:#/teacher/<int:tid>/courses/<int:sec_id>/student/grade
            r = requests.post(Config.API_BASE_URL + f"/teacher/{self.account.id}/courses/{self.curr_course_id}/student/grade", json=data, timeout=2)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            return False,"连接超时"
        except requests.exceptions.RequestException as e:
            return False,f"An error occurred: {e}"

        if r.json()['code'] == 0:
            return True,"Set course grade success."
        else:
            return False,r.json()['message']

