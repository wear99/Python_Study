import sqlite3
from datetime import datetime

conn = sqlite3.connect('test.db')
cur = conn.cursor()

def del_table():
    try:
        cur.execute('DROP TABLE code1')
    except Exception as ex:
        print(ex)

def creat_table():
    code = "CREATE TABLE code1 (code TEXT PRIMARY KEY,draw TEXT,name INTEGER,status TEXT DEFAULT (datetime('now','localtime')));"
    cur.execute(code)
    #conn.commit()

def insert_item():
    sql = 'INSERT OR REPLACE INTO code1 (code,draw,name) VALUES (?,?,?)'

    new = (('q', 'w', 22), ('qq', '22', 33), ('111', '222', 55))
    cur.executemany(sql, new)
    conn.commit()

def update_item():
    a = (22, 33)
    sql='UPDATE code1 SET draw= \'old\' WHERE name in '+str(a)
    #sql = 'SELECT * FROM code1 WHERE name in '+str(a)
    cur.execute(sql)
    #conn.commit()

def search_item():
    cur.execute('SELECT * FROM code1')
    for item in cur.fetchall():
        print(item)

insert_item()
#update_item()
search_item()

