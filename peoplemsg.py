from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesno, showerror, showinfo
from tkinter.simpledialog import askstring
import _thread as thread
import queue
import shelve
import os
'''
    用户资料管理模块
'''


class PeopleMsg(Frame):
    def __init__(self, parent=None, file=None, root_action=None):
        Frame.__init__(self, parent)
        self.file = file
        self.action = root_action
        self.name_list = ['编号', '姓名', '年龄', '手机号']
        self.ent_queue = queue.Queue()
        self.make_button()

    def make_button(self):
        Label(self, text='用户资料的维护及管理').pack(side=TOP, fill=BOTH)
        Button(self, text='添加信息', command=self.add_text).pack(side=TOP, fill=BOTH)
        Button(self, text='查询信息', command=self.search_text).pack(side=TOP, fill=BOTH)
        self.alt_inf = Button(self, text='修改信息', command=self.alter_text)
        self.alt_inf.pack(side=TOP, fill=BOTH)
        self.del_inf = Button(self, text='删除信息', command=self.delete_text)
        self.del_inf.pack(side=TOP, fill=BOTH)
        self.clr_inf = Button(self, text='清空信息', command=self.clear_text)
        self.clr_inf.pack(side=TOP, fill=BOTH)
        Button(self, text='返回', command=self.quit).pack(side=BOTTOM, fill=BOTH)

    def add_text(self):         # 添加用户资料
        self.text_check()
        thread.start_new_thread(self.set_information, ())

    def search_text(self):      # 查询用户资料
        if os.path.exists(self.file):
            showerror(title='警告！', message='无用户信息文件！')
            return
        new_win = Toplevel()
        text = ScrolledText(new_win)
        text.config(width=610)
        text.pack()
        f = shelve.open(self.file)
        for key in f:
            text.insert('end', '%s\t=>\n\t%s\n' % (key, f[key]))
            text.see('end')
            text.update()
        f.close()
        size = '%dx%d+%d+%d' % \
               (630, 230, (new_win.winfo_screenwidth() - 630) / 2, (new_win.winfo_screenheight() - 230) / 2)
        new_win.geometry(size)

    def alter_text(self):       # 修改用户资料
        num = askstring(title='Tip', prompt='请输入要修改的用户编号：')
        if not num:
            return
        if num not in shelve.open(self.file):
            showerror(title='错误', message='该用户信息不存在！')
            return
        thread.start_new_thread(self.alter_information, (num, ))

    def delete_text(self):      # 删除用户资料
        if os.path.exists(self.file):
            showerror(title='警告', message='无用户信息文件！')
            return
        num = askstring(title='Tip', prompt='请输入要删除的用户编号：')
        if not num:
            return
        data_file = shelve.open(self.file)
        if num in data_file:
            msg = '%s\t=> %s\n' % (num, data_file[num])
            if askyesno(title='警告', message='将要删除用户信息：\n' + msg):
                data_file.pop(num)
                showinfo(title='Tip', message='用户编号 (%s) 已删除！' % num)
        else:
            showerror(title='错误', message='用户编号 (%s) 不存在' % num)
        data_file.close()

    def clear_text(self):       # 清空所有用户资料
        if os.path.exists(self.file):
            showerror(title='警告', message='无用户信息文件！')
            return
        if askyesno(title='警告', message='确定要清空用户信息吗？'):
            data_file = shelve.open(self.file)
            data_file.clear()
            data_file.close()
            showinfo(title='Tip', message='用户信息已清空。')
        else:
            showinfo(title='Tip', message='操作已取消。')

    def quit(self):             # 返回上一级
        if self.action is None:
            Frame.quit(self)
        else:
            self.pack_forget()
            self.action()

    def set_information(self):  # 信息输入窗口
        new_win = Toplevel(self)
        i = 0
        ent_list = []
        for name in self.name_list:
            Label(new_win, text=name + ': ', width=25, relief=RIDGE).grid(row=i, column=0)
            ent = Entry(new_win, width=50, relief=SUNKEN)
            ent.grid(row=i, column=1)
            ent_list.append(ent)
            i += 1
        ent_list[0].focus_set()
        size = '%dx%d+%d+%d' % (
                530, 120, (new_win.winfo_screenwidth() - 530) / 2, (new_win.winfo_screenheight() - 120) / 2)
        new_win.geometry(size)

        def yes():
            self.ent_queue.put(ent_list)
            ask = askyesno(title='确定退出', message='需要继续输入吗？')
            if not ask:
                self.ent_queue.put(False)
                new_win.destroy()
            else:
                for i in range(len(ent_list)):
                    ent_list[i].delete(0, 'end')
                ent_list[0].focus_set()
                new_win.focus_set()

        def no():
            self.ent_queue.put(False)
            new_win.destroy()

        Button(new_win, text='确定！', command=yes).grid(row=len(self.name_list), column=0)
        Button(new_win, text='取消！', command=no).grid(row=len(self.name_list), column=1)
        new_win.bind('<Return>', lambda event: yes())

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
        ent_list[1].focus_set()
        size = '%dx%d+%d+%d' % \
               (530, 120, (new_win.winfo_screenwidth() - 530) / 2, (new_win.winfo_screenheight() - 120) / 2)
        new_win.geometry(size)

        def yes():
            self.ent_queue.put(ent_list)
            showinfo(title='Tip', message='用户编号 (%s) 修改成功！' % num)
            self.ent_queue.put(False)
            new_win.destroy()

        def no():
            self.ent_queue.put(False)
            new_win.destroy()

        Button(new_win, text='确定！', command=yes).grid(row=len(self.name_list), column=0)
        Button(new_win, text='取消！', command=no).grid(row=len(self.name_list), column=1)
        new_win.bind('<Return>', lambda event: yes())

    def text_check(self, delayMsecs=100):  # 录入来自输入窗口输入的信息
        try:
            ent_list = self.ent_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            if ent_list is False:
                return
            data = dict()
            for i in range(len(self.name_list)):
                data[self.name_list[i]] = ent_list[i].get()
            data_file = shelve.open(self.file)
            data_file[data[self.name_list[0]]] = data
            data_file.close()
        self.after(delayMsecs, lambda: self.text_check(delayMsecs))


if __name__ == '__main__':
    def main():
        b.pack_forget()
        PeopleMsg(root, file='people').pack()
    root = Tk()
    root.geometry('300x400')
    b = Button(root, text='press', command=main)
    b.pack()
    root.mainloop()
