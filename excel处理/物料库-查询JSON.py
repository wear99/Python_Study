# 读取生成好的物料库json文件,以供查询,可以使用通配符
# -*-coding=utf-8-*-

import json
import re
import openpyxl as xl

def find(s):
    rst_code.clear()
    for item in all_code:
        for m in item:
            if m and s.search(m):
                rst_code.append(item)

def rst_prt():
    if rst_code:
        print('共查找到物料: {0} 条'.format(len(rst_code)))
        print('查 询 结 果'.center(100, '-'))
        for key in rst_code:
            print('{0:<20}\t{1:<25}\t{2:<30}\t{3:>10}\t'.format(
                key[0], key[1], key[2], key[3]))

        print('查 询 结 束'.center(100, '-'))
    else:
        print('物料查找不存在！')

with open('all_code.json', 'r', encoding='utf-8') as f:
    all_code = json.load(f)

rst_code = []
while True:
    x = input('请输入要查询的物料编码或图号：\n').upper().strip()
    
    if x in ('q','Q','0'):
        break
    elif x:
        x=x.replace('*','.*')
        x=re.compile(x)
        find(x)
        rst_prt()