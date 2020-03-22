import tkinter as tk
from tkinter import ttk
import openpyxl as xl
import json
import re


class app():   # 把整个GUI程序 封装在一个类里面
    def __init__(self,):    # 窗体定义，基本函数，其它的都靠它来触发
        self.root = tk.Tk()
        self.root.title('物料查询')
        self.root.geometry('800x600')
        self.setpag()
        self.menu_en1()
        self.menu_tree()
        self.menu_bar()

    def setpag(self,):    # 把界面内容放在一个一起了，便于修改
        fm0 = ttk.Frame(self.root)
        fm1 = ttk.Frame(self.root)
        fm2 = ttk.Frame(self.root)
        fm0.pack()
        fm1.pack()
        fm2.pack(padx=10, expand='yes', fill='both')

        self.eny_t = tk.StringVar()
        self.en1 = ttk.Entry(fm0, width=30, textvariable=self.eny_t)
        self.en1.pack(padx=20, pady=10, side='left')

        self.en1.bind('<Button-3>', self.R_click_en1)

        ttk.Button(fm0, text='查询物料', command=lambda: self.find_code_GUI(
            self.eny_t.get())).pack(padx=20, pady=10, side='right')

        self.lab_r = tk.StringVar()
        ttk.Label(fm2, textvariable=self.lab_r).pack(pady=5)

        self.tev = ttk.Treeview(fm2, columns=('1', '2', '3', '4'))

        self.tev.heading('#0', text='层次/序号')
        self.tev.heading('1', text='编码')
        self.tev.heading('2', text='图号')
        self.tev.heading('3', text='名称')
        self.tev.heading('4', text='数量')

        self.tev.column('#0', width=120, anchor='w', stretch='no')
        self.tev.column('1', width=100, anchor='w', stretch='no')
        self.tev.column('2', width=100, anchor='w', stretch='no')
        self.tev.column('3', width=300, anchor='w')
        self.tev.column('4', width=80, anchor='center', stretch='no')

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
        self.tev.bind('<Button-3>', self.R_click_tree)

    def find_code_GUI(self, x):
        if x in ('', ' '):
            return
        elif len(x) < 3:
            self.lab_r.set('符合条件物料太多，请补充信息')
            return
        for item in self.tev.get_children():  # 对treeview进行清空
            self.tev.delete(item)

        find_code(x.upper().strip())

        if len(rst_code) == 0:
            self.lab_r.set('物料库中不存在')
        else:
            if len(rst_code) > 1:
                self.lab_r.set('有多个编码符合：')
            self.tev.heading('4', text='日期')
            self.tree_out(rst_code)

    def find_bom_GUI(self, x):
        find_bom(x)
        for item in self.tev.get_children():  # 对treeview进行清空
            self.tev.delete(item)
        if rst_bom:
            self.tev.heading('4', text='用量')
            self.tree_out(rst_bom)
        else:
            self.lab_r.set("没有BOM中使用：%s" % x)

    def find_son_GUI(self, x):
        find_son(x)
        for item in self.tev.get_children():  # 对treeview进行清空
            self.tev.delete(item)
        if rst_son:
            self.tev.heading('4', text='用量')
            self.tree_out(rst_son)
            if len(rst_son) == 1:
                self.lab_r.set("该物料没有子零件")

    def tree_out(self, rst):  # 向treeview中写入列表内容
        lv = {0: ''}
        a = len(rst[0][0])-1
        for key in rst:
            i = len(key[0])-a
            lv[i] = self.tev.insert(lv[i - 1],
                                    'end',
                                    text=key[0]+' '+str(key[5]),
                                    values=key[1:5])

    def menu_en1(self,):
        def onpaste(event=None):
            self.en1.event_generate('<<Paste>>')

        def copy(event=None):
            self.en1.event_generate("<<Copy>>")

        def cut(event=None):
            self.en1.event_generate("<<Cut>>")

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="剪切", command=cut)
        self.menu.add_separator()
        self.menu.add_command(label="复制", command=copy)
        self.menu.add_separator()
        self.menu.add_command(label="粘贴", command=onpaste)

    def menu_tree(self,):    # 定义了treeview处的右键菜单内容，但菜单弹出要由post来调用
        def tree_copy(x):
            self.root.clipboard_clear()
            self.root.clipboard_append(x)

        self.menu1 = tk.Menu(self.root, tearoff=0)
        self.menu1.add_command(
            label="复制编码", command=lambda: tree_copy(self.tree_code))
        self.menu1.add_separator()
        self.menu1.add_command(
            label="复制图号", command=lambda: tree_copy(self.tree_draw))
        self.menu1.add_separator()
        self.menu1.add_command(
            label="反查BOM", command=lambda: self.find_bom_GUI(self.tree_code))
        self.menu1.add_separator()
        self.menu1.add_command(
            label="查询子零件", command=lambda: self.find_son_GUI(self.tree_code))

    def menu_bar(self,):   # 定义菜单栏
        m_bar = tk.Menu(self.root)  # 创建菜单组

        m_file = tk.Menu(m_bar, tearoff=0)  # 创建2级菜单组
        m_file.add_separator()
        m_file.add_command(label='导入小批BOM',)
        m_file.add_separator()
        m_file.add_command(label='导入设计BOM',)
        m_file.add_separator()
        m_file.add_command(label='导 入 物 料', )
        # mabr上添加一个标签,链接到file_m
        m_bar.add_cascade(label='导      入', menu=m_file)

        m_view = tk.Menu(m_bar, tearoff=0)  # 创建2级菜单组
        
        v = tk.StringVar()
        for root in all_root:
            # 单选菜单整组有一个variable，每个选项都有一个value。当被选中时，该菜单的value就会赋值给variable。
            
            m_view.add_radiobutton(label=root[0] + root[1], value=root[0], variable=v,
                                   indicatoron=False, command=lambda: self.find_bom_GUI(v.get()))
            m_view.add_separator()
                       
        # mabr上添加一个链接标签,链接到file_m
        m_bar.add_cascade(label=' 查看已导入的BOM ', menu=m_view)

        self.root.config(menu=m_bar)   # 把mbar菜单组 配置到窗体;

    def R_click_en1(self, event):
        self.menu.post(event.x_root, event.y_root)

    def R_click_tree(self, event):   # 鼠标右键触发程序，该程序通过前面的bind 和右键绑定在一起
        iid = self.tev.identify_row(event.y)
        if iid:
            self.tev.selection_set(iid)    # 当右键时选中目前鼠标所在的行
            self.tree_code = self.tev.item(self.tev.selection(), 'values')[0]
            self.tree_draw = self.tev.item(self.tev.selection(), 'values')[1]
            self.tree_code = self.tree_code.replace(' old', '')
            self.menu1.post(event.x_root, event.y_root)


def find_bom(f):    # 根据编码反查使用的BOM
    # 根据之前找到物料的层次,向前查找上一层, 再继续向前查找更上层, 直到层次为 1;
    def find_lv(lv):
        for fu in all_bom[root][num-1::-1]:
            if len(fu[0]) == lv - 1:
                lv -= 1
                if rst_lv.get(lv, 'NA') == fu[1]:  # 如果上一层父项已经存在,则停止
                    break
                elif lv == 1:      # 如果是顶层,则进行添加,并终止
                    rst_lv[1] = fu[1]
                    rst_1.append(fu)
                    break
                else:  # 如果不是顶层并且层次内不存在,则添加后, 并继续向下查找
                    rst_lv[lv] = fu[1]
                    rst_1.append(fu)
    global rst_bom
    rst_bom.clear()
    rst_lv = {}
    if f in all_bom:
        # 这里改变了rst_bom的内存指向，所以必须声明global，如果是用append，都是在原内存操作，所以不必声明
        rst_bom=all_bom[f]   
    else:
        for root in all_bom:
            if root == 'index':
                continue
            # all_bom {root:[[lv,code,num],    ],   }
            for num, item in enumerate(all_bom[root]):
                lv = len(item[0])           # 获得当前物料的层次号
                for x in range(lv, 6):           # 对该层次信息中 大于该物料的子层清空
                    rst_lv[x] = ''
                if f in item[1]:  # 找到该物料, 添加到临时列表
                    rst_lv[lv] = item[1]
                    rst_1 = []
                    rst_1.append(item)
                    if lv == 1:   # 如果是顶层，则添加后停止
                        rst_bom.append(item)
                        break
                    else:          # 向前去查找上一层
                        find_lv(lv)
                        for y in rst_1[::-1]:
                            rst_bom.append(y)

    fmt_rst(rst_bom)


def get_code(s):
    sa = s.replace('P', '')
    if sa in all_code:
        return [s, all_code[sa][1], all_code[sa][2]]
    else:
        return [s + ' X', 'X', '物料库中不存在']


def find_code(f):  # 根据输入内容查找物料，先用字典key查找，如果没有则进入模糊查询
    rst_code.clear()
    if f in all_code:
        rst_code.append(all_code[f])
    else:
        f = f.replace('*', '.*')    # 将windows习惯用法的 * 转换为python中的 .*
        f = re.compile(f)           # 使用正则表达式中通配符进行查询
        for item in list(all_code.values()):
            for m in item[:3]:
                if m and f.search(m):
                    rst_code.append(item)
    fmt_rst(rst_code)


def find_son(f):      # 根据编码查找子零件
    rst_son.clear()
    lv = 0
    for root in all_bom:
        if root == 'index':
            continue
        for a in all_bom[root]:  # all_bom {root:[[lv,code,num],    ],   }
            if f in a[1]:  # 找到该物料, 后面的都进行添加，直到层次小于等于的它的
                lv = len(a[0])
                rst_son.append(a)
                continue
            if lv:
                if len(a[0]) > lv:
                    rst_son.append(a)
                else:
                    break
        if rst_son:
            break
    fmt_rst(rst_son)


def fmt_rst(rst):  # 对查询结果进行格式化，添加层次、序号、物料信息等
    if not rst:
        return
    if len(rst[0]) == 4:
        # 如果是单个物料列表，原结构为[code,draw,name,datetime],处理后为：[层次(均为' ')，code,draw,name,datetime,序号]
        for n, key in enumerate(rst):
            rst[n] = [' '] + key[:] + [n + 1]

    elif len(rst[0]) == 3:
        # 如果是BOM列表，原结构为[层次，code,num],处理后为：[层次，code,draw,name,num,层序号]
        lv_n = [0 for n in range(0, 7)]
        for n, key in enumerate(rst):
            for x in range(len(key[0])+1, 7):
                lv_n[x] = 0
            lv_n[len(key[0])] += 1
            rst[n] = [rst[n][0]] + \
                get_code(rst[n][1]) + [rst[n][2]] + [lv_n[len(key[0])]]


def read_date():    # 从现有文件读取数据
    global all_code, all_bom
    with open('all_code.json', 'r', encoding='utf-8') as fc:
        all_code = json.load(fc)

    with open('all_bom.json', 'r', encoding='utf-8') as fb:
        all_bom = json.load(fb)

    print('code库记录: ', len(all_code))
    print('bom库记录: %d ,已读取的产品有:' % len(all_bom))

    for root in all_bom['index']:
        print(root[1])
        xx = root[1].split(" ")
        all_root.append([xx[0], xx[1]])
        all_code[xx[0]] = [xx[0], '-', xx[1], '-']  # 把BOM表中的产品名写入code表
    
    all_root.sort(key=lambda x:x[0])


all_code = {}
all_bom = {}
all_root = []
rst_code = []
rst_bom = []
rst_son = []

read_date()
op = app()
op.root.mainloop()
