import tkinter as tk
from tkinter import ttk
import openpyxl as xl
import json
import re


class main_GUI():   # 把整个GUI程序 封装在一个类里面
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
        self.en1.bind("<Return>", self.en1_enter)
        #对于和事件绑定的函数,会自动给个event参数,所有在定义时要加上event参数
        
        ttk.Button(fm0,
                   text='查询物料',
                   command=lambda: self.find_code_GUI(self.en1.get())).pack(
                       padx=20, pady=10, side='right')

        self.lab_r = tk.StringVar()
        ttk.Label(fm2, textvariable=self.lab_r).pack(pady=5)

        self.tev = ttk.Treeview(fm2, columns=('1', '2', '3', '4','5'))

        self.tev.heading('#0', text='层次/序号')
        self.tev.heading('1', text='编码')
        self.tev.heading('2', text='图号')
        self.tev.heading('3', text='名称')
        self.tev.heading('4', text='数量')
        self.tev.heading('5', text='总数量')

        self.tev.column('#0', width=120, anchor='w', stretch='no')
        self.tev.column('1', width=100, anchor='w', stretch='no')
        self.tev.column('2', width=100, anchor='w', stretch='no')
        self.tev.column('3', width=300, anchor='w')
        self.tev.column('4', width=80, anchor='center', stretch='no')
        self.tev.column('5', width=80, anchor='center', stretch='no')

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

    def find_code_GUI(self,x):
        if x in ('', ' '):
            pass
        elif len(x) < 3:
            self.lab_r.set('符合条件物料太多，请补充信息')
            return
        else:
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

        self.tev.heading('4', text='用量')
        self.tree_out(rst_bom)
        if len(rst_bom)==1:
            self.lab_r.set("没有BOM中使用：%s" % x)

    def find_son_GUI(self, x):
        find_son(x)

        self.tev.heading('4', text='用量')
        self.tree_out(rst_son)
        if len(rst_son) == 1:
            if rst_son[0][4] == 'NA':
                self.lab_r.set("已读取的BOM库中未找到该物料")
            else:
                self.lab_r.set("该物料没有子零件")

    def tree_out(self, rst):  # 向treeview中写入列表内容
        for item in self.tev.get_children():  # 对treeview进行清空
            self.tev.delete(item)
        lv = {0: ''}
        a = len(rst[0][0])-1
        for key in rst:
            i = len(key[0])-a
            lv[i] = self.tev.insert(lv[i - 1],
                                    'end',
                                    text=key[0]+' '+str(key[6]),
                                    values=key[1:6])

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
        for root,name in all_bom_code['index'].items():
            # 单选菜单整组有一个variable，每个选项都有一个value。当被选中时，该菜单的value就会赋值给variable。
            m_view.add_radiobutton(label=root +' '+ name, value=root, variable=v,
                                   indicatoron=False, command=lambda: self.find_bom_GUI(v.get()))
            m_view.add_separator()

        # mabr上添加一个链接标签,链接到file_m
        m_bar.add_cascade(label=' 查看已导入的BOM ', menu=m_view)

        self.root.config(menu=m_bar)   # 把mbar菜单组 配置到窗体;

    def R_click_en1(self, event):
        self.menu.post(event.x_root, event.y_root)   # 在事件坐标处,弹出对应的菜单

    def R_click_tree(self, event):   # 鼠标右键触发程序，该程序通过前面的bind 和右键绑定在一起
        iid = self.tev.identify_row(event.y)   # 返回事件发生时鼠标坐标对应的行
        if iid:   # 如果鼠标所在是空,则不执行右键动作
            self.tev.selection_set(iid)    # 当右键时选中目前鼠标所在的行
            self.tree_code = self.tev.item(self.tev.selection(), 'values')[0]
            self.tree_draw = self.tev.item(self.tev.selection(), 'values')[1]
            self.tree_code = self.tree_code.replace(' old', '')
            self.menu1.post(event.x_root, event.y_root)

    def en1_enter(self,event):   #和事件绑定的函数,在事件触发时,会自动给一个event参数,所有定义时必须加上
        self.find_code_GUI(self.en1.get())

class main_act(main_GUI):
    pass

def find_bom(f):    # 根据编码反查使用的BOM
    # 在字典每个值的里面查找编码,找到后将对应的key,再作为编码进行同样查找,直到key=index
    # all_bom-code是所有从BOM表读出来的物料
    # all_bom只保留有子件的物料,减少数量,便于提高速度

    def find_code_in_bom(x, n):
        for key, item in all_bom.items():
            if key == 'index':
                continue
            for code in item:
                if x in code:
                    rst_1[n] = [n] + code
                    if key in all_bom['index']:
                        if key not in rst_root:
                            rst_root[key] = []
                        rst_1[n + 1] = [n + 1, key, 1]
                        num = n + 2
                        rst_2 = []
                        for y in rst_1[n + 1:0:-1]:
                            rst_2.append([num - y[0], y[1], y[2]])
                        rst_root[key].append(rst_2[:])
                        break
                    else:
                        find_code_in_bom(key, n + 1)
                        break

    def fmt_rst_root():
        for key in rst_root:
            lvcode = {}
            rst_root[key].sort()
            for items in rst_root[key]:
                for item in items:
                    if lvcode.get(item[0], 'NA') != item[1]:
                        lvcode[item[0]] = item[1]
                        for n in range(item[0] + 1, 7):
                            lvcode[n] = ''
                        rst_bom.append([item[0], item[1], item[2]])

    def total_num(x):
        # 计算反查物料在顶层的总用量,和本层用量
        lv_num = {0: 1, 1: 1}
        code_num = [0]
        root_index = 0

        for n, item in enumerate(rst_bom):
            lv_num[item[0]] = item[2] * lv_num[item[0] - 1]
            item.append(lv_num[item[0]])

            if item[1] == x:
                code_num.append(lv_num[item[0]])

            if item[0] == 1 or n == len(rst_bom) - 1:
                rst_bom[root_index][3] = (sum(code_num))
                code_num = [0]
                lv_num = {0: 1, 1: 1}
                root_index = n

    rst_bom.clear()
    rst_1 = ['' for x in range(7)]
    rst_root = {}

    find_code_in_bom(f, 1)

    if rst_root:
        fmt_rst_root()
        total_num(f)
    else:
        rst_bom.append([1,f,'NA'])
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
        rst_code.append(all_code[f][:])
    else:
        f = f.replace('*', '.*')    # 将windows习惯用法的 * 转换为python中的 .*
        x = re.compile(f)           # 使用正则表达式中通配符进行查询
        for item in list(all_code.values()):
            for m in item[:3]:
                if m and x.search(m):
                    rst_code.append(item[:])   #要对元素进行添加,而不是整个地址引用,那样会造成原列表被修改

    for n, key in enumerate(rst_code):
        key.insert(0, '')
        key.append('')
        key.append(n + 1)


def find_son(f):      # 根据编码查找子零件
    def find_son_code(x, n):
        if x in all_bom:
            for item in all_bom[x]:
                rst_son.append([n]+item[:])
                find_son_code(item[0],n+1)

    rst_son.clear()

    if f in all_bom:
        rst_son.append([1,f,1])
        find_son_code(f, 2)
    elif f in all_bom_code:
        rst_son.append([1, f, 1])
    else:
        rst_son.append([1, f, 'NA'])

    fmt_rst(rst_son)


def fmt_rst(rst):  # 对查询结果进行格式化，添加层次、序号、物料信息等
    # 如果是反查BOM列表，原结构为[层次(数字)，code,num,总数量],处理后为：[层次(++)，code,draw,name,num,层序号]
    lv_n = [0 for n in range(0, 7)]
    for n, key in enumerate(rst):
        for x in range(key[0]+1, 7):
            lv_n[x] = 0
        if len(key) == 3:
            key.append('')

        lv_n[key[0]] += 1
        rst[n] = ['+' * key[0]] + get_code(
            key[1]) + [key[2]] + [key[3]] + [lv_n[key[0]]]

def read_date(filename):  # 从现有文件读取数据
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print('读取失败')

def creat_all_bom():
    all_bom_1={}
    for k, v in all_bom_code.items():
        if v:
            all_bom_1[k] = v
    return all_bom_1

def wr_root_to_allcode():
    for root,name in all_bom['index'].items():
        all_code[root] = [root, '-', name, '-']  # 把BOM表中的产品名写入code表

rst_code = []
rst_bom = []
rst_son = []

all_code = read_date('all_code.json')
all_bom_code = read_date('all_bom_code.json')
all_bom=creat_all_bom()
wr_root_to_allcode()


print('code库记录: ', len(all_code))
print('bom库记录: %d ,已读取的产品有:' % len(all_bom), all_bom['index'])
print('有子零件的bom库记录: %d :' % len(all_bom))

op = main_GUI()
op.root.mainloop()
