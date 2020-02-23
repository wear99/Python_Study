# 列表可以快速生成

# 生成一个1到10的列表
x1 = list(range(1, 11))
print(x1)

#带表达式的生成方式,for每循环一次就赋值一次
x2= list(n * n for n in range(1, 6))
print(x2)
# 也可以直接用[]
x3 = [n * n for n in range(1, 6)]
print(x3)

# for后面可以加if语句进行判断,类似条件赋值,if后不要:
x4 = [n * n for n in range(1, 6) if n % 2 == 0]
print(x4)

#还可以使用两层循环，可以生成全排列. 每次for循环都会赋值
x5 = [m + n for m in 'ABC' for n in 'xyz']
print(x5)

#list中所有的字符串变成小写：
x6 = ['Hello', 'World', 'IBM', 'Apple']
x6=[s.lower() for s in x6]    #此时实际上重新生成了一个list,而不是在原list上修改
print(x6)

# 使用if..else时,不能放在for语句后面,因为后面是筛选条件,加else就无法筛选
# 如果if 写在for前面时,必须加else. 因为for前面的部分是一个表达式，它必须根据x计算出一个结果

x7 = [n * n if n % 2 == 0 else - n for n in range(1, 10)]
print(x7)
# if写在for后面是筛选,只有符合条件才返回值.  
# 而if..else写在for前面则是表达式, 对于for返回的每个值进行判断,符合条件则执行if前面的语句,不符合执行else后面的
