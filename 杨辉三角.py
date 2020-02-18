def 杨辉三角(max):
    上一层 = [1]
    当前层 = [1]
    print("1".center(100))
    n = 2
    while n < max:
        
        当前层[0] = 上一层[0]
        当前层.append(上一层[-1])
        for m in range(1, n - 1):
            当前层[m] = 上一层[m] + 上一层[m - 1]
        mystr = "   ".join(str(s) for s in 当前层)
        
        #print(mystr.center(100))
        yield mystr
        上一层 = 当前层[:]
        n += 1


for n in range(6):
    #杨辉三角(6)
    ss=杨辉三角(6)
    print(ss)
print("********************")
