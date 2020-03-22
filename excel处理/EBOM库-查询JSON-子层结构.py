# -*-coding=utf-8-*-
# all_bom_code.json 文件是字典结构,每个物料编码为key,值是第一层子件编码和数量,
# 结构为:[code:[[子件1编码,数量],[子件2编码,数量]],....]
# all_code.json 文件是字典结构, [code:[编码,图号,名称,修改日期],.....]

import openpyxl as xl
import json
import re

def find_bom(f):
    # 在字典每个值的里面查找编码,找到后将对应的key,再作为编码进行同样查找,直到key=index
    # all_bom-code是所有从BOM表读出来的物料
    # all_bom只保留有子件的物料,减少数量,便于提高速度

    def find_code_in_bom(x, n):
        for key, item in all_bom.items():
            if key == 'index':
                continue
            for code in item:
                if x in code:
                    rst_1[n] = [n] + code
                    if key in all_bom['index']:
                        if key not in rst_root:
                            rst_root[key] = []
                        rst_1[n + 1] = [n + 1, key, 1]
                        num = n + 2
                        rst_2 = []
                        for y in rst_1[n + 1:0:-1]:
                            rst_2.append([num - y[0], y[1], y[2]])
                        rst_root[key].append(rst_2[:])
                        break
                    else:
                        find_code_in_bom(key, n + 1)
                        break

    def fmt_rst_root():
        for key in rst_root:
            lvcode = {}
            rst_root[key].sort()
            for items in rst_root[key]:
                for item in items:
                    if lvcode.get(item[0], 'NA') != item[1]:
                        lvcode[item[0]] = item[1]
                        for n in range(item[0] + 1, 7):
                            lvcode[n] = ''
                        rst_bom.append([item[0], item[1], item[2]])

    def total_num(x):
        # 计算反查物料在顶层的总用量,和本层用量
        lv_num = {0: 1, 1: 1}
        code_num = [0]
        root_index = 0

        for n, item in enumerate(rst_bom):
            lv_num[item[0]] = item[2] * lv_num[item[0] - 1]
            item.append(lv_num[item[0]])

            if item[1] == x:
                code_num.append(lv_num[item[0]])

            if item[0] == 1 or n == len(rst_bom) - 1:
                rst_bom[root_index][3] = (sum(code_num))
                code_num = [0]
                lv_num = {0: 1, 1: 1}
                root_index = n

    rst_bom.clear()
    rst_1 = ['' for x in range(7)]
    rst_root = {}

    find_code_in_bom(f, 1)

    if rst_root:
        fmt_rst_root()
        total_num(f)
    else:
        rst_bom.append([1, f, 'NA'])
    rst_bom_prt()



def get_code(s):
    for item in all_code:
        if s.replace('P', '') == item[0]:
            if s == s.replace('P', ''):
                return item[:-1]
            else:
                return [item[0]+'(P)', item[1], item[2]]
    return ['X '+s+' X', 'X', '物料库中不存在']


def rst_bom_prt():
    # 到all-code列表中查找编码的图号,名称
    if not rst_bom:
        print('没有BOM使用')
    else:
        for key in rst_bom:
            #for key in a:
            #print(key)
            print("{0:<10}\t{1:<20}\t{2:<10}\t{3:<10}".format(
                key[0], key[1], key[2], key[3]))

def find_code(f):  # 根据输入内容查找物料，先用字典key查找，如果没有则进入模糊查询
    rst_code.clear()
    if f in all_code:
        rst_code.append(all_code[f][:])
    else:
        f = f.replace('*', '.*')  # 将windows习惯用法的 * 转换为python中的 .*
        f = re.compile(f)  # 使用正则表达式中通配符进行查询
        for item in list(all_code.values()):
            for m in item[:3]:
                if m and f.search(m):
                    rst_code.append(item[:])

def find_son(f):    #根据编码对应的子零件,再向下取出,直到子零件为''
    def find_son_code(x, n):
        if x in all_bom:
            for item in all_bom[x]:
                rst_son.append([n]+item)
                find_son_code(item[0],n+1)

    rst_son.clear()
    if f in all_bom:
        rst_son.append([1,f,1])
        find_son_code(f, 2)
    rst_son_prt(f)

def rst_son_prt(x):
    if len(rst_son) > 1:
        for key in rst_son:
            print("{0:<10}\t{1:<20}\t{2:<10}".format(
                 key[0], key[1], key[2]))

    elif x in all_bom_code:
        print('此物料没有子零件!'.center(100, '-'))
    else:
        print('已读取的产品库中此没有此物料!'.center(100, '-'))

def read_date(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as fc:
            return json.load(fc)
    except:
        print('读取失败')
'''
def find_input(x):
    x = x.replace('*', '.*')    # 将windows习惯用法的 * 转换为python中的 .*
    x = re.compile(x)             # 使用正则表达式中通配符进行查询
    find_code(x)
    if len(rst_code) == 0:
        print('-----物料库中不存在-----')
    elif len(rst_code) == 1:
        sect = input('请选择进行：\n 1. 反查\n 2. 查看子零件\n').strip()
        if sect == '1':
            print("物料信息: {0[0]}\t{1[1]}\t{2[2]}".format(rst_code[0],
                                                        rst_code[0], rst_code[0]))
            x = rst_code[0][0]
            find_bom(x)
            rst_bom_prt(x)
        elif sect == '2':
            print("物料信息: {0[0]}\t{1[1]}\t{2[2]}".format(rst_code[0],
                                                        rst_code[0], rst_code[0]))
            find_son(x)
            rst_son_prt(x)
    else:
        for n in range(len(rst_code)):
            print("{0}\t{1[0]}\t{2[1]:30}\t{3[2]}".format(n + 1, rst_code[n],
                                                        rst_code[n], rst_code[n]))
        while True:
            m = input('请选择需要查询的序号,输入 q 退出: ')
            if m in ('q', 'Q', '0', ''):
                break
            try:
                m = int(m)-1
                x = rst_code[m][0]
                print("选择的物料: {0[0]}\t{1[1]}\t{2[2]}".format(
                    rst_code[m], rst_code[m], rst_code[m]))
                sect = input('请选择进行：\n 1. 反查\n 2. 查看子零件\n').strip()
                if sect == '1':
                    find_bom(x)
                    rst_bom_prt(x)
                    break
                elif sect == '2':
                    find_son(x)
                    rst_son_prt(x)
                    break
            except:
                print('输入有误, ', end='')
'''

rst_code = []
rst_bom = []
rst_son = []

all_code = read_date('all_code.json')
all_bom_code = read_date('all_bom_code.json')

print('code库记录: ', len(all_code))
print('bom库记录: %d ,已读取的产品有:' % len(all_bom_code), all_bom_code['index'])

all_bom = {}   # 有子层结构的才保留

for key, item in all_bom_code.items():
    if item:
        all_bom[key] = item
print('有子零件的bom库记录: %d :' % len(all_bom))

while True:
    a=input('1:反查\n2:查询子零件   ')
    str_find = input('\n请输入要查询的物料编码或图号： ').upper().strip()
    if str_find in ('q', 'Q', '0'):
        break
    elif str_find:
        if a=='1':
            find_bom(str_find)
        elif a == '2':
            find_son(str_find)
