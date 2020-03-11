# 读取生成好的物料库json文件,以供查询
# -*-coding=utf-8-*-


import json
import openpyxl as xl
import time
def find(s):
    rst = []
    for item in all_code:
        for m in item:
            if m and s in m:
                rst.append(item)
    if rst:
        #rst.sort(key=lambda x: x[0])
        print('共查找到物料: %d' % len(rst))
        for key in rst:
            print('%-15s  %-25s  %-50s  %-10s' %
                  (key[0], key[1], key[2], key[3]))
    else:
        print('结果不存在！')


开始时间 = time.time()
with open('all_code.json', 'r', encoding='utf-8') as f:
    all_code = json.load(f)
结束时间 = time.time()
print('读取完毕，执行时间为 %f 秒' % (结束时间 - 开始时间))

while True:
    x = ''
    x = input('请输入要查询的物料编码或图号：\n').upper().strip()
    if x == 'q' or x == 'Q':
        break
    elif x:
        find(x)