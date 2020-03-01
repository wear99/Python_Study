# -*- coding: utf-8 -*-

# 一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数
# 函数名就是一个指向函数的变量，当加()时代表调用函数，不加()则是一个变量
from functools import reduce


def 绝对值加法(a, b, f):
    return f(a) + f(b)

print(绝对值加法(-3, 5, abs))

# Python内建了map()和reduce()函数。
# map()函数接收两个参数，一个是函数，一个是可迭代对象（list/tuple/生成器等），map将传入的函数依次作用到序列的每个元素，
# 并把结果作为新的Iterator（迭代器/生成器，保存的是计算方法，使用next来获得下一个值）返回。

print('map方式实现 ', list(map(str, [1, 2, 3, 4, 5])))
# map生成的迭代器（可用于for、等语句）是惰性序列，因此通过list()函数让它把整个序列都计算出来并返回一个list。

# 效果等同于以下for循环
L = []
for x in [1, 2, 3, 4, 5]:
    L.append(str(x))
print('for循环方式实现 ', L)

# reduce()接收两个参数，一个是函数，必须能接收2个参数；一个是可迭代对象（list/tuple/生成器等）。reduce把函数作用在一个序列，然后把结果继续和序列的下一个元素做累积计算，其效果就是：
# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

# 对一个序列求和

def 求和(a, b):
    return a + b

print('利用reduce累积功能计算', reduce(求和, [1, 2, 3, 4, 5]))

# 把字符串转为数字

def str2int(ss):
    转换字典 = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9}  # 定义了一个dict

    def 数字拼合(a, b):
        return 10 * a + b

    def 单个字符转int(s):
        return 转换字典[s]  # 根据key从字典（dict）中返回对应的vavle

    # 现在需要把 单个字符转int 这个函数作用到字符串的每个字符上，正适合map函数
    nn = list(map(单个字符转int, ss))  # nn接收map中生成的所有数字格式，必须用list取出来。

    # 现在需要对 nn 按 数字拼合去拼接起来，需要前后累积，适合reduce
    return reduce(数字拼合, nn)  # 也可以直接把上步的map(单个字符转int,ss) 写在这，因为生成的是一个迭代器

print('字符串转为数字 ', str2int('23455'))

print('*****************练习题 1****************')
# 利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字


def 规范名字(ss):     # 先写出对单个元素生效的函数，再利用map应用到list每个成员上

    def 规范(s):
        return s.title()
    return list(map(规范, ss))

例子 = ['adam', 'LISA', 'barT']

print(规范名字(例子))

print('*****************练习题 2****************')
# 请编写一个prod()函数，可以接受一个list并利用reduce()求积

def 求积(s):

    def 积(a, b):
        return a * b

    return reduce(积, s)

print(求积([1, 2, 3, 4, 5]))

print('*****************练习题 3****************')
# 编写一个str2float函数，把字符串'123.456'转换成浮点数123.456

def str2float(s):
    # 先算出字符串中小数点后面位数,然后将字符串中.去除，便于转换和拼接
    n = 0
    if s.find('.') > 0:  # find查找出现的位置，找不到返回-1，只能用于字符串，不能用于list。而index都可以用，但找不到会报错。

        n = len(s) - s.find('.')-1
        s = s.replace('.', '')

    转换字典 = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9}  # 定义了一个dict

    def 数字拼合(a, b):
        return 10 * a + b

    def 单个字符转int(s):
        return 转换字典[s]

    return reduce(数字拼合, map(单个字符转int, s))/10**n

print(str2float('0.123456'))
