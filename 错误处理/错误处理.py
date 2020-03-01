#当我们认为某些代码可能会出错时，就可以用try来运行这段代码，如果执行出错，则后续代码不会继续执行，
# 而是直接跳转至错误处理代码，即except语句块，执行完except后，
# 如果有finally语句块，则执行finally语句块，至此，执行完毕。
# 如果 try 语句中未出错，则会跳过 except语句，直接执行 finally。finally可以没有
# 中间可以有多个 except语句，还可以加上else，这样当没错误时执行

try:
    print('开始计算 10/0 ')
    a = 10 / 2
    b=10/int('ss')
    print('计算结果是: ', a)
except ZeroDivisionError as e:    #这里要罗列出各种可能出的错误，所以需要多个except
    print('错误是：', e)
except ValueError as e:
    print('错误是：', e)

# 如果错误没有被捕获，它就会一直往上抛（外层函数），最后被Python解释器捕获，打印一个错误信息，然后程序退出。

# 记录错误
# 如果不捕获错误，自然可以让Python解释器来打印出错误堆栈，但程序也被结束了。
# 既然我们能捕获错误，就可以把错误堆栈打印出来，然后分析错误原因，同时，让程序继续执行下去。
# Python内置的logging模块可以非常容易地记录错误信息：
import logging

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)

main()
print('END')