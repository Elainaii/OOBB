create table department (
    did int primary key,
    dept_name varchar(50) not null
);

create table student (
    sid int primary key,
    student_name varchar(50) not null,
    mid int not null,
    did int not null ,
    sex char(1) not null,check ( sex in ('M','F')),
    birthday date not null,
    ID_number char(18) not null,
    Email varchar(50) not null,
    foreign key (did) references department(did),
    foreign key (mid) references major(mid)
);

create table course (
    cid int primary key,
    did int not null,
    course_name varchar(50) not null,
    credit int not null,check ( credit >= 0),
    foreign key (did) references department(did)
);

create table teacher (
    tid int primary key,
    did int not null,
    teacher_name varchar(50) not null,
    sex char(1) not null,check ( sex in ('M','F')),
    birthday date not null,
    ID_number char(18) not null,
    Email varchar(50) not null,
    foreign key (did) references department(did)
);


create table classroom (
    classroom_id int primary key,
    building_name varchar(50) not null,
    room_number int not null,
    capacity int not null,check ( capacity > 0)
);

create table timeslot (
    timeslot_id int primary key,
    day int not null,
    start_time int not null,
    end_time int not null
);

create table award (
    sid int not null,
    award_name varchar(10) not null,
    award_content text
);

create table section (
    sec_id int primary key,
    cid int not null,
    semester varchar(10) not null,
    year int not null,
    start_week int not null,
    end_week int not null,
    max_students int not null,
    foreign key (cid) references course(cid)
);

create table homework (
    sec_id int not null,
    homework_name varchar(50) not null,
    deadline date not null,
    content text not null,
    foreign key (sec_id) references section(sec_id)
);

create table homework_collection (
    sid int not null,
    sec_id int not null,
    homework_name varchar(50) not null,
    submit_time date not null,
    content text not null,
    score numeric(4,1),
    foreign key (sid) references student(sid),
    foreign key (sec_id) references section(sec_id)
);

create table pre_course (
    cid int not null,
    pre_cid int not null,
    foreign key (cid) references course(cid),
    foreign key (pre_cid) references course(cid)
);

create table student_section (
    sid int not null,
    sec_id int not null,
    score numeric(4,1),
    foreign key (sid) references student(sid),
    foreign key (sec_id) references section(sec_id)
);

create table teacher_section (
    tid int not null,
    sec_id int not null,
    foreign key (tid) references teacher(tid),
    foreign key (sec_id) references section(sec_id)
);

create table course_section (
    cid int not null,
    sec_id int not null,
    foreign key (cid) references course(cid),
    foreign key (sec_id) references section(sec_id)
);

create table major(
    mid int primary key,
    major_name varchar(50) not null
);

create table classroom_section (
    sec_id int not null,
    classroom_id int not null,
    foreign key (sec_id) references section(sec_id),
    foreign key (classroom_id) references classroom(classroom_id)
);

create table timeslot_section (
    sec_id int not null,
    timeslot_id int not null,
    foreign key (sec_id) references section(sec_id),
    foreign key (timeslot_id) references timeslot(timeslot_id)
);

create table account(
    id int primary key,
    password varchar(50) not null,
    identity char(1) not null,check ( identity in ('S','T','A'))

)

create table manager(
    manager_id int primary key,
    manager_name varchar(50) not null,
    Email varchar(50) not null
)

show create table manager;

drop table manager;

SHOW CREATE TABLE account;



drop table course_section;

create table semester(
    semester_id int primary key,
    year int not null,
    season char(1) not null,check ( season in ('春','夏','秋','冬'))
);

# 把semester_id加到section表中，删掉semester和year字段
alter table section add semester_id int not null;
alter table section drop column semester;
alter table section drop column year;
alter table section add foreign key (semester_id) references semester(semester_id);


drop table classroom_section;
drop table timeslot_section;

create table timeslot_classroom_section(
    sec_id int not null,
    timeslot_id int not null,
    classroom_id int not null,
    foreign key (sec_id) references section(sec_id),
    foreign key (timeslot_id) references timeslot(timeslot_id),
    foreign key (classroom_id) references classroom(classroom_id)
);



# 往section中加入rest_number字段，表示剩余可选人数
alter table section add rest_number int not null;