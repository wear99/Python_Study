def 计算(a1,b1,c1,a2,b2,c2):
    global 解组合
    for x in range(1, 20):
        for y in range(1, 20):
            if a1 * x + 2 * b1 * y == 5 * c1 and a2 * x + 2 * b2 * y == 5 * c2:
                
                #print("x,y的第%5d组解为%5d,%5d,   此时a1,b1,c1的值为%5d,%5d,%5d" % (n, x, y, a1, b1, c1))
                
                m = str(x) + "," + str(y)
                v=str(a1) + "," + str(b1)+"," + str(c1)+"," + str(a2)+"," + str(b2)+"," + str(c2)
                解组合.append([m,v])
    

def abc不重复函数(解组合abc):
    abc不重复=[]
    for k in 解组合abc:
        isnew = True
        for l in abc不重复:
            if k[1] == l[-1]:
                isnew = False
                
                l.insert(0,k[0])
                
                break
        if isnew:
                        
            abc不重复.append(k[:])      #如果直接添加KK，则对应的是原list的地址，而不是list中值，所以原list就会同样本改变
    return abc不重复                     #python中有变量和常量，像list属于变量，存储的是list的地址，而不是里面常量的地址；其它int str都属于常量，他们里面存储的是对应数值的地址。
                                        #类似.copy和[:]都只能对list第一层的对象地址进行复制，对于多层list则需要用.deepcopy
def xy不重复函数(解组合xy):
    xy不重复=[]
    for k in 解组合xy:
        isnew = True
        for l in xy不重复:
            if k[0] == l[0]:
                isnew = False
                l.append(k[1])
                break
        if isnew:
            xy不重复.append(k[:])    
    return xy不重复




解组合=[]
ABC组合=[]

for a1 in range(1, 20):         #求出符合方程式1条件的所有a,b,c值
    
    for b1 in range(1, 20):
        for c1 in range(1, 20):
            if a1 * 3 + b1 * 4 == c1:
                #ABC = [a1, b1, c1]
                ABC组合.append([a1, b1, c1])
                #del ABC
#print(ABC组合)
#print(len(ABC组合))


for aa in range(0,len(ABC组合)):        #对符合条件的a,b,c值两两组合，去求出x,y的值
    if aa == len(ABC组合)-1:
        break
    for bb in range(aa+1,len(ABC组合)):
        计算(ABC组合[aa][0],ABC组合[aa][1],ABC组合[aa][2],ABC组合[bb][0],ABC组合[bb][1],ABC组合[bb][2])


print("*********************************")
xy = xy不重复函数(解组合)

print("该方程式的解共有%5d" % len(xy))
print("同样x,y 对应的a,b,c值")
for p in xy:
    
    print(p)
    print("-------------------------------------------------")

print("*********************************")

abc=abc不重复函数(解组合)
print("该方程式的解共有%5d" % len(abc))
print("同样a,b,c 对应的x,y值")
for pp in abc:
    
    print(pp)
    print("-------------------------------------------------")

print("*********************************")
print("穷举计算完毕")