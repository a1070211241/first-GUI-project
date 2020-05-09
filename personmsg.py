from tkinter import *
from tkinter.messagebox import showerror, showinfo, askyesno
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText
import queue
import shelve
import os
'''
    账号信息管理模块
'''


class PersonMsg(Frame):
    def __init__(self, parent=None, file=None, action=None, name=None):
        Frame.__init__(self, parent)
        self.file = file
        self.action = action
        self.name = name
        self.ent_queue = queue.Queue()
        self.name_list = ['用户名', '密码']
        self.make_button()

    def make_button(self):
        Button(self, text='所有账号', command=self.search_text).pack(side=TOP, fill=BOTH)
        self.alt_pass = Button(self, text='修改密码', command=self.alter_text)
        self.del_name = Button(self, text='删除账号', command=self.delete_text)
        self.del_name.pack(side=TOP, fill=BOTH)
        Button(self, text='返回', command=self.quit).pack(side=BOTTOM, fill=BOTH)

    def search_text(self):
        new_win = Toplevel(self)
        text = ScrolledText(new_win)
        text.pack()
        data_file = shelve.open(self.file)
        for key in data_file:
            text.insert('end', '用户名：%s\n' % key)
            text.see('end')
            text.update()
        data_file.close()
        size = '%dx%d+%d+%d' % \
               (170, 300, (new_win.winfo_screenwidth() - 170) / 2, (new_win.winfo_screenheight() - 300) / 2)
        new_win.geometry(size)

    def alter_text(self):
        self.alter_information(self.name)

    def delete_text(self):
        if os.path.exists(self.file):
            showerror(title='警告', message='无账号信息文件！')
            return
        num = askstring(title='Tip', prompt='请输入要删除的账号：')
        if not num:
            return
        data_file = shelve.open(self.file)
        if askyesno(title='警告', message='将要删除账号：\n' + num):
            data_file.pop(num)
            showinfo(title='Tip', message='账号 (%s) 已删除！' % num)
        data_file.close()

    def quit(self):             # 返回上一级
        if self.action is None:
            Frame.quit(self)
        else:
            self.pack_forget()
            self.action()

    def alter_information(self, num):  # 信息输入窗口
        new_win = Toplevel(self)
        i = 0
        ent_list = []
        for name in self.name_list:
            Label(new_win, text=name + ': ', width=25, relief=RIDGE).grid(row=i, column=0)
            ent = Entry(new_win, width=50, relief=SUNKEN)
            ent.grid(row=i, column=1)
            ent_list.append(ent)
            i += 1
        ent_list[0].insert('end', str(num))
        ent_list[0].config(state='readonly')
        size = '%dx%d+%d+%d' % \
               (530, 75, (new_win.winfo_screenwidth() - 530) / 2, (new_win.winfo_screenheight() - 75) / 2)
        new_win.geometry(size)

        def yes():
            data_file = shelve.open(self.file)
            data_file[ent_list[0].get()] = ent_list[1].get()
            data_file.close()
            showinfo(title='Tip', message='密码修改成功！')
            new_win.destroy()

        def no():
            new_win.destroy()

        Button(new_win, text='确定！', command=yes).grid(row=len(self.name_list), column=0)
        Button(new_win, text='取消！', command=no).grid(row=len(self.name_list), column=1)
        new_win.bind('<Return>', lambda event: yes())


if __name__ == '__main__':
    root = Tk()
    PersonMsg(root).pack()
    root.mainloop()
