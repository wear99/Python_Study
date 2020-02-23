名单=['张三','李四','王五']
print("目前宴会名单", 名单)
while True:
    x = input("0:退出 \n1:增加名单 \n2:删除名单\n")
    if int(x) == 0:
        break
    if int(x) == 1: 
        增加=input('请输入要增加的名字\n')
        名单.append(增加)
        print("目前的宴会名单是", 名单)
    if int(x) == 2:
        删除=input('请输入要删除的名字\n')
        if 删除 in 名单:
            名单.remove(删除)
            print("目前的宴会名单是", 名单)
        else:
            print("名字不存在\n")
    input("输入任意键继续....\n")


