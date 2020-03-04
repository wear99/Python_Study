import os
# 读取目录中所有文件夹
def all_dir(目录):
    # [x for x in os.listdir(目录) if os.path.isdir(x)],这样对当前层有效,一旦进入第2层就会一直返回false.
    # isdir(),isfile() 里面用绝对路径比较安全

    所有文件=[x for x in os.listdir(目录)]
    所有路径=[os.path.join(目录,x) for x in 所有文件]
    for n in 所有路径:
        if os.path.isdir(n):
            所有目录.append(n)
            all_dir(n)         #递归调用,不断进入每层文件夹,再从头查找

所有目录=[]
s=os.path.abspath('.')
all_dir(s)
for x in 所有目录:
    print(x)


