# -*- coding: utf-8 -*-


import tkinter as tk  # 使用Tkinter前需要先导入
from PrepareLessons import update_source_database as usd
import common_parameters as cp

# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('yusen_system')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('1000x600')  # 这里的乘是小x

var = tk.StringVar()



Label1 = tk.Label(window, textvariable=var, bg='white', font=('Arial', 12), width=30, height=2)
Label1.place(x=50, y=30, anchor='nw')


# 第5步，在窗口界面设置放置Button按键
beike = tk.Button(window, text='备课', font=('Arial', 12), width=10, height=1, command=usd.Source)
beike.place(x=50, y=100, anchor='nw')

# 添加文字信息


# 第6步，主窗口循环显示
window.mainloop()
