# 操作数据库
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import logging

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


class db():
    def __init__(self):
        self.session = self.get_session()

    # 获取session------------------------------------------------------------------
    def get_session(self):
        logging.info('开始创建连接...')
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
        engine = create_engine(
            'mysql+mysqlconnector://%s:%s@%s:%d/%s' % (cg.user, cg.password, result, port, cg.db_name))

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
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

    def close(self):
        self.session.close()

    def query_all(self, class_name):  # 查询数据库中所有信息
        # class_name为待查表对应的类对象名称
        # filters筛选格式为：类名.属性==值
        result = self.session.query(class_name)

        # 返回结果是user类组成的可迭代对象
        return result
