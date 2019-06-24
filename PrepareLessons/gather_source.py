# 收到gui传入的数据，然后开始调集资源

import orm
import difflib
import config as cg
import os
from win32com.shell import shell
# from win32com.shell import shellcon

import pythoncom

pythoncom.CoInitialize()


class CourceNode():

    def __init__(self, raw_data, msg, db):
        self.msg = msg
        self.raw_data = raw_data
        self.db = db

        self.new_class_code = self.raw_data[0].split(' ')
        self.class_time = self.raw_data[1].split(' ')
        self.course = self.__del_blank_space(self.raw_data[2].split('\n'))

        self.source_data = self.db.query_all(orm.Source)  # Source表中的所有数据
        # -----------------------------------------------------------------以下函数尽在调试阶段出现-----------------------
        print(self.get_history_floder(self.new_class_code[0], self.class_time[0]))
        print(self.__create_gather_list())
        pythoncom.CoInitialize()
        self.do_gather()

    def __del_blank_space(self, listx):
        fin_listx = []
        for ch in listx:
            if ch in ['', '\n', ' ']:
                pass
            else:
                fin_listx.append(ch)
        return fin_listx

    def __get_file_name_and_address(self, name):  # 根据资源名称获取资源的真实名称及文件地址
        '''
        :param name: 输入待查找的文件名
        :return: 返回非None则意味着找到符合要求的文件，返回格式是（文件真实名称，文件地址）
        '''
        sim_score_max = 0
        file_name = ''
        file_address = ''
        for data in self.source_data:
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

    def __create_tasks(self):  # 创建任务单，格式为[[任务1],[任务2],……]，任务x格式为[new_class_code,class_time,[资源1，资源2，……]]
        tasks_list = []
        max_cnt = len(self.new_class_code)
        for i in range(max_cnt):
            tasks_list.append([self.new_class_code[i], self.class_time[i], self.course])
        return tasks_list

    def __create_gather_list(self):  # 根据任务单，创建调集单，调集单也任务单相比，临时名称变成真名，且增加文件路径
        task_list = self.__create_tasks()
        gather_list = []
        for task in task_list:
            gather_task = {}
            gather_task['new_class_code'] = task[0]
            gather_task['class_time'] = task[1]
            source_info = []  # （real_name，address）
            for source_name in task[2]:
                source_name_info = self.__get_file_name_and_address(source_name)
                if source_name_info != None:
                    source_info.append((source_name_info[0], os.path.split(source_name_info[1])[0]))
                else:
                    source_info.append((source_name, None))

            gather_task['source_info'] = source_info
            gather_list.append(gather_task)
        return gather_list

    def do_gather(self):
        '''
        target_dir：待导入的文件夹地址
        :return:
        '''
        gather_list = self.__create_gather_list()
        for item in gather_list:
            # item表示一个调集单
            new_class_code = item['new_class_code']
            class_time = item['class_time']
            source_info = item['source_info']
            target_dir = self.get_history_floder(new_class_code, class_time)
            bad_list = []  # 未调集成功的资源项目清单
            work_dic = {}  # 调集成功的资源项目，一个资源项目可能存在多个文件，所以项目名称为key，列表为value，value是资源文件的集合
            for ch in source_info:
                # ch 代表一个调集单中的一项，如 ('并列不当', 'C:\\Users\\liyu\\Desktop\\李老师\\标准资料\\101病句\\10105')
                if ch[1] != None:  # 表示找到了文件地址，文件存在
                    work_dic[ch[0]] = []
                    for file in os.listdir(ch[1]):  # 列出文件夹下所有文件
                        if not os.path.isdir(os.path.join(ch[1], file)):  # 排除文件夹
                            if (file.split('.')[1] in cg.source_suffix) and (file[:2] != '~$'):  # 选中指定格式文件，滤除临时文件
                                self.set_shortcut(os.path.join(ch[1], file), os.path.join(target_dir, file))
                                work_dic[ch[0]].append(file)
                else:
                    bad_list.append(ch[0])
            # 把记录写入课程表
            if not len(bad_list) > 0:
                course_code = self.__get_course_code(new_class_code)
                source_code = self.__get_source(work_dic)
                class_time = orm.myTime(class_time, self.msg).time  # 778280
                self.msg.insert(0,
                                self.save_course(course_code, new_class_code, source_code, class_time))
            else:
                str1 = '%s班调集资源未全部完成，没有写入课程记录，失败资源如下：' % new_class_code
                self.msg.append(str1)
                for ch in bad_list:
                    self.msg.insert(0,ch)

    def __get_source(self, workdic):  # 把调集到的课程变成字符串
        source_list = list(workdic.keys())
        return '//'.join(source_list)

    def get_history_floder(self, new_class_code, class_time):  # 根据班号获取班级文件夹所在地址，同时根据时间创建上课文件夹
        floders = os.listdir(cg.history_path)
        for floder in floders:
            class_floder_path = os.path.join(cg.history_path, floder)
            if os.path.isdir(class_floder_path):
                if new_class_code == floder.split('_')[1]:  # 找到班级文件夹
                    for time_floder in os.listdir(class_floder_path):
                        if time_floder == class_time:  # 找到class_time文件夹
                            return os.path.join(class_floder_path, time_floder)
                    class_time_floder = os.path.join(class_floder_path, orm.myTime(class_time, self.msg).time4floder)
                    try:
                        os.mkdir(class_time_floder)  # 创建不存在的文件夹
                    except:
                        self.msg.insert(0, '文件夹已经存在')
                    return class_time_floder
        return None

    def save_course(self, course_code, new_class_code, source_code, class_time):  # 向数据库中写入课程信息
        course_list = []
        course_list.append(
            orm.Course(course_code=course_code, new_class_code=new_class_code, source_code=source_code,
                       class_time=class_time))
        self.db.insert(*course_list)
        return '%s班新增课程信息成功：%s' % (new_class_code, source_code)

    def set_shortcut(self, filename, lnkname):  # 如无需特别设置图标，则可去掉iconname参数，创建超链接
        shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        shortcut.SetPath(filename)

        if os.path.splitext(lnkname)[-1] != '.lnk':
            lnkname += ".lnk"
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)

    def __get_course_code(self, new_class_code):  # 构造课程信息的course_code项
        data = self.db.query(orm.Course.course_code, orm.Course.new_class_code == new_class_code,
                             orm.Course.course_code)
        if data.count() == 0:
            return str(new_class_code) + '001'
        else:
            return str(int(data[-1][0]) + 1)
