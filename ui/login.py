#!/usr/bin/env python3

import tkinter as tk


class Application(tk.Frame):
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
        root.destroy()

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_verify_code(self):
        return self.__verify_code


def get_info(verify=None):
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    root.geometry('210x245')
    app = Application(master=root, verify_file=verify)
    app.mainloop()
    return [app.get_username(), app.get_password(), app.get_verify_code()]


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    root.geometry('210x245')
    app = Application(master=root)
    app.mainloop()
    print([app.get_username(), app.get_password(), app.get_verify_code()])
