import tkinter as tk
import random

# 生成加减算式
def 算式生成(层数):
    数字 = random.randint(30, 85)
    习题 = str(数字)
    习题答案 = 数字

    for n in range(0, 层数):

        if random.randint(0, 10) < 5:

            数字 = random.randint(5, 90 - 习题答案)
            习题答案 = 习题答案 + 数字
            习题 += '+'
            习题 += str(数字)

        else:
            数字 = random.randint(4, 习题答案-5)
            习题答案 = 习题答案 - 数字
            习题 += '-'
            习题 += str(数字)
    return 习题, 习题答案

# 点击答题完毕后对结果和答案进行对比
def 答题完毕():
    n=0
    for i in range(1, 11):
        if int(输入框[i].get())!=习题答案集[i]:
            n+=1
    if n == 0:
        结果.set('恭喜你,全部答对了!')
    else:
        结果.set('共错了'+str(n)+'题'+'请再检查检查')


wd = tk.Tk()

wd.title('练习题')
wd.geometry('500x500')
# 将所有答案收集在list,便于核对成绩
习题答案集 = [0,]
输入框=[0,]

for i in range(1, 11):
    习题, 习题答案 = 算式生成(2)
    习题答案集.append(习题答案)

    lab1 = tk.Label(wd, text=str(i) +'.  '+ 习题+' =')

    输入框.append(tk.Entry(wd))

    lab2 = tk.Label(wd, text=习题答案)

    lab1.place(x=15, y=i * 25)
    输入框[i].place(x=150,y=i * 25)
    lab2.place(x=400, y=i * 25)


tk.Button(wd, text="答题完成", command=答题完毕).pack(side='bottom')

结果 = tk.StringVar()
tk.Label(wd, textvariable=结果).pack(side='bottom')

wd.mainloop()
