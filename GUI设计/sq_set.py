# -*- coding: utf-8 -*-
import sqlite3

dbfile = 'batchITEM.db'
conn = sqlite3.connect(dbfile)
cur = conn.cursor()

def del_table():   #删除整个表,如果只是清空表:delete from TableName   
    
    try:        
        cur.execute('DROP TABLE roots')
    except Exception as ex:
        print("处理时出现如下异常%s" % ex)

def sheet_info(sheet):
    sql = "PRAGMA table_info({0})".format(sheet)
    cur.execute(sql)
    #for item in cur.fetchall():
    s = tuple(x[1] for x in cur.fetchall())
    print(s)
    #print(item[1])

def find_db(item, sheet,col):    
    sql = "PRAGMA table_info({0})".format(sheet)
    cur.execute(sql)
    cols = tuple(x[1] for x in cur.fetchall())
    if col == 'ALL':
        col=''
        for x in cols:
            col += x+' or '
    elif col in cols:
        pass
    else:
        return
        
    sql = 'SELECT * FROM {0} WHERE '.format(sheet)+'(code)'+' in '+str(item)
    cur.execute(sql)
    for item in cur.fetchall():
        print(item)

def show_all(sheet):
    sql='SELECT * FROM '+sheet+' LIMIT 10'
    cur.execute(sql)
    for x in cur.fetchall():
        print(x)

def set_old_item(roots):  #对有变动的物料,remark设置为old    
    cur = conn.cursor()
    #cur.execute('SELECT * FROM roots')
    #root = cur.fetchall()
    
    cur.executemany('INSERT OR REPLACE INTO root VALUES (?,?,?)', roots)
    
    #sql = 'UPDATE '+table+' SET remark =\'BATCH\' WHERE type like \'batch\''
    #cur.execute(sql)
    conn.commit()    
    cur.close()


#del_table()

r=[('C07-0031', 'GPF-33-4L-FS全自动折叠堆码机', 'BATCH'),
('C07-0026', '卓越CEF-33-1L-F-FS折叠机堆码机', 'BATCH'),
('C04-0030', '650高速熨平机', 'DESIGN'),
('C07-0032', 'GPF-33-1L-FS全自动折叠堆码机', 'BATCH'),
('C04-0030', 'GPYD6-33-6高速熨平机', 'BATCH'),
('C04-0027', 'GPYD8-3300-4高速熨平机', 'BATCH'),
('C04-0029', 'GPHF-33-4高速送布机', 'BATCH'),
('C04-0029', '四工位高速展布机', 'DESIGN'),
('C07-0032', 'GPF-33-1L-FS全自动折叠堆码机', 'DESIGN'),
('C07-0030','GPF-33-1L-FS高速折叠机','DESIGN')]

set_old_item(r)
show_all('root')

#find_db(('15R07011330','16R07000180'), 'code', 'ALL')


    
