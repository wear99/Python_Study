import openpyxl as xl


def huizong(ws):
    # sheet.rows为生成器, 里面是每一行的数据，每一行又由一个tuple包裹。
    # sheet.columns类似，不过里面是每个tuple是每一列的单元格。
    for n in ws.rows:
        if n[0].value == '姓名':
            continue
        if n[0].value not in a and n[1].value:

            temp = [n[0].value]
            # temp += [str(n[x].value).replace('小时', '')] if n[x].value else ['']

            for x in (1, 2, 3, 4):
                if n[x].value:
                    temp.append(str(n[x].value).replace('小时', ''))
                else:
                    temp.append('')
            a[n[0].value] = [temp]
            #a[n[0].value] = [[n[0].value]+[str(n[x].value) for x in (1, 2, 3, 4)]]

        elif n[1].value:
            temp = ['']
            for x in (1, 2, 3, 4):
                if n[x].value:
                    temp.append(str(n[x].value).replace('小时',''))
                else:
                    temp.append('')
            a[n[0].value].append(temp)
            #a[n[0].value].append([""]+[str(n[x].value) for x in (1, 2, 3, 4)])


def xlwr():
    newxl = xl.Workbook()
    newxs = newxl.active
    newxs['A1'] = '姓名'
    newxs['B1'] = '加班日期'
    newxs['C1'] = '加班时间'
    newxs['D1'] = '抵充日期'
    newxs['E1'] = '剩余时间'

    for x in a:
        for y in a[x]:
            newxs.append(y)

    for x in b:
        newxs.append(b[x])
    newxl.save('汇总.xlsx')


def shengyu():
    for x in a:
        sum = 0
        used = 0
        for y in a[x]:
            if y[2]:
                sum += float(y[2])
            if y[4]:
                used += (float(y[2]) - float(y[4]))
        b[x] = [x, sum, used, sum - used]


a = {}
b = {}

x = [
    r'E:\Users\SUN\Downloads\技术部年休假和加班统计\2020年技术部人员加班.xlsx',
    r'E:\Users\SUN\Downloads\技术部年休假和加班统计\2019年技术部人员加班.xlsx',
    r'E:\Users\SUN\Downloads\技术部年休假和加班统计\2018年技术部人员加班.xlsx',
    r'E:\Users\SUN\Downloads\技术部年休假和加班统计\2017年技术部人员加班.xlsx',
]

for wb in x:

    wf = xl.load_workbook(wb)
    ws = wf.active
    huizong(ws)

shengyu()
xlwr()
