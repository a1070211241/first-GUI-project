from tkinter import *
from tkinter.messagebox import showerror, showinfo
from tkinter.messagebox import askyesno
import shelve
'''
    注册账号模块
'''


class Person(Frame):
    def __init__(self, parent=None, file=None, root_action=None):
        Frame.__init__(self, parent)
        self.name_list = ['用户名', '密码']
        self.file = file
        self.action = root_action
        self.set_information()

    def set_information(self):
        i = 0
        ent_list = []
        for name in self.name_list:
            Label(self, text=name + ': ', width=25, relief=RIDGE).grid(row=i, column=0)
            ent = Entry(self, width=50, relief=SUNKEN)
            ent.grid(row=i, column=1)
            ent_list.append(ent)
            i += 1

        def yes():
            if not ent_list[0].get() or not ent_list[1].get():
                showerror(title='警告', message='用户名或密码不能为空！')
                return
            elif ent_list[0].get() == 'admin':
                showerror(title='警告', message='用户名不能为管理员用户！')
                return
            a = askyesno(title='Tip', message='确认注册用户 (%s) 吗？' % ent_list[0].get())
            if not a:
                return
            file = shelve.open(self.file)
            file[ent_list[0].get()] = ent_list[1].get()
            file.close()
            showinfo(title='Tip', message='用户 (%s) 注册成功！' % ent_list[0].get())
            self.pack_forget()
            self.action()

        def no():
            self.pack_forget()
            self.action()

        Button(self, text='确定！', command=yes).grid(row=len(self.name_list), column=0)
        Button(self, text='取消！', command=no).grid(row=len(self.name_list), column=1)


if __name__ == '__main__':
    root = Tk()
    Person(root, 'person').pack()
    root.mainloop()
