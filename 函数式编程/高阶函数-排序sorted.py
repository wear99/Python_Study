# sorted 可以对一个List进行排序，sorted([1,4,2,6,3])
# 也可以带一个函数，利用函数作用在每个变量后的返回值进行排序，再返回原list的排序结果

print(sorted([3, -3, 2, 6, -10, 1], key=abs))  #按abs(x)进行排序，返回的还是原序列的数据

# 要进行反向排序，不必改动key函数，可以传入第三个参数reverse=True

print('***********练习题 排序*************')

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def 成绩(s):
    return s[1]    

def 名字(s):
    return s[0]

print('按成绩排序', sorted(L, key=成绩))

print('按名字排序',sorted(L,key=名字))