# -*-coding=utf-8-*-
# all_bom.json 文件是字典结构,每个产品代码为key,值是产品内物料,结构为:[[层次,编码,数量],....]
# all_code.json 文件是列表结构, [[编码,图号,名称,修改日期],.....]

import openpyxl as xl
import json

def find(f):
    rst_bom.clear()
    # 根据之前找到物料的层次,向前查找上一层, 再向前查找更上层, 直到层次为 1;
    def find_lv(num,lv):
        for b in range(num,-1,-1):
            if len(all_bom[root][b][0]) == lv - 1:
                lv -= 1
                if rst_lv.get(lv,'NA') == all_bom[root][b][1]:  #如果上一层父项已经存在,则停止
                    break
                elif lv==1:      # 如果是顶层,则进行添加,并终止
                    rst_lv[1] = all_bom[root][b][1]
                    rst_1.append(all_bom[root][b])
                    break
                else:  # 如果不是顶层并且层次内不存在,则添加后, 并进入下一层查找
                    rst_lv[lv] = all_bom[root][b][1]
                    rst_1.append(all_bom[root][b])
                    find_lv(b,lv)
                    break

    rst_lv = {}
    for root in all_bom:
        for a in range(len(all_bom[root])):  # all_bom {root:[[lv,code,num],    ],   }
            lv = len(all_bom[root][a][0])
            for x in range(lv, 7):
                rst_lv[x]=''
            if f in all_bom[root][a][1]:  # 找到该物料, 往前去查找上一层
                rst_lv[lv] = all_bom[root][a][1]
                rst_1 = []
                rst_1.append(all_bom[root][a])
                if lv == 1:
                    rst_bom.append(all_bom[root][a])
                    break
                else:
                    find_lv(a,lv)
                    for y in rst_1[::-1]:
                        rst_bom.append(y)

def rst_prt(x):
    # 到all-code列表中查找编码的图号,名称
    def get_code(s):
        for item in all_code:
            if s.replace('P','') == item[0]:
                if s==s.replace('P',''):
                    return item[:-1]
                else:
                    return [item[0]+'(P)',item[1],item[2]]
        return ['X '+s+' X', 'X', '物料库中不存在']

    if rst_bom:
        n = 0
        m=0
        sum_n = []
        lv_num = [1, '', '', '', '', '', '']
        name=''
        print('查 询 结 果'.center(100,'-'))
        for key in rst_bom:
            # key[lv,code,draw,name,num]
            key = [key[0]] + get_code(key[1]) + [key[2]]
            lv_num[len(key[0])] = key[4] * lv_num[len(key[0])-1]

            if x in key[1]:
                n += 1
                key[1] = '>> ' + key[1]
                sum_n.append(lv_num[len(key[0])])

            if len(key[0]) == 1:
                if sum_n:
                    print("\n< {0} > 中物料总用量为: {1}".format(name,sum(sum_n)))
                    print(''.ljust(50,'-'))
                name = key[1] +' '+ key[3]
            print("{0:<4}\t{1:<20}\t{2:<20}\t{3:<30}\t{4:>10.1f}".format(
                    key[0], key[1], key[2], key[3], key[4]))
            m += 1
            if m==len(rst_bom):
                print("\n< {0} > 中物料总用量为:  {1}".format(
                    name,sum(sum_n)))

        print('查 询 结 束'.center(100,'-'))
    else:
        print('已读取的产品库中没有使用此物料!'.center(100,'-'))

def find_code(x):
    rst_code.clear()
    for item in all_code:
        for c in item:
            if x in c:
                rst_code.append(item)

rst_bom = []
rst_code = []

with open('all_code.json', 'r', encoding='utf-8') as f:
    all_code = json.load(f)

with open('all_bom.json', 'r', encoding='utf-8') as f:
    all_bom = json.load(f)

print('code库记录: ', len(all_code))
print('bom库记录: %d ,已读取的产品有:'% len(all_bom))
for rootname in all_bom:
    print(rootname,end='\t')

while True:
    x = ''
    x = input('\n请输入要查询的物料编码或图号： ').upper().strip()
    if x == 'q' or x == 'Q':
        break
    elif x:
        find_code(x)
        if len(rst_code)==0:
            print('-----物料库中不存在-----')
        elif len(rst_code) == 1:
            print("物料信息: {0[0]}\t{1[1]}\t{2[2]}".format(rst_code[0],
                                                 rst_code[0], rst_code[0]))
            x=rst_code[0][0]
            find(x)
            rst_prt(x)
        else:
            for n in range(len(rst_code)):
                print("{0}\t{1[0]}\t{2[1]:30}\t{3[2]}".format(n + 1, rst_code[n],
                                                     rst_code[n], rst_code[n]))
            while True:
                m = input('请选择需要查询的序号,输入 q 退出: ')
                if m == 'q' or m == 'Q':
                    break
                try:
                    m=int(m)-1
                    x = rst_code[m][0]
                    print("物料信息: {0[0]}\t{1[1]}\t{2[2]}".format(
                        rst_code[m], rst_code[m], rst_code[m]))
                    find(x)
                    rst_prt(x)
                    break
                except:
                    print('输入有误, ',end='')