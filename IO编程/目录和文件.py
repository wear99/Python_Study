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

def all_file(patch):
    def get_file(patch):
        files = [x for x in os.listdir(patch)]    #列出当前目录下所有内容
        patchs = [os.path.join(patch, x) for x in files]  #拼接出当前目录下所有路径
        
        for item in patchs:
            if os.path.isfile(item):
                fname = os.path.basename(item)
                lname=os.path.splitext(item)[1]
                if lname in ('.txt'):                
                    name=fname.replace(lname,'')
                    all_file[name]=item
            elif os.path.isdir(item):
                get_file(item)

    all_file = {}
    get_file(patch)
    return all_file


#所有目录=[]
#s=os.path.abspath('.')
#all_dir(s)
p='D:\\work\\python\\excel\\'
file=all_file(p)

for x,y in file.items():
    print(x,' : ',y)


