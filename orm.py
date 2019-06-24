# 操作数据库
from sqlalchemy import Column, String, DateTime, create_engine, Date, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import logging
import datetime
import time

import config  as cg
import common_parameters as cp

logging.basicConfig(level=logging.INFO)

# 创建对象的基类:
Base = declarative_base()


class Source(Base):
    # 表的名字
    __tablename__ = 'source'

    # 表的结构
    source_code = Column(String(255), primary_key=True)
    source_name = Column(String(255))
    type_name = Column(String(255))
    apply_grade = Column(String(255))
    associate_knowledge = Column(String(255))
    origin = Column(String(255))
    difficulty = Column(String(255))
    address = Column(String(255), primary_key=True)
    date_time = Column(DateTime(), primary_key=True)


class Course(Base):
    # 表的名字
    __tablename__ = 'course'

    # 表的结构
    course_code = Column(String(255), primary_key=True)
    new_class_code = Column(String(255), ForeignKey("new_class.new_class_code"))
    source_code = Column(String(255))
    class_time = Column(Date())


class NewClass(Base):
    # 表的名字
    __tablename__ = 'new_class'

    # 表的结构
    new_class_code = Column(String(255), primary_key=True)
    appointed_time = Column(String(255))
    class_type = Column(String(255))
    teach_address = Column(String(255))
    teach_class = Column(String(255))
    grade = Column(String(255))
    create_time = Column(String(255))


class Score(Base):
    # 表的名字
    __tablename__ = 'score'

    # 表的结构
    student_code = Column(String(255), ForeignKey("student.student_code"), primary_key=True)
    course_code = Column(String(255), ForeignKey("course.course_code"), primary_key=True)
    on_class = Column(String(255))
    score1 = Column(Float(7, 3))
    score2 = Column(Float(7, 3))
    judge = Column(String(255))


class Student(Base):
    # 表的名字
    __tablename__ = 'student'

    # 表的结构
    student_code = Column(String(255), primary_key=True)
    school = Column(String(255))
    name = Column(String(255))
    grade = Column(String(255))
    class1 = Column(String(255))
    new_class_code = Column(String(255), ForeignKey("new_class.new_class_code"))
    team = Column(String(255))
    status = Column(String(255))


class db():
    def __init__(self, raw_msg):
        self.raw_msg = raw_msg
        self.session = self.get_session()

    # 获取session------------------------------------------------------------------
    def get_session(self):
        self.raw_msg.insert(0,'开始创建连接...')
        # 确定主机ip及port-----------------------------------------------
        os.system('arp -a > %s' % cg.lan_path_temp)
        result = cg.web_address
        port = cg.web_port
        with open('%s' % cg.lan_path_temp) as fp:
            for line in fp:
                line = line.split()[:2]
                if len(line) == 2 and line[1] == '%s' % cg.mac_code:
                    result = line[0]  # 局域网数据库主机ip
                    port = cg.lan_port
        os.remove(os.path.join(os.getcwd(), '%s' % cg.lan_path_temp))

        # 本机测试，所以用localhost，部署时删除该语句
        result = 'localhost'  # 部署时删除
        port = 3306  # 部署时删除

        # 返回session----------------------------------------------------
        self.engine = create_engine(
            'mysql+mysqlconnector://%s:%s@%s:%d/%s' % (cg.user, cg.password, result, port, cg.db_name))

        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        self.create_tables()

        return session

    def insert(self, *objs):  # insert函数
        for obj in objs:
            self.session.add(obj)
        self.session.commit()

    def update(self, *objs):  # update函数
        for obj in objs:
            self.session.add(obj)
        self.session.commit()

    def clear_table(self, table_class):  # 清空表，class_name为table_name对应的类对象，不是字符串而是类
        objs4del = self.query_all(table_class)
        for obj in objs4del:
            self.session.delete(obj)
        self.session.commit()

    def query_all(self, class_name):  # 查询数据库中所有信息
        # class_name为待查表对应的类对象名称
        # filters筛选格式为：类名.属性==值
        # self.raw_msg.append('正在查询%s对象数据' % class_name)
        result = self.session.query(class_name)
        # 返回结果是user类组成的可迭代对象
        return result

    def close(self):
        self.session.close()

    def create_tables(self):
        self.raw_msg.insert(0,'正在创建数据表...')
        Base.metadata.create_all(self.engine)

    def query(self, class_name, filter_sentence, rank):  # 筛选查询数据库中的信息
        result = self.session.query(class_name).filter(filter_sentence).order_by(rank)
        return result


class myTime():
    def __init__(self, raw_time, msg):
        self.msg = msg
        self.raw_time = raw_time
        if len(raw_time) == 8:
            date_fin = self.ver8()[0]
            time4floder = self.ver8()[1]
        elif len(raw_time) == 9:
            date_fin = self.ver9()
            time4floder = ''
        elif len(raw_time) == 1:
            date_fin = self.ver1()[0]
            time4floder = self.ver1()[1]
        else:
            self.msg.insert(0,'时间格式出错，请检查')
            date_fin = ''
            time4floder = ''

        self.time = date_fin
        self.time4floder = time4floder

    def ver8(self):
        year = int(self.raw_time[0:4])
        month = int(self.raw_time[4:6])
        day = int(self.raw_time[6:])

        dt_obj = datetime.datetime(year, month, day, 0, 0, 0)
        return (dt_obj.strftime('%Y-%m-%d'), self.raw_time)

    def ver9(self):
        weekday_chinese = ['一', '二', '三', '四', '五', '六', '天']

        weekday = weekday_chinese[int(self.raw_time[0:1]) - 1]
        hour1 = self.raw_time[1:3]
        min1 = self.raw_time[3:5]

        hour2 = self.raw_time[5:7]
        min2 = self.raw_time[7:]

        return "星期%s %s：%s-%s：%s" % (weekday, hour1, min1, hour2, min2)

    def ver1(self):
        weekday_chinese = ['一', '二', '三', '四', '五', '六', '天', '七']
        weekday_english = ['1', '2', '3', '4', '5', '6', '7']
        raw_time = str(self.raw_time)
        today = datetime.datetime.now()
        now = time.localtime()
        if raw_time in weekday_chinese:  # 返回下一个星期X的日期
            now_weekday = int(time.strftime("%w", now))
            future_weekday_index = weekday_chinese.index(raw_time)
            if future_weekday_index == 7:
                future_weekday_index = 6
            future_weekday = int(weekday_english[future_weekday_index])
            daydiff = future_weekday - now_weekday
            if daydiff >= 0:
                delta = datetime.timedelta(days=daydiff)
                n_days = today + delta
                return (n_days.strftime('%Y-%m-%d'), n_days.strftime('%Y%m%d'))
            else:
                daydiff1 = 7 - now_weekday + future_weekday
                delta = datetime.timedelta(days=daydiff1)
                n_days = today + delta
                return (n_days.strftime('%Y-%m-%d'), n_days.strftime('%Y%m%d'))
        elif raw_time in weekday_english:  # 返回X天后的日期
            delta = datetime.timedelta(days=int(raw_time))
            n_days = today + delta
            return (n_days.strftime('%Y-%m-%d'), n_days.strftime('%Y%m%d'))
