#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename

'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
'''


class Login(tk.Frame):
    def __init__(self, master=None, verify_file=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.__verify_file = verify_file
        self.__user_value = tk.StringVar()
        self.__password_value = tk.StringVar()
        self.__verify_value = tk.StringVar()

        self.__username = None
        self.__password = None
        self.__verify_code = None

        self.__create_widgets()

    def __create_widgets(self):
        tk.Label(self, text='用户名').pack()
        tk.Entry(self, textvariable=self.__user_value).pack()

        tk.Label(self, text='密码').pack()
        tk.Entry(self, textvariable=self.__password_value).pack()

        if self.__verify_file:
            self.__verify_image = tk.PhotoImage(file=self.__verify_file)
            tk.Label(self, image=self.__verify_image).pack()
            tk.Entry(self, textvariable=self.__verify_value).pack()

        self.__confirm = tk.Button(self, text='确定')
        self.__confirm.bind('<Button-1>', self.__get_value)
        self.__confirm.pack()

    def __get_value(self, *args):
        self.__username = self.__user_value.get()
        self.__password = self.__password_value.get()
        self.__verify_code = self.__verify_value.get()
        self.master.destroy()

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_verify_code(self):
        return self.__verify_code


def get_login_info(verify=None):
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    root.geometry('210x245')
    app = Login(master=root, verify_file=verify)
    app.mainloop()
    return {
        'username': app.get_username(),
        'password': app.get_password(),
        'code': app.get_verify_code()
    }


class ChooseTarget(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        self.__choose_path = tk.StringVar()
        self.__path = None
        self.__choose_filename = tk.StringVar()
        self.__filename = None

        self.__create_widgets()

    def __create_widgets(self):
        tk.Label(self, text='目标路径').grid(row=0, column=0)
        tk.Entry(self, textvariable=self.__choose_path).grid(row=0, column=1)

        self.__directory = tk.Button(self, text='路径选择')
        self.__directory.grid(row=0, column=2)
        self.__directory.bind('<Button-1>', self.__get_path_value)

        tk.Label(self, text='目标文件').grid(row=1, column=0)
        tk.Entry(self, textvariable=self.__choose_filename).grid(row=1, column=1)

        self.__file = tk.Button(self, text='选择文件')
        self.__file.grid(row=1, column=2)
        self.__file.bind('<Button-1>', self.__get_filename_value)

        self.__confirm = tk.Button(self, text='确定', command=self.master.destroy)
        self.__confirm.grid(row=2, column=1)

    def __get_path_value(self, *args):
        self.__path = askdirectory()
        self.__choose_path.set(self.__path)

    def __get_filename_value(self, *args):
        self.__filename = askopenfilename()
        self.__choose_filename.set(self.__filename)

    def get_path(self):
        return self.__path

    def get_filename(self):
        return self.__filename


def get_choose_path():
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    app = ChooseTarget(root)
    app.mainloop()
    return app.get_path()


def get_choose_file():
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    app = ChooseTarget(root)
    app.mainloop()
    return app.get_filename()


if __name__ == '__main__':
    pass
