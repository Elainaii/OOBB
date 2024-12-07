'''
这个文件专门用于生成数据集
'''

import mysql.connector
from faker import Faker


# 链接数据库

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password = '123456',
    database = 'campus'
)

cursor = db.cursor()
# 初始化Faker
faker = Faker('zh_CN')




# 要插入的学院名称列表
departments = [
    "计算机科学与技术学院", "电子信息工程学院", "机械工程学院", "经济管理学院", "外国语学院",
    "化学与化工学院", "土木工程学院", "电气工程学院", "生物工程学院", "建筑学院",
    "材料科学与工程学院", "数学与统计学院", "物理学院", "环境科学与工程学院", "医学院",
    "法学院", "历史学院", "哲学院", "社会学学院", "政治与公共管理学院",
    "新闻与传播学院", "艺术学院", "体育学院", "心理学院", "教育科学学院",
    "地理科学学院", "航空航天学院", "交通运输学院", "矿业工程学院", "农学院",
    "林学院", "海洋科学学院", "光学与光电子学院", "软件学院", "网络空间安全学院",
    "统计与数据科学学院", "人文学院", "公共卫生学院", "药学院",
    "公共管理学院", "政治学与国际关系学院", "旅游管理学院", "艺术设计学院", "传播学院",
    "光电工程学院", "新能源学院", "数据科学与大数据技术学院", "智能科学与技术学院", "经济学院",
    "商学院", "应用技术学院", "职业技术学院",
    "海洋资源与环境学院", "生态学与环境科学学院", "农林经济管理学院", "园林学院", "植物保护学院", "坤学院", "魔法学院", "魂学院"
]

'''
# 将部门插入
cursor = db.cursor()
for i in range(len(departments)):
    cursor.execute(f"INSERT INTO department VALUES ({(1000) + (i + 1)},'{departments[i]}')")
db.commit()
'''

'''
# 存储已经生成的sid以检查重复
generated_sids = set()

# 插入学生
for i in range(10000):
    while True:
        sid = f"{faker.random_int(min=2010, max=2020)}{faker.random_int(min=10000, max=99999)}"
        if sid not in generated_sids:
            generated_sids.add(sid)
            break
    student_name = faker.name()
    did = faker.random_int(min=1, max=len(departments)) + 1000
    sex = faker.random_element(elements=('F', 'M'))
    birthday = faker.date_of_birth(minimum_age=18, maximum_age=30)  # 生成2000年以后生日
    ID_number = f"{faker.random_int(min=110000, max=999999)}{birthday.strftime('%Y%m%d')}{faker.random_int(min=1000, max=9999)}"
    Email = faker.email()

    # 插入数据到数据库
    sql = "INSERT INTO student (sid, student_name, did, sex, birthday, ID_number, Email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (sid, student_name, did, sex, birthday, ID_number, Email))

# 提交事务
db.commit()

'''

'''
# 存储已经生成的tid以检查重复
generated_tids = set()

# 插入学生
for i in range(1000):
    while True:
        tid = f"{faker.random_int(min=1980, max=2020)}{faker.random_int(min=1000, max=9999)}"
        if tid not in generated_tids:
            generated_tids.add(tid)
            break
    teacher_name = faker.name()
    did = faker.random_int(min=1, max=len(departments)) + 1000
    sex = faker.random_element(elements=('F', 'M'))
    birthday = faker.date_of_birth(minimum_age=30, maximum_age=65)  # 生成2000年以后生日
    ID_number = f"{faker.random_int(min=110000, max=999999)}{birthday.strftime('%Y%m%d')}{faker.random_int(min=1000, max=9999)}"
    Email = faker.email()
    is_admin = faker.random_element(elements=(0, 1))

    # 插入数据到数据库
    sql = "INSERT INTO teacher (tid, teacher_name, did, sex, birthday, ID_number, Email, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (tid, teacher_name, did, sex, birthday, ID_number, Email, is_admin))

# 提交事务
db.commit()

'''


course_names = [
    "数据结构", "算法设计与分析", "操作系统", "计算机网络", "软件工程",
    "数学分析", "线性代数", "概率论与数理统计", "微分方程", "数值分析",
    "力学", "电磁学", "量子力学", "热力学与统计物理", "光学",
    "无机化学", "有机化学", "物理化学", "分析化学", "生物化学",
    "普通生物学", "分子生物学", "遗传学", "生态学", "细胞生物学",
    "微观经济学", "宏观经济学", "计量经济学", "国际经济学", "发展经济学",
    "管理学原理", "市场营销", "财务管理", "人力资源管理", "运营管理",
    "中国文学", "英美文学", "文学理论", "比较文学", "世界文学",
    "法理学", "宪法学", "刑法学", "民法学", "国际法学",
    "解剖学", "生理学", "病理学", "药理学", "临床医学",
    "艺术史", "文学导论", "哲学概论", "音乐理论", "戏剧表演",
    "心理学导论", "社会学概论", "政治学基础", "经济学原理", "人类学研究",
    "会计学基础", "市场营销原理", "管理学导论", "金融学基础", "商务沟通",
    "生物学导论", "健康科学基础", "医学伦理学", "护理学原理", "公共卫生学",
    "教育心理学", "教学方法论", "课程设计与评估", "特殊教育导论", "教育技术",
    "英语写作", "外语入门", "语言学概论", "文学分析", "创意写作",
    "数据库管理", "网络安全", "人工智能导论", "网页开发",
    "地球科学概论", "天文学基础", "生物化学", "环境科学", "植物学",
    "法律基础", "国际关系", "宪法学", "刑法原理", "法律写作",
    "市场调研", "广告学", "品牌管理", "消费者行为", "电子商务",
    "财务报表分析", "审计学", "税务学", "金融市场", "投资学",
    "组织行为学", "绩效管理", "劳动法", "战略管理",
    "供应链管理", "项目管理", "生产计划与控制", "质量管理",
    "市场营销策略", "新产品开发", "销售管理", "客户关系管理", "国际市场营销",
    "创业学", "企业家精神", "小企业管理", "创新管理", "风险投资",
    "国际经济学", "贸易理论与政策", "国际金融", "跨国公司管理",
    "货币银行学", "财政学", "产业经济学",
    "城市规划", "环境经济学", "人口经济学", "区域经济学", "资源经济学",
    "统计学", "数理经济学", "行为经济学", "实验经济学",
    "法律伦理学", "比较法学", "国际公法", "国际私法", "人权法",
    "刑事诉讼法", "民事诉讼法", "商法", "知识产权法", "环境法",
    "公共法", "公司法", "金融法",
    "诊断学", "内科学", "外科学", "妇产科学",
    "儿科学", "眼科学", "耳鼻喉科学", "皮肤病学", "精神病学",
    "公共卫生学", "流行病学", "卫生统计学", "健康教育学", "职业卫生学",
    "营养学", "妇幼保健学", "老年医学", "社区医学", "健康管理学",
    "急救医学", "重症医学", "康复医学", "运动医学", "临终关怀",
    "中医学", "针灸学", "推拿学", "中药学", "方剂学",
    "中医内科学", "中医外科学", "中医妇科学", "中医儿科学", "中医骨伤科学",
    "中医养生学", "中医基础理论", "中医诊断学", "中医药理学", "中医临床医学",
    "中西医结合学", "中医急诊学", "中医康复学", "中医预防医学", "中医营养学"
]

'''
# 插入到课程
for i in range(len(course_names)):
    cid = 1000 + i
    course_name = course_names[i]
    # 学分：以0.5为一个单位，0-6之间
    credit = faker.random_int(min=0, max=12) * 0.5
    did = faker.random_int(min=1, max=len(departments)) + 1000
    # 插入数据到数据库
    sql = "INSERT INTO course (cid, course_name, credit, did) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (cid, course_name, credit, did))

# 提交事务
db.commit()

'''

'''

build_name = [
    "哈基米楼", "曼波楼", "宫崎英高楼", "魔法楼", "川普楼", "金太阳楼",
]
j = 1
for i in range(1, len(build_name) + 1):
    building_name = build_name[i - 1]
    for k in range(1, 6): # k表示楼层
        for l in range(1, 10): # l表示教室
            # room_number 是教室号，例如：101 表示1楼1号教室
            room_number = f"{k}0{l}"
            capacity = faker.random_int(min=50, max=150)
            # 插入数据到数据库
            sql = "INSERT INTO classroom (classroom_id, building_name, room_number, capacity) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (j, building_name, room_number, capacity))
            j += 1

db.commit()
'''


'''
j = 1
for i in range(1, 8): # i 星期
    for k in range(8, 21):
        sql = "INSERT INTO timeslot (timeslot_id, day, start_time, end_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (j, i, k, k + 1))
        j += 1

db.commit()

'''



majors = [
    "计算机科学与技术", "软件工程", "信息安全", "网络工程", "数据科学与大数据技术",
    "人工智能", "电子信息工程", "通信工程", "自动化", "电气工程及其自动化",
    "机械工程", "材料科学与工程", "能源与动力工程", "工业工程", "车辆工程",
    "建筑学", "土木工程", "环境工程", "给排水科学与工程", "建筑环境与能源应用工程",
    "化学工程与工艺", "生物工程", "制药工程", "食品科学与工程", "轻化工程",
    "数学与应用数学", "信息与计算科学", "物理学", "应用物理学", "化学",
    "应用化学", "生物科学", "生物技术", "生态学", "心理学",
    "应用心理学", "统计学", "管理科学", "工商管理", "市场营销",
    "会计学", "财务管理", "人力资源管理", "旅游管理", "物流管理",
    "电子商务", "国际经济与贸易", "经济学", "金融学", "投资学",
    "法学", "政治学与行政学", "国际政治", "社会学", "社会工作",
    "教育学", "学前教育", "小学教育", "体育教育", "运动训练",
    "汉语言文学", "汉语言", "英语", "翻译", "商务英语",
    "新闻学", "广告学", "传播学", "编辑出版学", "网络与新媒体",
    "历史学", "考古学", "哲学", "逻辑学", "伦理学",
    "物理学", "应用物理学", "化学", "应用化学", "生物科学",
    "生物技术", "生态学", "心理学", "应用心理学", "统计学",
    "管理科学", "工商管理", "市场营销", "会计学", "财务管理",
    "人力资源管理", "旅游管理", "物流管理", "电子商务", "国际经济与贸易",
    "经济学", "金融学", "投资学", "法学", "政治学与行政学",
    "国际政治", "社会学", "社会工作", "教育学", "学前教育",
    "小学教育", "体育教育", "运动训练", "汉语言文学", "汉语言",
    "英语", "翻译", "商务英语", "新闻学", "广告学",
    "传播学", "编辑出版学", "网络与新媒体", "历史学", "考古学",
    "哲学", "逻辑学", "伦理学", "公共管理", "行政管理",
    "劳动与社会保障", "土地资源管理", "农业资源与环境", "农学", "园艺",
    "植物保护", "动物科学", "动物医学", "林学", "园林",
    "水产养殖学", "草业科学", "农林经济管理", "农业机械化及其自动化", "农业电气化",
    "农业建筑环境与能源工程", "农业水利工程", "农业工程", "食品质量与安全", "食品科学与工程",
    "食品营养与检验教育", "食品科学与工程", "食品营养与检验教育", "食品质量与安全", "生物工程",
    "制药工程", "食品科学与工程", "轻化工程", "数学与应用数学", "信息与计算科学",
    "物理学", "应用物理学", "化学", "应用化学", "生物科学",
    "生物技术", "生态学", "心理学", "应用心理学", "统计学",
    "管理科学", "工商管理", "市场营销", "会计学", "财务管理",
    "人力资源管理", "旅游管理", "物流管理", "电子商务", "国际经济与贸易"
]



'''
for i in range(1, len(majors) + 1):
    major_name = majors[i - 1]
    mid = 1000 + i
    sql = "INSERT INTO major (mid, major_name) VALUES (%s, %s)"
    cursor.execute(sql, (mid, major_name))

db.commit()

'''
'''
# 更新学生的mid，先给学生创建mid列，外码约束major
cursor.execute("ALTER TABLE student ADD COLUMN mid INT, ADD CONSTRAINT fk_student_mid FOREIGN KEY (mid) REFERENCES major(mid)")
db.commit()

'''

'''
# 给每个学生都加上mid
# 给每一个学生加上一个major，这个major是随机的，但是要保证这个major是存在的
cursor.execute("SELECT sid FROM student")
students = cursor.fetchall()
for student in students:
    sid = student[0]
    mid = faker.random_int(min=1, max=len(majors)) + 1000
    sql = "UPDATE student SET mid = %s WHERE sid = %s"
    cursor.execute(sql, (mid, sid))

'''


'''
# 账号
# 对每一个学生，创建一个账号，账号名是学号，密码是666666
# 对每一个老师，创建一个账号，账号名是工号，密码是666666
cursor.execute("SELECT sid FROM student")
students = cursor.fetchall()
for student in students:
    sid = student[0]
    sql = "INSERT INTO account (id, password, identity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (sid, '666666', 'S')) # 学生的

# 获取老师的id
cursor.execute("SELECT tid FROM teacher")
teachers = cursor.fetchall()
for teacher in teachers:
    tid = teacher[0]
    sql = "INSERT INTO account (id, password, identity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (tid, '666666', 'T')) # 老师的

'''

'''
# 管理员账号
cursor.execute("SELECT manager_id FROM manager")
managers = cursor.fetchall()
for manager in managers:
    manager_id = manager[0]
    sql = "INSERT INTO account (id, password, identity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (manager_id, '666666', 'A')) # 管理员的

db.commit()

'''

'''

# 存储已经生成的tid以检查重复
generated_mids = set()

# 插入管理员
for i in range(100):
    while True:
        # mid 7位，随机年份加三位随机数字
        manager_id = f"{faker.random_int(min=1980, max=2020)}{faker.random_int(min=100, max=999)}"
        if manager_id not in generated_mids:
            generated_mids.add(manager_id)
            break
    manager_name = faker.name()
    Email = faker.email()
    sql = "INSERT INTO manager (manager_id, manager_name, Email) VALUES (%s, %s, %s)"
    cursor.execute(sql, (manager_id, manager_name, Email))


'''

cursor.execute("SELECT cid FROM course")
courses = cursor.fetchall()

# 选择出20门基础课程（确保basic_courses是一个包含课程ID的列表）
basic_courses = [course[0] for course in faker.random_elements(elements=courses, length=20)]

# 然后从不是基础课程的课程，在基础课程中随机选择一个作为前置课程，这个课程就可以加入到基础课程中
for course in courses:
    cid = course[0]
    if cid not in basic_courses:
        i = faker.random_int(min=1, max=3)  # 随机选择1-3门基础课程作为前置课程
        pre_courses = faker.random_elements(elements=basic_courses, length=i)
        for pre_course in pre_courses:
            if pre_course != cid:
                sql = "INSERT INTO pre_course (cid, pre_cid) VALUES (%s, %s)"
                cursor.execute(sql, (cid, pre_course))
        # 把这门课程加入到基础课程中
        basic_courses.append(cid)

db.commit()