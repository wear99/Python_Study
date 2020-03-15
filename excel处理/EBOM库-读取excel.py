# -*-coding=utf-8-*-
# 按bom表原样添加,产品码前层次为'*'. 整个bom库为字典结构, 每个产品代码为key,结构为值.

import openpyxl as xl
import json


def get_root(wsheet):
    for n in wsheet.rows:
        for root in all_root:
            if root in n[0].value:
                return '*',n[0].value, 1

def get_col(wsheet):
    start_r = 1
    lv_c = 0
    code_c = 0
    num_c=0
    for n in wsheet.rows:
        start_r += 1
        for col in range(0, len(n)):
            if n[col].value and ('级别' in str(n[col].value) or '层次' in str(n[col].value)):
                lv_c = str(col)
            if n[col].value and '编码' in str(n[col].value):
                code_c = col
            if n[col].value and ('用量' in str(n[col].value) or '数量' in str(n[col].value)):
                num_c = col
            if lv_c and code_c and num_c:
                return int(lv_c), code_c, num_c, start_r

def add_item(wsheet):
    def std(s):
        if s:
            return str(s).upper().strip()

    for n in wsheet.iter_rows(min_row=start_row, max_col=num_col+1):
        bom_lv = n[lv_col].value + '+'
        code = std(n[code_col].value)
        #fu_code = get_fu(n)
        num = float(std(n[num_col].value))
        all_bom[root].append([bom_lv, code, num])

filename = ['ZD折叠机.xlsx']
patch = 'E:\\Python Study\\excel处理\\xlsx\\'
file = [patch + x for x in filename]

all_bom = {}
all_root=['C01-','C02-','C03-','C04-','C05-','C06-','C07-','C08-','C09-',]

for wbook in file:
    wb = xl.load_workbook(wbook, read_only=True)
    for sname in wb.sheetnames:
        ws = wb[sname]

        # 查找sheet表内的产品型号
        lv,root,n = get_root(ws)

        if root and root not in all_bom:
            all_bom[root] = [[lv, root, n]]
        else:
            continue

        # 查找层次,编码,数量 对应的列数,及起始行数
        lv_col, code_col, num_col ,start_row = get_col(ws)
        if str(lv_col) and code_col and num_col and start_row:
            pass
        else:
            continue
        # 添加物料到all_bom
        add_item(ws)

print(len(all_bom))

with open('all_bom.json', 'w', encoding='utf-8') as f:
    json.dump(all_bom, f, indent=4, ensure_ascii=False)
