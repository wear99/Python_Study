# -*- coding:utf-8 -*-

# 程序入口
# 需将GUI中函数与数据处理函数进行对应

from core.MainPage import main_GUI
from core.DataHandler import dataHandler
import tkinter as tk

mod = dataHandler()

root = tk.Tk()
main_GUI(root, mod)
root.mainloop()




