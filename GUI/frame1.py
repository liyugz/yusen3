# 选项卡框架，顶部按钮，模拟选项卡功能

import tkinter as tk  # 使用Tkinter前需要先导入
import frame2 as f2
import transfer_message as tm


class Tab():
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, height=300, width=600)
        self.frame.grid(row=0, column=0, columnspan=6)

        self.create_tab(self.command1, '备课', 0)
        self.create_tab(self.command2, '评分', 1)
        self.create_tab(self.command3, '机器人', 2)

    def create_tab(self, fcn, tab_text, y):
        tab = tk.Button(self.frame, text=tab_text, width=47,
                        height=1, command=fcn)
        tab.grid(row=0, column=y)
        return tab

    def command1(self):
        for ch in tm.current_frame:
            ch.destory()
        tm.current_frame.clear()
        f2.MakeCourse(self.window)

    def command2(self):
        print('ok')

    def command3(self):
        print('ok')
