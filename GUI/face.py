import tkinter as tk
import orm

import frame1 as f1
import frame2 as f2


class MainWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('yusen')
        self.window.geometry('1000x500')
        self.window.resizable(0, 0)
        self.raw_msg = []

        self.db = orm.db(self.raw_msg)

        f1.Tab(self.window)
        f2.MakeCourse(self.window, self.db, self.raw_msg)  # 建立首页默认页

        self.window.mainloop()
        self.db.close()


if __name__ == '__main__':
    MainWindow()

