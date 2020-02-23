# 如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？
# 这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，
# 称为生成器：generator。

L = [x * x for x in range(10)]

#把列表生成的[]改成()即可创建生成器

g = (x * x for x in range(10))
# generator保存的是算法，所以不能直接得到里面的具体数值. 每次调用next(g)，就计算出g的下一个
# 元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。

print('这是第1次调用生成器', next(g))

print('这是第2次调用生成器', next(g))
print('这是第3次调用生成器', next(g))

print("---------使用for循环---------")
# 正确的方法是使用for循环，因为generator也是可迭代对象
for n in g:
    print(n)

#我们创建了一个generator后，基本上永远不会调用next()，而是通过for循环来迭代它，
# 并且不需要关心StopIteration的错误。

print("------使用函数型生成器--------------")
# generator非常强大。如果推算的算法比较复杂，用类似列表生成式的for循环无法实现的时候，
# 还可以用函数来实现。
# 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：

# 最难理解的就是generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行
# 函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，
# 再次执行时从上次返回的yield语句处继续执行。
# yield 后面就是要返回的数值


def 生成器():
    for n in range(10):
        #print(n)
        yield n * n


a = 生成器()  # 类似实例化
print(next(a))
print(next(a))
print(next(a))

print("------使用for 函数型生成器--------------")
# 一般都是使用for来取出生成器函数中数值:

for x in 生成器():  #每次直接用函数名,则重新开始.如果想接着前面的,要用实例化的名字
    print(x)

# 这时我们拿不到生成器结尾的值,即不知道生成器什么时候结束.
# 如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中：

print("------使用函数型生成器,拿到结束标志--------------")
b = 生成器()
while True:
    # 捕获异常,try:尝试执行的代码, except:出现错误的处理.避免出现错误时程序报错.
    try:
        x = next(b)
        print(x)
    except StopIteration as e:
        print('生成器返回值', e.value)
        break

# 如果想把一个List转变为迭代器,可使用next来调用下一个值:
q = iter([1, 2, 3, 4, 5, 6])
next(iter(q))

print("------练习题,杨辉三角--------------")


def 杨辉三角():
    xx = []
    while True:

        if len(xx) < 2:
            xx.append(1)
            yield xx
        else:
            xx = [1] + [(xx[n] + xx[n - 1]) for n in range(1, len(xx))] + [1]
            yield xx


#a=杨辉三角()
#for x in range(10):
#    print(next(a))
n = 0
for x in 杨辉三角():
    print(x)
    n += 1
    if n > 10:
        break
