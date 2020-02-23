a = 5 if 3 > 5 else 6  #条件赋值,如果If成立则前面的值,否则else的值

aa = 3 > 5
print(aa)

print(5 if 3 > 5 else 6)  #条件输出

print(3 > 2 )    #bool值

#短路效应
print(3 < 2 and 10)  #and条件时,前面有假,后面的不进行判断.     如果前面为真,则取最后的值

print(3>2 or 10)   #or条件时,前面为真,后面不判断.    

#循环赋值

ss = [n + n for n in 'asdfg']
print(ss)

aa = [n for n in range(10)]
print(aa)

#实现list两项相加功能,for每次循环就会给List一个值
aa = [aa[n] + aa[n + 1] for n in range(len(aa) - 2)]
print(aa)