import turtle as tl

# 设置笔刷宽度
tl.width(2)

# 向前距离
tl.forward(2)

# 右转
#tl.right(90)
tl.forward(2)

# 笔刷颜色
tl.pencolor('red')
tl.forward(2)

# 窗口等待操作,而不是马上关闭
# tl.done()

# 画五角星

tl.pencolor('red')
for x in range(5):
    tl.forward(100)
    tl.right(144)

# 画图练习
tl.setpos(0,0)   # 设置笔起点位置
tl.color('red', 'yellow')
tl.begin_fill()
while True:
    tl.forward(200)
    tl.left(170)
    
    if abs(tl.pos()) < 1:   # 判断笔的当前坐标
        #
        break
tl.end_fill()

tl.done()