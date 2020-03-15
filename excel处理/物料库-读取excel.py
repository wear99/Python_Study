# 读取指定的excel文件,将物料属性以list形式存储，并写入json文件
# -*-coding=utf-8-*-

import openpyxl as xl
import json
from datetime import datetime

# 根据excel 行读取到列表中
def add_item(n):
    code = std(n[1].value)
    draw = std(n[4].value)
    name = std(n[2].value)
    data = std(n[5].value)

    if code and code!='-':
        x = [code, draw, name, data]
        if code:
            all_code.append(x)

def std(s):
    if isinstance(s, datetime):
        return s.strftime('%Y-%m-%d')
    elif s:
        return str(s).upper().strip()
    else:
        return '-'

# 查找旧编码,并在编码前加标记 *
def old_item():
    all_code.sort(key=lambda x: x[0])
    # 编码已经被排序,对任一编码和下一个编码进行比对,如果除了最后一位相同,且比较小,则认为是旧编码
    for x in range(len(all_code) - 1):
        
        a = all_code[x][0]
        if a[2] == 'R':
            b = all_code[x + 1][0]
            if a[:-1] == b[:-1]:
                if a[-1] <= b[-1]:
                    all_code[x][0] = all_code[x][0]+' old'
                elif a[-1] == b[-1]:
                    all_code[x][0] = all_code[x][0]+' rpt'

all_code = []

filename = ['折叠机加工件新编码.xlsx', '各种采购件新编码.xlsx', '滚筒烫平机加工件新编码.xlsx']
patch = 'E:\\Python Study\\excel处理\\xlsx\\'
file = [patch + x for x in filename]

for wbook in file:
    wb = xl.load_workbook(wbook, read_only=True)
    for sname in wb.sheetnames:
        ws = wb[sname]
        for m in ws.iter_rows(min_row=2, max_col=6):
            add_item(m)

old_item()

print(len(all_code))

# indent 有缩进，后一个是不用ascii编码，就可以在文件中显示成中文
# 把读取的物料表写入json文件,方便快速读取
with open('all_code.json', 'w', encoding='utf-8') as f:
    json.dump(all_code, f, indent=4, ensure_ascii=False)

