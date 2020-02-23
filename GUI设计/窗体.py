import tkinter as tk


# 读取new_nme的值,然后给var2. 也可以直接用entry名字来get
# stringvar本质是一个元组tuple,操作方法相同
def 按钮():
    var2.set(int(name.get())+1)
    var3.set(mylist[0].get())


# 实例化object，建立窗口wd
wd = tk.Tk()

# 第2步，给窗口的可视化起名字
wd.title('第一个界面')

# 第3步，设定窗口的大小(长 * 宽)
wd.geometry('500x300')

# 第4步，在图形界面上设定标签
l = tk.Label(wd, text='hello world!')
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高



# 第5步，放置标签
l.place(x=10, y=50)
# Label内容content区域放置位置，自动调节尺寸
# 放置lable的方法有：
# 1）l.pack(); 按上下左右的方式排列
# 2) l.place();  指定坐标
# 3） l.Grid(); 按方格坐标指定位置

# 设置一个按钮,当按下时执行 按钮 这个子程序,内容自己定义.
b = tk.Button(wd, text="hit me", command="按钮")
# 放置按钮
b.pack()

# 在图形界面上设定输入框控件entry并放置控件,将输入内容传递给new_nme,
# 可使用new_nme.get()或name.get()来获得具体内容
new_nme = tk.StringVar()
name=tk.Entry(wd, show='*', textvariable=new_nme)  # 显示成密文形式

name.pack()
new_pwd = tk.StringVar()
tk.Entry(wd, show=None, textvariable=new_pwd).pack()  # 显示成明文形式




var2 = tk.StringVar()

tk.Label(wd, textvariable=var2).pack()


mylist=[]
#将输入框传递给list,通常组件数量有限,不需要这样
mylist.append(tk.Entry(wd))

mylist[0].pack()

var3 = tk.StringVar()
tk.Label(wd, textvariable=var3).pack()

# 刷新窗口显示
wd.mainloop()
