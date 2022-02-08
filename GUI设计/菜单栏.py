import tkinter as tk
from  tkinter import ttk  #导入内部包

class app():
    def __init__(self,):
        self.root = tk.Tk()
        self.menu_test()
        self.en1 = ttk.Entry(self.root)
        self.en1.pack()
        self.R_click_menu()
        self.root.bind('<Button-3>', self.R_click)

    def menu_test(self,):
        menubar = tk.Menu(self.root)   # 创建一个菜单组件

        fmenu = tk.Menu(menubar, tearoff=0)  # 在菜单下创建1个子菜单,并添加了 打开/保存, tearoff是指菜单是否可以独立
        fmenu.add_command(label='打开',)
        fmenu.add_command(label='保存',)

        menubar.add_cascade(label='文件', menu=fmenu)   # 在菜单组件上创建了 文件,链接到 子菜单fmenu上

        Emenu = tk.Menu(menubar, tearoff=0)
        Emenu.add_command(label='复制', )
        Emenu.add_command(label='粘贴', )
        menubar.add_cascade(label='编辑', menu=Emenu)

        self.root.config(menu=menubar)  # 窗体上配置菜单栏,menubar

    def R_click_menu(self,):
        def copy_1(x):
            self.root.clipboard_clear()
            self.root.clipboard_append(x)
        def copy_2():   # 对应可以用鼠标选中的文本,可以直接调用本身的事件 复制/粘贴/剪切命令.
            self.en1.event_generate("<<Copy>>")

        self.R_menu = tk.Menu(self.root, tearoff=0)   #创建一个菜单组件
        self.R_menu.add_command(label='复制', command=lambda: copy_1(
            self.x))  # 使用lambda 来对函数传入参数,因为在这调用时不能直接加括号,否则在刚运行时就被执行
        self.R_menu.add_separator()
        self.R_menu.add_command(label='文本框复制', command=copy_2)
        self.R_menu.add_separator()

    def R_click(self, event):  # 定义一个和右键动作绑定的函数,便于传递参数
        self.x=self.en1.get()
        self.R_menu.post(event.x_root, event.y_root)    #

op=app()
op.root.mainloop()

'''
创建下拉菜单的步骤如下：

(1)创建顶层菜单
menubar=tk.Menu(root)
(2)创建子菜单或者下拉菜单
filemenu=tk.Menu(menubar)
(3)子子菜单中添加菜单项
filemenu.add_command(label=’打开文件’,command=open_file)
filemenu.add_command(label=’关闭文件’,command=close_file)
(4)关联级联菜单
menubar.add_cascade(label=‘文件’, menu=filemenu)
(5)关联窗口
root.config(menubar)
'''