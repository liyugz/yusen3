# 备课框架

import tkinter as tk  # 使用Tkinter前需要先导入
import threading
from PrepareLessons import gather_source as gs
import transfer_message as tm
import time
from multiprocessing import Process


class LabelxEntry():
    def __init__(self, frame, label_text, x, y):
        '''
        window:附着的窗口
        label_text:label控件显示的文本
        x:联合组件距离窗口左部边缘的距离
        y:联合组件距离窗口顶部边缘的距离
        '''
        self.frame = frame
        self.label_text = label_text
        self.x = x
        self.y = y

        self.label = self.create_label()
        self.entry = self.create_entry()

    def create_label(self):
        l = tk.Label(self.frame, text=self.label_text, font=('宋体', 12), width=10, height=1, anchor='e')
        l.grid(row=self.x, column=self.y, pady=12, padx=20)
        return l

    def create_entry(self):
        e = tk.Entry(self.frame, width=60, show=None)  # 显示成明文形式
        e.grid(row=self.x, column=self.y + 1, pady=12)
        return e

    def getwd(self):
        return self.entry.get()


class LabelxText():
    def __init__(self, frame, label_text, x, y):
        '''
        window:附着的窗口
        label_text:label控件显示的文本
        x:联合组件距离窗口左部边缘的距离
        y:联合组件距离窗口顶部边缘的距离
        '''
        self.frame = frame
        self.label_text = label_text
        self.x = x
        self.y = y

        self.label = self.create_Label()
        self.text = self.create_Text()

    def create_Label(self):
        l = tk.Label(self.frame, text=self.label_text, font=('宋体', 12), width=10, height=1, anchor='e')
        l.grid(row=self.x, column=self.y, pady=12, sticky=tk.N, padx=20)
        return l

    def create_Text(self):
        t = tk.Text(self.frame, width=60, height=10)
        t.grid(row=self.x, column=self.y + 1, pady=12)
        return t

    def getwd(self):
        return self.text.get('0.0', 'end')

    def delete(self):
        self.label.destroy()


class Btn():
    def __init__(self, frame, btn_text, x, y, fun):
        '''
        :param btn_text: 按钮上的文字
        :param x: 组件距离窗口左部边缘的距离
        :param y: 组件距离窗口顶部边缘的距离
        :return:
        '''
        self.frame = frame
        self.btn_text = btn_text
        self.x = x
        self.y = y
        self.fun = fun

        self.b = self.create_button(self.frame, self.btn_text, self.x, self.y, self.fun)

    def create_button(self, frame, btn_text, x, y, fun):
        b1 = tk.Button(frame, text=btn_text, width=10,
                       height=2, command=fun)
        b1.grid(row=x, column=y, sticky=tk.W, pady=10)
        return b1


class MakeCourse():
    def __init__(self, window, db, msg):
        self.window = window
        self.frame1 = tk.Frame(window, height=300, width=600)
        self.frame1.grid(row=1, column=0, pady=50, sticky=tk.S + tk.N)
        self.raw_msg = msg

        self.db = db

        self.le1 = LabelxEntry(self.frame1, '班号：', 1, 0)
        self.le2 = LabelxEntry(self.frame1, '上课时间：', 2, 0)
        self.lt1 = LabelxText(self.frame1, '课程内容：', 3, 0)
        self.b1 = Btn(self.frame1, '开始备课', 4, 1, self.handle_raw_data)

        # 创建信息展示窗口
        self.msg = tk.StringVar()
        self.show_info = tk.Label(self.frame1, textvariable=self.msg, width=50, height=17, bg='black', fg='white',
                                  anchor='nw', justify='left', font=('宋体', 10))
        self.show_info.grid(row=1, column=2, pady=12, rowspan=5, sticky=tk.N, padx=50)
        self.show_info.after(1000, self.get_msg)

        tm.current_frame.append(self)

    def get_raw_data(self):
        new_class_code = self.le1.getwd()
        class_time = self.le2.getwd()
        course_plan = self.lt1.getwd()
        raw_data = [new_class_code, class_time, course_plan]
        return raw_data

    def handle_raw_data(self):
        raw_data = self.get_raw_data()
        t1 = threading.Thread(target=gs.CourceNode, args=(raw_data, self.raw_msg, self.db))
        t1.start()
        t1.join()

    def get_msg(self):
        info_str = '\n'.join(self.raw_msg)
        self.msg.set(info_str)
        self.show_info.after(1000, self.get_msg)

    def destory(self):
        self.frame1.destroy()
