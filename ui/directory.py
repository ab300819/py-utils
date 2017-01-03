#!/usr/bin/env python3
import tkinter as tk
from tkinter.filedialog import askdirectory


class ChooseDirectory(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.__choose_path = tk.StringVar()
        self.__path = None

        self.__create_widgets()

    def __create_widgets(self):
        tk.Label(self, text='目标路径').grid(row=0, column=0)
        tk.Entry(self, textvariable=self.__choose_path).grid(row=0, column=1)

        self.__choose = tk.Button(self, text='路径选择')
        self.__choose.grid(row=0, column=2)
        self.__choose.bind('<Button-1>', self.__get_value)

        self.__confirm = tk.Button(self, text='确定', command=root.destroy)
        self.__confirm.grid(row=1, column=1)

    def __get_value(self, *args):
        self.__path = askdirectory()
        self.__choose_path.set(self.__path)

    def get_path(self):
        return self.__path


def get_choose_path():
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    app = ChooseDirectory(master=root)
    app.mainloop()
    return app.get_path()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    # root.title('登陆信息')
    app = ChooseDirectory(master=root)
    app.mainloop()
    print(app.get_path())
