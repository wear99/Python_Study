# 最底层零件(不算原材料)成本由4块组成: 合计,材料,人工,费用;
# 父项零件成本则由底层零件累加而成
# 读取成本表格,建立成本数据库;
# 定期更新: 根据bom库里面父项的子零件成本逐个进行累加计算;

import openpyxl as xl
import json

def read_cost(file):
    def get_col(wsheet):
        col.clear()
        cost_need = {            
            '编码': 'code',
            '材料成本': 'metal',
            '人工成本': 'labor',            
            '子件名称': 'name',
            '费用成本': 'exp',
                
        }

        str_row = 1
        for row in wsheet.values:
            str_row += 1
            if str_row > 10:
                rst['error']='前10行找不到BOM属性列(层次，编码，名称，数量)'
                break         
            for c, value in enumerate(row):
                for key in cost_need:
                    if isinstance(value, str) and key in value.replace(' ', ''):
                        col[cost_need[key]] = c

            if len(col) == 5:
                col['start_r']= str_row             
                break
            else:
                col.clear()

    def std(s):       
        if isinstance(s, (int, float)):
            return round(s,2)            
        else:
            return 0
        
    def add_item(ws):
        for row in ws.iter_rows(min_row=col['start_r'], values_only=True):
            code = row[col['code']]
            code = code.upper().strip() if code else '-'
            name = row[col['name']]            
            metal = std(row[col['metal']])
            labor = std(row[col['labor']])            
            exp = std(row[col['exp']])
            tot = metal + labor + exp
            
            if code != '-':
                excel_cost.append([1,code,name, metal, labor, exp,tot])
    
    excel_cost = []
    col = {}
    rst = {}    
    try:
        wb = xl.load_workbook(file, read_only=True)
    except:        
        rst['error']=file+'文件读取失败'
        return rst
 
    wsheet = wb.active
    get_col(wsheet)

    if col and 'error' not in rst:  # 查找层次,编码,数量 对应的列数,及起始行数        
        add_item(wsheet)
        rst['read']= excel_cost

    return rst

def update_to_cost_db(excel_cost):
    rst = {}
    cost_change=[]
    for item in excel_cost:
        if item[1] in all_cost and item[6] != all_cost[item[1]][3]:
            cost_change.append(item)
            cost_change.append([2, '', ''] + all_cost[item[1]])            
        all_cost[item[1]] = item[3:]    
    try:
        with open('all_cost.json', 'w', encoding='utf-8') as f:
            json.dump(all_cost, f, indent=4, ensure_ascii=False)
        
        rst['info']='已成功更新成本库'        
    except:
        rst['info']='文件写入失败'
    if cost_change:
        rst['change'] = cost_change

    return rst

def update_parent_cost():  # 对BOM库中组合件的成本重新按结构进行累加
    updated_code = {}   
    def find_child_cost(x, n,c0,c1,c2,c3):
        if x in batchbom_has_child and x not in updated_code and (x[:3] == '24R' or x[0]=='C'):
            #只针对24R组合件或成品吗需要对子零件成本累加,其它的无须更新
            all_cost[x]=[0,0,0,0]
            for item in batchbom_has_child[x]:
                all_cost[x]=find_child_cost(item[0], item[1],all_cost[x][0],all_cost[x][1],all_cost[x][2],all_cost[x][3])
            updated_code[x] = ''
            print(x, all_cost[x])
            
        if x in all_cost:
            updated_code[x] = ''
            return round(c0+all_cost[x][0] * n,2),round(c1+all_cost[x][1] * n,2),round(c2+all_cost[x][2] * n,2),round(c3+all_cost[x][3] * n,2)           
            
        else:
            updated_code[x] = ''
            return c0,c1,c2,c3
            
    #for f in all_batch_bom:
    f='C04-0029'
    all_cost[f]=find_child_cost(f, 1,0,0,0,0)    

def read_json_date(filename):  # 从现有文件读取数据
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print(filename+' 数据库读取失败')
        return {}        

def creat_batchbom_has_child():  # 创建有子件物料的BOM当前库
    batchbom_has_child.clear()
    for k, v in all_batch_bom.items():
        if v:
            batchbom_has_child[k] = v 

all_cost = {}
file=r'D:\work\python\excel处理\excel\C04_0029-成本.xlsx'
rst = read_cost(file)
update_to_cost_db(rst['cost'])

all_batch_bom = read_json_date('all_batch_bom.json')

batchbom_has_child = {}
creat_batchbom_has_child()

update_parent_cost()   