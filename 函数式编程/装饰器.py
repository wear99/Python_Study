# 装饰器就是闭包
# 我们想对一个函数增加一些功能，譬如记录调用时间等，但又不想去修改每一个函数。那么就可以通过闭包的形式，把这些功能附加到这个函数内。
# 这样当函数被调用时，就会自动代入了这些参数、数据。   这就是装饰器

# 应用场景：检查是否允许调用函数(装饰器内加判断)，记录函数logging
'''
基本结构：
def 装饰器名称(函数):
    @functools.wraps(函数)
    def 装饰器功能(*args,**kw):
        在调用函数前执行的语句

        f=函数(*args,**kw)

        在函数结束后执行的语句

        return f
    return 装饰器功能
'''

#想要在调用每个函数前打印'函数已被调用'
def ad(a,b):
    return a + b

def 装饰器(函数):     # 装饰器这个函数，可以接收一个函数名作为参数，然后通过闭包的形式
    def 打印(*args,**kw):    #表示可以接收不定参数，这样就可以适用于各种函数
        print(函数.__name__,' 被调用...')     # __name__是每个函数的属性，代表函数名
        return 函数(*args,**kw)
    
    return 打印                  #记住，当函数不带()时，只是个指向函数的变量，函数并没有被调用执行

f=装饰器(ad)     #f 指向装饰器，装饰器返回 打印，打印又返回了 ad,   所以f 此时就指向ad()，但同时又会执行 打印 这个函数
print(f(2, 5))


# 上述可以简单表示为
# @装饰器
# def 函数():
# 表示： 函数=装饰器(函数)

print('****************装饰器带参数，3层嵌套********************')
# 假如装饰器也要带参数，那就再嵌套一层
import functools

def log(s):
    def 装饰器1(函数):

        @functools.wraps(函数)        #用于把原函数的属性复制过来，否则现在 ssss 的属性是 打印1 的
                
        def 打印1(*args,**kw):
            print(函数.__name__,' 被调用... ',s)
            return 函数(*args,**kw)
        return 打印1
    return 装饰器1

@log('装饰器参数')
def ssss(a, b):
    print(a + b)

ssss(2,7)
print(ssss.__name__)  #如果不使用functools.wraps(函数)，那么打印出来的函数名就是 打印1

print('***************练习题，打印任何函数执行时间******************')

import time

def 时间装饰器(函数):
    @functools.wraps(函数)
    def 时间(*args,**kw):
        开始时间 = time.time()
        print(函数.__name__,'开始执行')
        
        f=函数(*args,**kw)

        结束时间=time.time()

        print('函数已结束，执行时间为 %f 秒' % (结束时间 - 开始时间))
        return f     # 此时f 指向的是函数的运行结果，而不是函数。如果这里写 return 函数(*args,**kw),那函数就会被再执行一边，并返回结果
    return 时间

@时间装饰器
def fast(x, y):
    time.sleep(0.0012)
    return x + y;

@时间装饰器
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

print(fast(11, 22))
print(slow(11, 22, 33))



        