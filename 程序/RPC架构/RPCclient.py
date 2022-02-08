# _*_ coding:utf-8 _*_

from xmlrpc.client import ServerProxy
from core.MainPage import main_GUI
import tkinter as tk

if __name__=="__main__":
    server = ServerProxy("http://127.0.0.1:8001", allow_none=True)
    #server = ServerProxy("http://localhost:9999", allow_none=True)
    root = tk.Tk()
    main_GUI(root, server)
    root.mainloop()



















