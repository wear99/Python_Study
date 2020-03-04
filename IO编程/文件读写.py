# 所有的文件读写都必须通过操作系统的接口来实现

# 标示符'r'表示读，这样，我们就成功地打开了一个文件。如果文件不存在，open()函数就会抛出一个IOError的错误
f = open(r'E:/test.txt', 'r', encoding='utf-8')
# \ 在Python表示转义字符，不能直接使用：1.前面加r，表示直接引用；2.用 \\ ；3.用/代替
# utf-8: 所有文件编码; gbk(ANSI),简体中文;

# 如果文件打开成功，接下来，调用read()方法可以一次读取文件的全部内容，Python把内容读到内存，用一个str对象表示：
ss = f.read()
print(ss)

# 最后一步是调用close()方法关闭文件
f.close()

# 由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。
# 所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现：

# Python引入了with语句来自动帮我们调用close()方法,简化代码
with open('e:\\test.txt', 'r', encoding='utf-8') as ff:
    print(ff.read())

# 调用read()会一次性读取文件的全部内容;
# 调用readline()可以每次读取一行内容，
# 调用readlines()一次读取所有内容并按行返回list。
# 调用read(size)方法，每次最多读取size个字节的内容

with open(r'E:/test.txt', 'r', encoding='utf-8') as vsc:
    for x in vsc.readlines():
        print(x.strip())  #

# 要读取二进制文件，比如图片、视频等等，用'rb'模式打开文件即可
# 在文本文件中可能夹杂了一些非法编码的字符。遇到这种情况，open()函数还接收一个errors参数，
# 表示如果遇到编码错误后如何处理。最简单的方式是直接忽略：
# f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')

#****************************************
# 写文件和读文件是一样的，唯一区别是调用open()函数时，传入标识符'w'或者'wb'表示写文本文件或写二进制文件
# 以'w'模式写入文件时，如果文件已存在，会直接覆盖（相当于删掉后新写入一个文件）。
# 如果我们希望追加到文件末尾怎么办？可以传入'a'以追加（append）模式写入

with open(r'E:/test.txt', 'w', encoding='utf-8') as f:
    f.write('write test...\n')

# 可以反复调用write()来写入文件，但是务必要调用f.close()来关闭文件。当我们写文件时，
# 操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。
# 只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。
# 忘记调用close()的后果是数据可能只写了一部分到磁盘，剩下的丢失了。所以，还是用with语句来得保险
import datetime

with open(r'E:/test.txt', 'a+', encoding='utf-8') as f:
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(time_now + ' write test...\n')
    # 此时指针被移动到文件末尾,所有直接读取会是空白,需要把指针移回文件头
    f.seek(0, 0)        # 0-文件头;1-当前位置;2-末尾; 1,2必须在二进制模式下使用
    print(f.read())
    
'''
open() 的所有模式
r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。
r+	打开一个文件用于读写。文件指针将会放在文件的开头。
rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
w	打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
w+	打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。
'''