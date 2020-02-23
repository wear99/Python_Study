# 系统内已自带了很多函数,类似 abs max sum之类
# 自己定义函数
def 乘法(m, n):
    # 要执行的语句,
    # 通常要对传入的参数类型是否正确进行检查
    if isinstance(m, (int, float)) and isinstance(n, (int, float)):
        return m * n
    else:
        print('不是数字格式')

    # return 是返回的值,可以不要,则返回None


print(乘法(2, 'a'))

print("---------------------")

def 一元二次方程求解(a, b, c):
    # 首先检查参数是否是数字格式
    for x in [a, b, c]:
        if not isinstance(x, (int, float)):
            return '不是数字格式'

    if b * b < 4 * a * c:
        return '方程无实数解'
    else:
        return (-b + (b*b-4 * a * c)**0.5) / (2 * a), (-b -
                                                   (b*b-4 * a * c)**0.5) / (2 * a)
# 返回多个值时,实际上是1个元组(,).  如果外部有相同数量的变量对接,则会对应赋值


x0 = 一元二次方程求解(5, 10, 2)
x1, x2 = 一元二次方程求解(5, 10, 2)

print('x0=', x0)
print('x1=', x1)
print('x2=', x2)

'''
小结
定义函数时，需要确定函数名和参数个数；

如果有必要，可以先对参数的数据类型做检查；

函数体内部可以用return随时返回函数结果；

函数执行完毕也没有return语句时，自动return None。

函数可以同时返回多个值，但其实就是一个tuple。
'''
