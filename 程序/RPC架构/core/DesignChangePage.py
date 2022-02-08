#!/usr/bin/env python
# -*- coding:utf-8 -*-

#设计更改页面
import tkinter as tk
from tkinter import ttk
#from DataHandler import dataHandler

class design_change_GUI(object):
    def __init__(self,master=None,mod=""):
        self.pop = tk.Toplevel(master)
        self.pop.title('设计更改查询')
        self.pop.geometry('800x600')
        self.mod=mod
        #self.pop.transient(root)
        #self.pop.grab_set()  # 聚焦在此窗口上，其它窗口不可用
        self.setpag()
        self.menu_tree()

    def setpag(self,):
        fm1 = ttk.Frame(self.pop)
        fm2 = ttk.Frame(self.pop)

        fm1.pack()
        fm2.pack(expand='yes', fill='both')

        self.cmb_db_eny = tk.StringVar()
        self.cmb_db = ttk.Combobox(
            fm1, height=15, width=40, textvariable=self.cmb_db_eny)
        self.cmb_db.pack(padx=10, pady=10, side='left')
        self.cmb_db.bind('<Button-3>', self.R_click_cmb)
        self.cmb_db.bind("<Return>", self.search_click)

        self.cmb_eny_1 = tk.StringVar()
        self.cmb_1 = ttk.Combobox(
            fm1, height=15, width=8, textvariable=self.cmb_eny_1)
        self.cmb_1.pack(padx=10, pady=10, side='left')
        self.cmb_1["state"] = "readonly"
        self.cmb_1["value"] = ['AND', 'OR']
        self.cmb_1.current('0')

        ttk.Button(fm1,
                   text='设计更改查询', command=self.search_click).pack(padx=20, pady=10, side='left')

        self.lab_txt = tk.StringVar()
        ttk.Label(fm1, textvariable=self.lab_txt, font=(
            "微软雅黑", 12, 'italic')).pack(pady=5)
        self.tev = ttk.Treeview(fm2, columns=(
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'), selectmode='browse')
        self.tev.bind('<Button-3>', self.R_click_tree)

        tree_style = {'#0': ('层次', 60),
                      '1': ('序号', 40),
                      '2': ('图号/更改单号', 120),
                      '3': ('名称', 120),
                      '4': ('更改前编码', 100),
                      '5': ('更改后编码', 100),
                      '6': ('更改前说明', 80),
                      '7': ('更改后说明', 80),
                      '8': ('更改类别', 30),
                      '9': ('更改方式', 60),
                      '10': ('库存数量', 30),
                      '11': ('在途数量', 30),
                      '12': ('已制品处理', 60),
                      '13': ('涉及机型', 60)
                      }
        self.tree = {}
        self.tree_select = {}
        self.tree['col_name'] = []
        self.tree['bom'] = []
        for key, (name, wid) in tree_style.items():
            self.tev.heading(key, text=name)
            self.tev.column(key, width=wid, minwidth=wid)
            self.tree['col_name'].append(name)

        self.tev.column('#0', width=20)
        self.vbar = ttk.Scrollbar(fm2,
                                  orient='vertical',
                                  command=self.tev.yview)
        self.tev.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side='right', fill='y')

        self.hbar = ttk.Scrollbar(
            fm2, orient='horizontal', command=self.tev.xview)
        self.tev.configure(xscrollcommand=self.hbar.set)
        self.hbar.pack(side='bottom', fill='x')

        self.tev.pack(expand='yes', fill='both')

    def menu_tree(self,):    # 定义了treeview处的右键菜单内容，但菜单弹出要由post来调用
        def tree_copy():
            self.pop.clipboard_clear()
            self.pop.clipboard_append(self.tree_select['item'])

        def add_child():
            '查找此更改单中该物料的子项，并添加到显示中'
            item = self.tev.item(self.tree_select['iid'], 'values')
            rst = self.mod.find_in_bom(item, bom="DESIGNCHANGE",
                              parent=False, child=True, opt='AND')
            if 'bom' in rst:
                self.tree_view(rst['bom'][1:], parent=self.tree_select['iid'])

        self.menu_tree_code = tk.Menu(self.pop, tearoff=0)
        self.menu_tree_code.add_command(label="复制", command=tree_copy)
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(label="显示此更改子项", command=add_child)
        self.menu_tree_code.add_separator()
        #self.menu_tree_code.add_command(label="导出清单", command=self.tree_save)

    def search_click(self, event=None):
        x = self.cmb_db_eny.get()
        if not x:
            return

        self.creat_list(x)  # 更新下拉框列表
        x = x.upper()  # 转大写，去首尾空格
        x = x.replace('\n', '')  # 去掉换行符

        op1 = self.cmb_eny_1.get()
        xx = x.split()

        self.find_change_GUI(xx, op=op1)

    def R_click_cmb(self, event):   # 输入框绑定动作
        def onpaste(event=None):
            self.cmb_db.event_generate('<<Paste>>')

        def copy(event=None):
            self.cmb_db.event_generate("<<Copy>>")

        def cut(event=None):
            self.cmb_db.event_generate("<<Cut>>")

        self.menu_eny1 = tk.Menu(self.pop, tearoff=0)
        self.menu_eny1.add_command(label="剪切", command=cut)
        self.menu_eny1.add_separator()
        self.menu_eny1.add_command(label="复制", command=copy)
        self.menu_eny1.add_separator()
        self.menu_eny1.add_command(label="粘贴", command=onpaste)

        self.menu_eny1.post(event.x_root, event.y_root)   # 在事件坐标处,弹出对应的菜单

    def R_click_tree(self, event):   # 鼠标右键绑定的动作，该程序通过前面的bind 和右键绑定在一起
        iid = self.tev.identify_row(event.y)   # 返回事件发生时鼠标坐标对应的行
        n = self.tev.identify_column(event.x)
        if iid:  # 如果鼠标所在是空,则不执行右键动作
            self.tree_select['iid'] = iid    # 当右键时选中目前鼠标所在的行id
            n = int(n.replace('#', ''))
            self.tree_select['item'] = self.tev.item(iid, 'values')[n-1]
            self.tev.selection_set(iid)
            self.menu_tree_code.post(event.x_root, event.y_root)

    def creat_list(self, sql_):
        sql_edit = list(self.cmb_db["value"])

        if sql_ in sql_edit:
            sql_edit.remove(sql_)

        sql_edit.append(sql_)

        while len(sql_edit) > 10:
            del sql_edit[0]

        self.cmb_db["value"] = sql_edit[:]

    def find_change_GUI(self, xx, op='AND'):
        rst = self.mod.find_in_bom(xx, bom="DESIGNCHANGE",
                          parent=True, child=True, opt=op)
        if 'bom' in rst:
            self.lab_txt.set(str(xx)+'查询有 %d 项：' % len(rst['code']))
            self.tree_view(rst['bom'])
        else:
            self.lab_txt.set(str(xx)+'查询无结果')

    def tree_view(self, bom, parent=''):
        if not bom:
            return
        #if parent=='':
        for item in self.tev.get_children(parent):  # 对treeview进行清空
            self.tev.delete(item)

        if bom:
            lv = {bom[0][0] - 1: parent}
            #a = bom[0][0] - 1
        order_n = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for n, key in enumerate(bom):
            i = key[0]
            order_n[i + 1:8] = 0, 0, 0, 0, 0, 0, 0, 0
            order_n[i] += 1

            lv[i] = self.tev.insert(
                lv[i - 1], 'end', text=str(order_n[i]), values=key[1:])

            if key[1] == 'ROOT':
                self.tev.item(lv[i], tag='tar')
            self.tev.item(lv[i], open=True)
        self.tev.tag_configure('tar', foreground='blue',
                               background='red', font=('宋体', 10, 'bold'))
        #self.tree['bom']= bom

    def tree_save(self,):
        def get_child(pr):
            for iid in self.tev.get_children(pr):
                bom.append(self.tev.item(iid, 'values'))
                get_child(iid)
        bom = []
        get_child("")

if __name__ == '__main__':
    design_change_bom = {}
    root=tk.Tk()
    design_change_GUI(root)
    root.mainloop()
