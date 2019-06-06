# 收到gui传入的数据，然后开始调集资源

import orm
import difflib


class CourceNode():

    def __init__(self, raw_data, msg, db):
        self.msg = msg
        self.raw_data = raw_data
        self.db = db

        self.new_class_code = self.raw_data[0].split(' ')
        self.class_time = self.raw_data[1].split(' ')
        self.course = self.__del_blank_space(self.raw_data[2].split('\n'))

        self.__get_file_name_and_address('n')

    def __del_blank_space(self, listx):
        fin_listx = []
        for ch in listx:
            if ch in ['', '\n', ' ']:
                pass
            else:
                fin_listx.append(ch)
        return fin_listx

    def __create_tasks(self):
        tasks_list = []
        max_cnt = len(self.new_class_code)
        for i in range(max_cnt):
            tasks_list.append((self.new_class_code[i], self.class_time[i], self.course))
        return tasks_list

    def __get_file_name_and_address(self, name):  # 根据资源名称获取资源的真实名称及文件地址
        '''
        :param name: 输入待查找的文件名
        :return: 返回非None则意味着找到符合要求的文件，返回格式是（文件真实名称，文件地址）
        '''
        source_data = self.db.query_all(orm.Source)
        sim_score_max = 0
        file_name = ''
        file_address = ''
        for data in source_data:
            current_score = self.__string_similar(data.source_name, name)
            if current_score > sim_score_max:
                sim_score_max = current_score
                file_name = data.source_name
                file_address = data.address
        if sim_score_max >= 0.5:
            return (file_name, file_address)
        else:
            return None

    def __string_similar(self, s1, s2):  # 比较s1、s2连个字符串的相似度，返回相似度
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
