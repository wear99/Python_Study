# -*- coding: utf-8 -*-
import sqlite3

def update_parent_cost(x):  # ?BOM?????????????????    
    def find_child_cost(x, n,c0,c1,c2,c3):
        if x in parent_cost and x not in updated_code:   # ???24R?????????????????,???????
            parent_cost[x]=(0,0,0,0)
            for item in all_batch_bom[x]:
                c0,c1,c2,c3 = find_child_cost(item[0], item[1], parent_cost[x][0], parent_cost[x][1], parent_cost[x][2], parent_cost[x][3])
                
                parent_cost[x]=(parent_cost[x][0]+c0*n,parent_cost[x][1]+c1*n,parent_cost[x][2]+c2*n,parent_cost[x][3]+c3*n)

            updated_code[x] = ''
            print('%s???:'%x,parent_cost[x])
            return parent_cost[x]
        elif x in all_cost:
            updated_code[x] = ''

            return round(all_cost[x][0] * n,2),round(all_cost[x][1] * n,2),round(all_cost[x][2] * n,2),round(all_cost[x][3] * n,2)
        else:
            updated_code[x] = ''
            return 0,0,0,0

    updated_code = {}
    parent_cost={}
    
    for f,item in all_batch_bom.items():
        if (f.startswith('24R') or f.startswith('28R') or f.startswith('C')):
            parent_cost[f] = item
    
    print(all_cost[x])
    print('---------------------------')
    cost=find_child_cost(x,1,0,0,0,0)
    
    return cost

def load_batch_db(dbfile):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM batchBOM')
    for item in cur.fetchall():            
        if item[0] not in all_batch_bom:
            all_batch_bom[item[0]] = [[item[1], item[2]]]
        else:
            all_batch_bom[item[0]].append([item[1], item[2]])
    
    cur.execute('SELECT * FROM cost')
    for item in cur.fetchall():
        all_cost[item[0]] = item[1:]
        
    conn.close()

sql1 = 'select' + '#\'code\'#' 
f='ddd'
sql = 'SELECT * FROM designBOM WHERE \'#\'||code||\'#\'||name||\'#\' like \'#' + f + '#\''

print(sql)
all_batch_bom = {}
all_cost = {}

dbfile='batchITEM.db'
load_batch_db(dbfile)

x='24R07003230'
cost=update_parent_cost(x)

print('%s???:'%x,cost)

