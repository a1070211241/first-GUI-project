from tkinter import *
from tkinter.messagebox import showerror
import shelve
'''
    登录界面模块
'''


class Login(Frame):
    NAME = 'admin'
    PASSWORD = '123456'

    def __init__(self, parent=None, file=None, action=None):
        Frame.__init__(self, parent)
        self.pack()
        self.file = file                # 账号资料文件
        self.action = action            # 页面跳转回调函数
        self.admin = False              # 是否以管理员账户登录
        self.name = None
        Label(self, text='登录界面').pack(side=TOP)
        self.login()
        Button(self, text='登录！', command=self.onLogin).pack(side=LEFT)
        Button(self, text='退出！', command=self.quit).pack(side=RIGHT)

    def login(self):
        l = Frame(self)
        l.pack(side=TOP)
        Label(l, text='用户名：', width=20, relief=RIDGE).grid(row=0, column=0)
        self.ent_name = Entry(l, width=50, relief=SUNKEN)
        self.ent_name.grid(row=0, column=1)
        self.ent_name.focus_set()
        Label(l, text='密码：', width=20, relief=RIDGE).grid(row=1, column=0)
        self.ent_pass = Entry(l, width=50, relief=SUNKEN)
        self.ent_pass.grid(row=1, column=1)

    def onLogin(self):
        try:
            f = shelve.open(self.file)
            if str(f[self.ent_name.get()]) == str(self.ent_pass.get()):
                self.pack_forget()
                self.name = self.ent_name.get()
                self.action()
                f.close()
            else:
                f.close()
                raise Exception
        except Exception:
            if str(self.ent_name.get()) == Login.NAME and str(self.ent_pass.get()) == Login.PASSWORD:
                self.admin = True
                self.name = self.ent_name.get() + ' (管理员) '
                self.pack_forget()
                self.action()
            else:
                showerror('登录失败！', '用户名或密码错误！')


if __name__ == '__main__':
    Login().mainloop()
