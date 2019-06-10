# 更新资数据库
# 无输入参数
# 传出调集进度数据

import os
import time

import config as cg
import orm


class Source():
    def __init__(self,db,raw_msg):
        self.root = cg.source_path
        self.operation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.source_data_list = []  # 存放待插入的source数据
        self.db = db
        self.raw_msg=raw_msg

        # 初始化之后自动运行---------------------------------------------------------------------------------------------
        # 清空数据表
        self.db.clear_table(orm.Source)

        # 搜索并写数据表
        self.raw_msg.append('遍历资源文件夹')
        readme_paths = self.walk_source_folder()
        for readme_path in readme_paths:
            readme_dic = self.parse_readme(readme_path)
            self.gather_source_data(readme_dic)

        self.raw_msg.append('向数据库中插入数据')
        self.write2database(self.source_data_list)
        self.db.close()

    def walk_source_folder(self):
        ReadMe_dir = []
        for root, dirs, files in os.walk(self.root):
            '''
            root:当前正在被被遍历的文件夹的地址，该文件夹简称root文件夹
            dirs：root文件夹里的所有文件夹名称
            files：root文件夹内的所有文件名称

            返回readme文件地址，格式为：['地址1','地址2',……]
            '''
            for ch in files:
                if ch == 'ReadMe.txt':
                    ReadMe_dir.append(os.path.join(root, ch))
        return ReadMe_dir

    def parse_readme(self, readme_dir):
        '''
        传入一个readme文件的地址，然后进行解析
        返回解析后的数据，为一个字典，形式为：{'key':['value1','value2',……]，……}
        其中，key由readme文件决定
        '''
        f = open(readme_dir, 'rt')
        readme_data = f.readlines()
        f.close()

        readme_data_dic = {}
        cnt = 1
        keyword = ''
        for ch in readme_data:
            if ch == '\n':
                cnt = 1
            else:
                ch = self.__ignore_kuohao(ch)  # 忽略括号
                ch = self.__ignore_huiche(ch)  # 清除回车
                if cnt == 1:
                    readme_data_dic[ch] = []
                    keyword = ch
                    cnt += 1
                else:
                    readme_data_dic[keyword].append(ch)
        readme_data_dic['位置'] = [readme_dir]
        return readme_data_dic

    def __ignore_kuohao(self, str1):  # 忽略readme文件中字段后面的括号
        N = str1.find('（')
        if N != -1:
            return str1[:N]
        else:
            return str1

    def __ignore_huiche(self, str1):  # 忽略回车
        return str1.strip('\n')

    def gather_source_data(self, readme_dic):  # 获得待插入数据的列表

        source_code = self.__parse_readme_dic(readme_dic['资源编号'])
        source_name = self.__parse_readme_dic(readme_dic['名称'])
        type_name = self.__parse_readme_dic(readme_dic['类型'])
        apply_grade = self.__parse_readme_dic(readme_dic['适用年级'])
        associate_knowledge = self.__parse_readme_dic(readme_dic['关联知识点'])
        origin = self.__parse_readme_dic(readme_dic['题目来源'])
        difficulty = self.__parse_readme_dic(readme_dic['难度'])
        address = self.__parse_readme_dic(readme_dic['位置'])
        date_time = self.operation_time

        source_x = orm.Source(source_code=source_code, source_name=source_name, type_name=type_name,
                              apply_grade=apply_grade,
                              associate_knowledge=associate_knowledge, origin=origin, difficulty=difficulty,
                              address=address,
                              date_time=date_time)
        self.source_data_list.append(source_x)
        return True

    def write2database(self, source_obj_list):
        self.db.insert(*source_obj_list)

    def __parse_readme_dic(self, readme_x_list):
        '''
        传入参数为某个readme文件的一个键值，是个列表
        返回字符串
        '''
        result = '/'.join(readme_x_list)
        return result
