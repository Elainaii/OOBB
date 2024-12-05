create table department (
    did int primary key,
    dept_name varchar(50) not null
);

create table student (
    sid int primary key,
    student_name varchar(50) not null,
    did int not null ,
    sex char(1) not null,check ( sex in ('M','F')),
    birthday date not null,
    ID_number char(18) not null,
    Email varchar(50) not null,
    foreign key (did) references department(did)
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
    is_admin bool not null,
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