#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 数据库编辑页面
import tkinter as tk
from tkinter import ttk
import re

class db_edit(object):
    def __init__(self,master=None,mod=''):
        self.pop = tk.Toplevel(master)
        self.pop.title('更新物料库')
        self.pop.geometry('800x600')
        self.mod=mod
        #self.pop.transient(root)
        #self.pop.grab_set()  # 聚焦在此窗口上，其它窗口不可用
        self.sql_edit=[]
        self.setpag()
        self.menu_tree()

    def setpag(self,):
        fm1 = ttk.Frame(self.pop, height=25)
        fm2 = ttk.Frame(self.pop)

        fm1.pack()
        fm2.pack(expand='yes', fill='both')

        self.lab_txt = tk.StringVar()
        self.cmb_db_eny = tk.StringVar()
        self.cmb_db = ttk.Combobox(
            fm1, height=15, width=50, textvariable=self.cmb_db_eny)
        self.cmb_db.pack(padx=20, pady=10, side='left')
        #self.en1 = ttk.Entry(fm1, width=50, textvariable=self.lab_txt,font=("微软雅黑", 12))
        #self.en1.pack(padx=20, pady=10, side='left')
        self.tree_select = {}
        ttk.Button(fm1,
                   text='执行', command=lambda: self.ex_db(self.cmb_db_eny.get())
                   ).pack(padx=20, pady=10, side='left')
        ttk.Button(fm1,
                   text='确认提交', command=self.sure
                   ).pack(padx=10, pady=10, side='left')
        ttk.Button(fm1,
                   text='回滚操作', command=self.canel
                   ).pack(padx=10, pady=10, side='left')

        self.tev = ttk.Treeview(fm2, columns=(
            '1', '2', '3', '4', '5', '6', '7', '8'), selectmode='browse')

        self.tev.heading('1', text='字段A')
        self.tev.heading('2', text='字段B')
        self.tev.heading('3', text='字段C')

        self.tev.column('#0', width=60)
        self.tev.column('1', width=200)
        self.tev.column('2', width=200)
        self.tev.column('3', width=200)
        self.tev.pack(expand='yes', fill='both')

        self.tev.bind('<Button-3>', self.R_click_tree)
        self.vbar = ttk.Scrollbar(fm2,
                                  orient='vertical',
                                  command=self.tev.yview)
        self.tev.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side='right', fill='y')

    def menu_tree(self,):
        def tree_copy(x):
            self.pop.clipboard_clear()
            self.pop.clipboard_append(x)

        self.menu_tree_code = tk.Menu(self.pop, tearoff=0)
        self.menu_tree_code.add_command(
            label="复制", command=lambda: tree_copy(self.tree_select['item']))
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(
            label="复制物料信息", command=lambda: tree_copy(self.tree_select['items']))
        self.menu_tree_code.add_separator()
        #self.menu_tree_code.add_command(label="修改物料", command=self.modify_item)

    def R_click_tree(self, event):   # 鼠标右键绑定的动作，该程序通过前面的bind 和右键绑定在一起
        iid = self.tev.identify_row(event.y)   # 返回事件发生时鼠标坐标对应的行
        n = self.tev.identify_column(event.x)
        if iid:  # 如果鼠标所在是空,则不执行右键动作
            self.tree_select['id'] = iid    # 当右键时选中目前鼠标所在的行id
            self.tev.selection_set(iid)

            n = int(n.replace('#', ''))
            self.tree_select['item'] = self.tev.item(iid, 'values')[n-1]
            self.tree_select['items'] = self.tev.item(
                self.tev.selection(), 'values')

            self.menu_tree_code.post(event.x_root, event.y_root)

    def creat_list(self, sql_):
        help_db = [r'select * from 表 where 条件1(in/like) AND/OR 条件2',
                   r'delete from 表 where 条件',
                   r'INSERT OR REPLACE INTO 表 VALUES(?,?,?)',
                   r'UPDATE 表 SET 字段 = 值 WHERE 条件',
                   r'PRAGMA table_info(表)',
                   r'select * from sqlite_master where type="table"',
                   r'通配符: \%,单个通配符: \_'
                   ]

        #if sql_ in ('HELP', 'help', 'Help'):
        if not self.sql_edit:
            self.sql_edit = help_db
        else:
            if sql_ in self.sql_edit:
                self.sql_edit.remove(sql_)
            self.sql_edit.append(sql_)

        while len(self.sql_edit) > 20:
            del self.sql_edit[0]

        self.cmb_db["value"] = self.sql_edit[::-1]

    def ex_db(self, sql):
        if sql:
            sql = sql.strip()
        if not sql:
            return

        rst = []
        self.creat_list(sql)

        if sql in ('HELP', 'help', 'Help'):
            return

        #先判断指令类型
        if 'SELECT' in sql.upper():
            txt = '查询的记录：'
            ss = self.db_command(sql)
            rst = ss

        elif 'UPDATE' in sql.upper():
            txt = '更新的的记录：'
            sql_s = re.sub('update(.*)set.*where',
                           'select * from \g<1> where', sql, flags=re.I)
            # 正则中()表示对匹配条件分组，后续可以直接用\g<对应顺序号>来使用该内容
            ss = self.db_command(sql)
            rst = self.db_command(sql_s)

        elif 'DELETE' in sql.upper():
            txt = '删除的记录：'
            sql_s = re.sub('delete', 'select *', sql, flags=re.I)
            rst = self.db_command(sql_s)
            ss = self.db_command(sql)
        else:
            txt = '执行如下：'
            ss = self.db_command(sql)
            rst = ss

        iid = self.tev.insert('', 'end', text='-->', values=(sql, txt))
        self.tev.item(iid, tag='tar')
        self.tev.tag_configure(
            'tar', foreground='blue', background='red', font=('宋体', 10, 'bold'))

        if '指令出错' in str(ss+rst):
            self.tev.set(iid, column='3', value=ss[0])
        elif rst:
            for n, item in enumerate(rst):
                self.tev.insert(iid, 'end', text=str(n+1), values=item)
                if n > 100:
                    break
            self.tev.set(iid, column='3', value=str(
                len(rst)) + ' 条记录,只显示100条..')
            self.tev.insert(iid, 'end', text='-->',
                            values=('以上修改按 [确认提交] 后生效', '如须撤销按 [回滚操作] '))
            self.tev.item(iid, open=True)

    def modify_item(self,):  # 未完成
        def get_tablename():
            rst = {}
            iid_p = self.tev.parent(self.tev.selection())
            info = self.tev.item(iid_p, 'values')
            # ?: 表示非元组匹配
            name = re.findall(
                r'(?:from|update|info) (.*) (?:where|set|values)', info[0], flags=re.I)
            if not name:
                return
            table_name = name[0]
            r = self.db_command('PRAGMA table_info (' + name[0]+")")
            table_info = [x[1] for x in r]
            return table_name, table_info

        old_item = self.tree_select['items']

        pass

    def sure(self,):
        self.mod.db_command('ok')
        self.tev.insert('', 'end', text='-->',
                        values=('-------数据库操作已提交！------'))

    def canel(self,):
        self.mod.db_command('ok')
        self.tev.insert('', 'end', text='-->',
                        values=('**********数据库已回滚！*********'))

    def db_command(self,s):
        r = []
        try:
            cur = self.mod.conn.cursor()
            cur.execute(s)
            for item in cur.fetchall():
                r.append(item)
        except Exception as ex:
            #self.tev.set(iid,column='3',value='指令出错!'+str(ex))
            r.append('指令出错!'+str(ex))
        finally:
            cur.close()
            return r
