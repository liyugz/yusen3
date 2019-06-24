# 备课框架

import tkinter as tk  # 使用Tkinter前需要先导入
import threading
from PrepareLessons import gather_source as gs, update_source_database as usd
import transfer_message as tm
from tkinter import ttk
import orm


class LabelxCombobox():
    def __init__(self, frame, label_text, x, y, listx):
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
        self.cmb = self.create_combobox(listx)

    def create_label(self):
        l = tk.Label(self.frame, text=self.label_text, font=('Times New Roman', 12), width=10, height=1, anchor='e')
        l.grid(row=self.x, column=self.y, pady=12, padx=20)
        return l

    def create_combobox(self, listx):
        e = ttk.Combobox(self.frame, width=60, show=None)  # 显示成明文形式
        e['values'] = listx
        e.grid(row=self.x, column=self.y + 1, pady=12, columnspan=5)
        return e

    def getwd(self):
        return self.cmb.get()


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
        l = tk.Label(self.frame, text=self.label_text, font=('Times New Roman', 12), width=10, height=1, anchor='e')
        l.grid(row=self.x, column=self.y, pady=12, padx=20)
        return l

    def create_entry(self):
        e = tk.Entry(self.frame, width=60, show=None)  # 显示成明文形式
        e.grid(row=self.x, column=self.y + 1, pady=12, columnspan=5)
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
        l = tk.Label(self.frame, text=self.label_text, font=('Times New Roman', 12), width=10, height=1, anchor='e')
        l.grid(row=self.x, column=self.y, pady=12, sticky=tk.N, padx=20)
        return l

    def create_Text(self):
        t = tk.Text(self.frame, width=60, height=10)
        t.grid(row=self.x, column=self.y + 1, pady=12, columnspan=5)
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
                       height=2, command=fun, font=('Times New Roman', 11))
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
        self.b2 = Btn(self.frame1, '更新资源', 4, 2, self.update_source)

        # 创建信息展示窗口
        self.msg = tk.StringVar()
        self.show_info = tk.Text(self.frame1, width=50, height=17, bg='white', fg='#0000FF',
                                 font=('Times New Roman', 11))
        self.show_info.grid(row=1, column=6, pady=12, rowspan=5, sticky=tk.N, padx=50)
        label_on_info = tk.Label(self.frame1, text='滚动信息窗口', font=('宋体', 11, 'bold'), width=11,
                                 height=1, anchor='w', fg='#0000FF')
        label_on_info.grid(row=0, column=6, sticky=tk.W, padx=45)
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
        usd.Source(self.db, self.raw_msg)
        t1 = threading.Thread(target=gs.CourceNode, args=(raw_data, self.raw_msg, self.db))
        t1.start()
        t1.join()

    def update_source(self):
        usd.Source(self.db, self.raw_msg)

    def get_msg(self):
        info_str = '\ninfoline：'.join(self.raw_msg)
        info_str = 'infoline：' + info_str
        self.show_info.delete(0.0, tk.END)
        self.show_info.insert('insert', info_str)
        self.show_info.after(1000, self.get_msg)

    def get_class_info(self):
        list = self.db.query_all(orm.NewClass.new_class_code)
        return list

    def destory(self):
        self.frame1.destroy()
