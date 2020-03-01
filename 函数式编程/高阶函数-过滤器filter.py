# filter()函数用于过滤序列
# 和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
#注意filter()函数返回的是一个迭代器Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果，需要用list()函数获得所有结果并返回list

def no_empty(s):
    return s and s.strip()    #字符之间用 and，s为true，则返回s.spilt()，否则返回s
    # strip() 用于移除字符串头尾指定的字符（默认为空格）或字符序列,中间的不会删除。
    # 注意删除多个字符时：只要头尾有对应其中的某个字符即删除，不考虑顺序

print(list(filter(no_empty,['a','c','','d',None,' '])))

print('***********练习 计算素数************')
# 埃氏筛法，用2，3，4...不断的向后筛除他们的倍数，最终留下来的就是素数
def 生成序列():
    n = 1
    while True:
        n += 1
        yield n

def 倍数(n):  #闭包函数，2个函数套起来。当第一次调用倍数时，代入了参数n,然后返回一个内层 函数，这时可以接收一个参数 x。
              #  实现了map/filter中函数只能一个参数的限制
    def 内层(x):
            if x % n > 0:
                return x
    return 内层
    #return lambda x: x % n > 0    ，这是闭包函数简单写法，直接用lambda 来代替def 定义的函数

def 筛选():
    num = 生成序列()  
    while True:
        n = next(num)
        yield n
        num=filter(倍数(n),num)
 
for x in 筛选():
    if x < 100:
        print(x)
    else:
        break

print('*************生成素数 方法2***********')

def 筛选1(n):
    def 倍数检查(x):                 # 一个变量如果本函数下未定义，则自动去外层函数查找
        if x % n != 0 or x == n:
            return True

    global 序列
    序列 = list(filter(倍数检查, 序列))


序列 = list(range(2, 100))

list(map(筛选1, 序列))
print(序列)


print('************练习题 回数******************')
# 回数是指从左向右读和从右向左读都是一样的数
# 思路，利用字符串的反转函数，如果反转后相同，则为回数

def 回数(s):
    #if str(s) == str(s)[::-1]:    #反转方法：切片法; 函数法，先用list转为列表，再用reverse()反转，再用join组合："".join(list)
    return str(s) == str(s)[::-1]
    
l=list(range(1,1000))
print(list(filter(回数,l)))

