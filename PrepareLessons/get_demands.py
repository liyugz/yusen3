# 搜索历史资料文件夹，记录ReadMe_course文件的位置
# 传入参数：历史资料文件夹的地址
# 返回数据：调集资料任务单


import os
import logging
import time
import config as cg

logging.basicConfig(level=logging.INFO)


class ReadMe_Course():
    def __init__(self):
        self.operation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def walk_history_folder(self):
        ReadMe_course_dir = []  # 存储待完成调集单的地址
        for root, dirs, files in os.walk(cg.history_path):
            '''
            root:当前正在被被遍历的文件夹的地址，该文件夹简称root文件夹
            dirs：root文件夹里的所有文件夹名称
            files：root文件夹内的所有文件名称
            '''
            flag_c = 0  # 表示ReadMe_course文档是否存在
            flag_r = 0  # 表示result文档是否存在
            for ch in files:
                if ch == 'ReadMe_course.txt':
                    flag_c = 1
                elif ch == 'result.txt':
                    flag_r = 1
                else:
                    pass

            if flag_c == 1 and flag_r == 0:  # 有ReadMe_course但是没有result
                ReadMe_course_dir.append(os.path.join(root, 'ReadMe_course.txt'))

        if len(ReadMe_course_dir) == 0:
            logging.info('没有需要调集资源的文件夹')

        return ReadMe_course_dir

    def parse_readme_course(self, readme_course_dir):
        f = open(readme_course_dir)
        course_data = f.readlines()
        '''
        course_data是一个字典，key为字符串，value为列表
        固定key有：地址、操作时间
        不固定key是从ReadMe_course文件中提取的，对应value的形式为['data1','data2',……]
        '''
        f.close()

        course_data_dic = {}
        course_data_dic['地址'] = [os.path.split(readme_course_dir)[0]]
        course_data_dic['操作时间'] = self.operation_time

        cnt = 1
        key_word = ''
        for ch in course_data:
            if ch == '\n':
                cnt = 1
            else:
                ch = self.__ignore_kuohao(ch)
                ch = self.__ignore_huiche(ch)
                if cnt == 1:
                    course_data_dic[ch] = []
                    key_word = ch
                    cnt += 1
                else:
                    course_data_dic[key_word].append(ch)
        return course_data_dic

    def __ignore_kuohao(self, str1):  # 忽略readme文件中字段后面的括号
        N = str1.find('（')
        if N != -1:
            return str1[:N]
        else:
            return str1

    def __ignore_huiche(self, str1):  # 忽略回车
        return str1.strip('\n')
