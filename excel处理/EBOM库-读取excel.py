# -*-coding=utf-8-*-
# 按bom表原样添加,产品码前层次为'*'. 整个bom库为字典结构, 每个产品代码为key,结构为值.

import openpyxl as xl
import json


def get_root(wsheet):
    m = 0
    for n in wsheet.rows:
        m += 1
        if m > 10:
            break
        for root in all_root:
            if root == n[0].value[0:4]:
                return '*', n[0].value, 1,n[1].value
    return '', '', ''


def get_col(wsheet):
    start_r = 1
    lv_c, code_c, num_c = 0, 0, 0

    for n in wsheet.rows:
        start_r += 1
        if start_r > 10:
            break
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
patch = 'D:\\work\\python\\excel处理\\excel\\'
file = [patch + x for x in filename]

all_bom = {'index':[]}
# 产品代码的起头，不包含在内的将不被读取
all_root = ['C01-', 'C02-', 'C03-', 'C04-',
            'C05-', 'C06-', 'C07-', 'C08-', 'C09-', ]

for wbook in file:
    wb = xl.load_workbook(wbook, read_only=True)
    for wsname in wb.sheetnames:
        ws = wb[wsname]

        # 查找sheet表内的产品型号
        lv, root, n,name = get_root(ws)

        if root and root not in all_bom:
            all_bom['index'].append([lv,root+' '+name,n])
            all_bom[root] = [[lv, root, n]]
        else:
            print('{0} 文件的{1} 工作表中未找到产品型号，跳过'.format(wbook, wsname))
            continue

        # 查找层次,编码,数量 对应的列数,及起始行数
        lv_col, code_col, num_col, start_row = get_col(ws)
        if str(lv_col) and code_col and num_col and start_row:
            pass
        else:
            print('{0} 文件的{1} 工作表中未找到物料属性表头，跳过'.format(wbook, wsname))
            continue
        # 添加物料到all_bom
        add_item(ws)

print('已读取的BOM数量：',len(all_bom))
for x in all_bom['index']:
    print(x[1])

with open('all_bom.json', 'w', encoding='utf-8') as f:
    json.dump(all_bom, f, indent=4, ensure_ascii=False)
