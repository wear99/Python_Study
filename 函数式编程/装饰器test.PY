import time

def 运行时间(fun):
    def 计算时间(*arges,**kargs):
        print(fun.__name__,'开始运行')
        stime=time.time()
        x=fun(*arges,**kargs)
        etime=time.time()
        print(fun.__name__,'结束运行')
        print('运行时间是: ',etime-stime)
        return x
    return 计算时间

@运行时间
def ss(a):
    m=1
    for n in a:
        m=n*m
    
    time.sleep(3)
    return m

mylist=list(range(1,100))


print(ss(mylist))