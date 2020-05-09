from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo
from login import Login
from register import Person
from peoplemsg import PeopleMsg
from personmsg import PersonMsg
import os, sys
'''
    主界面模块
'''


class MainFrame(Frame):
    def __init__(self, parent=None, i_action=None, p_action=None):
        Frame.__init__(self, parent)
        Button(self, text='账号信息管理', command=i_action).pack(side=TOP, fill=BOTH)
        Button(self, text='用户资料管理', command=p_action).pack(side=TOP, fill=BOTH)
        Button(self, text='退出', command=self.quit).pack(side=TOP, fill=BOTH)


class Main(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.log = Login(self, 'person', self.action)
        self.log.pack()
        self.main_frame = MainFrame(self, self.i_action, self.p_action)
        self.people_msg = PeopleMsg(self, 'people', self.root_action)
        self.reg = Person(self, 'person', self.root_action)
        self.master.bind('<Return>', lambda event: self.log.onLogin())
        self.lab = Label(self, text='管理员账户：用户名：admin	密码：123456')
        self.lab.pack(anchor=SW)

    def action(self):           # 载入主界面
        self.per_msg = PersonMsg(self, 'person', self.root_action, self.log.name)
        self.master.unbind('<Return>')
        self.lab.pack_forget()
        self.make_menu()
        Label(self.master, text='当前用户：%s' % self.log.name).pack(side=BOTTOM)
        self.main_frame.pack()

    def i_action(self):         # 载入账号信息管理界面
        self.main_frame.pack_forget()
        if not self.log.admin:
            self.per_msg.alt_pass.pack(side=TOP, fill=BOTH)
            self.per_msg.del_name.pack_forget()
        self.per_msg.pack()

    def p_action(self):         # 载入用户资料管理界面
        self.main_frame.pack_forget()
        if not self.log.admin:
            self.people_msg.alt_inf.pack_forget()
            self.people_msg.del_inf.pack_forget()
            self.people_msg.clr_inf.pack_forget()
        self.people_msg.pack()

    def root_action(self):         # 重新载入主界面
        self.main_frame.pack()

    def make_menu(self):
        self.top = Menu(self)
        self.master.config(menu=self.top)
        per = Menu(self.top, tearoff=False)
        if self.log.admin:
            per.add_command(label='注册', command=self.register)
        per.add_command(label='注销', command=self.breaking)
        per.add_command(label='退出', command=self.quit)
        self.top.add_cascade(label='账户', menu=per)
        help = Menu(self.top, tearoff=False)
        help.add_command(label='帮助信息', command=self.help_text)
        help.add_command(label='关于', command=self.about)
        self.top.add_cascade(label='帮助', menu=help)

    def register(self):         # 注册界面显示
        self.main_frame.pack_forget()
        self.people_msg.pack_forget()
        self.per_msg.pack_forget()
        self.reg.pack()

    def breaking(self):         # 注销操作
        os.execl(sys.executable, sys.executable, *sys.argv)

    def help_text(self):         # 帮助文档
        new_win = Toplevel(self)
        text = ScrolledText(new_win)
        text.pack()
        msg = '''
    非管理员用户无法进行修改，删除操作。
    
    管理员用户可在菜单栏账户一栏看见注册功能。
    
    注册功能可注册一个普通用户。
    
    小软件没与数据库对接，文件均保存在people(用户资料)和person(账号资料)。
        '''
        text.insert('1.0', msg)
        center_window(new_win, 550, 150)

    def about(self):            # 关于
        about_text = '用户信息管理系统V1.3'
        showinfo(title='Tip', message=about_text)


def center_window(root, width, height):             # 窗口居中
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


if __name__ == '__main__':
    root = Tk()
    root.title('用户信息管理系统V1.3')
    center_window(root, 400, 300)
    Main(root)
    root.mainloop()
