benjin = input("请输入贷款本金(万)")
nianlilv = input("请输入贷款年利率%")
nian = input("请输入贷款年数")
yue_lilv = float(nianlilv) / (12*100)
yue = int(nian) * 12
zong_benjin = 0.0
zong_benxi = 0.0
huankuan_benxi_list=[]
for n in range(1, yue + 1):
    huankuan_benjin = (float(benjin)*10000 * yue_lilv *
                       (1 + yue_lilv)**yue) / ((1 + yue_lilv)**yue - 1)
    #    benjinhe=int(benjin)*(1+float(lilv))**n
    #    print("第 %d 月的还款金额数量为:%.2f" % (n, huankuan))
    zong_benjin += huankuan_benjin

    huankuan_benxi = (float(benjin) * 10000 /
                      yue) + (float(benjin) * 10000 - zong_benxi) * yue_lilv
    huankuan_benxi_list.append(huankuan_benxi)
    zong_benxi += huankuan_benxi

print("等额本金总还款额为%.2f，每月还款额为%.2f" % (zong_benjin, huankuan_benjin))
print("等额本息总还款额为%.2f,%.2f,首月还款额为%.2f" % (zong_benxi,sum(huankuan_benxi_list), huankuan_benxi_list[0]))
for m in range(1, yue+1 ):
    if m % 12 == 1:
        print("第%d年" % (m / 12+1),end=" ")
    print("%8.2f" % huankuan_benxi_list[m-1], end=" ")
    if m % 12 == 0:
        print(" ")
