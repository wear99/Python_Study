# -*- coding:utf-8 -*-

#程序主页面
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
from tkinter.simpledialog import askstring
import re,logging,traceback,sys
from os import path,listdir,startfile
from datetime import datetime

from DesignChangePage import design_change_GUI
from DbEditPage import db_edit

class main_GUI(object):   # 把整个GUI程序 封装在一个类里面
    def __init__(self,master=None,mod=''):    # 窗体定义，基本函数，其它的都靠它来触发
        self.root = master
        tk.Tk.report_callback_exception=self.show_error   #因为tk中异常只在控制台输出，也不会抛出，所以要重写异常处理，增加logging记录功能        
        
        #w, h = self.root.maxsize()
        #self.root.geometry("{}x{}".format(w, h))
        self.root.geometry('1024x600')
        self.mod=mod
        self.all_root=self.mod.get_root()
        self.creatPage()
        self.menu_en1()
        self.menu_tree()
        self.menu_bar()
        self.creat_cmb_list()
        #ttk.Style().theme_use('clam')   #('clam','alt','default','classic')

    def show_error(self, exc, val, tb):      #在原异常处理下增加了logging 
        print("Exception in Tkinter callback", file=sys.stderr)
        sys.last_type = exc
        sys.last_value = val
        sys.last_traceback = tb
        traceback.print_exception(exc, val, tb)

        err = 'Exception in Tkinter callback\n'
        for item in traceback.format_exception(exc, val, tb):
            err=err+item
        logging.warning(err)
        self.lab_text.set('')
        tkinter.messagebox.showerror(title='程序错误',message=err)

    def creatPage(self,):    # 把界面内容放在一个一起了，便于修改
        fm0 = ttk.Frame(self.root)
        fm1 = ttk.Frame(self.root)
        fm2 = ttk.Frame(self.root)
        fm0.pack()
        fm1.pack()
        fm2.pack(padx=10, expand='yes', fill='both')

        self.t1 = tk.StringVar()
        self.t2=tk.StringVar()

        self.eny_t = tk.StringVar()        
        #self.en1 = ttk.Entry(fm0, width=30, textvariable=self.eny_t,font=("微软雅黑", 12))
        self.en1 = ttk.Combobox(fm0, width=30, textvariable=self.eny_t,font=("微软雅黑", 12))
        self.en1.pack(padx=10, pady=10, side='left')
        self.en1.bind('<Button-3>', self.R_click_en1)
        self.en1.bind("<Return>", self.en1_enter)

        self.cmb_eny=tk.StringVar()
        self.cmb = ttk.Combobox(fm0, height=15,width=25,textvariable=self.cmb_eny)
        self.cmb.pack(padx=10, pady=10, side='left')
        self.cmb["state"] = "readonly"
        
        self.cmb_eny_1=tk.StringVar()
        self.cmb_1 = ttk.Combobox(fm0, height=15,width=8,textvariable=self.cmb_eny_1)
        self.cmb_1.pack(padx=10, pady=10, side='left')
        self.cmb_1["state"] = "readonly"
        self.cmb_1["value"]=['AND','OR']
        self.cmb_1.current('0')
        #self.cmb.bind("<<ComboboxSelected>>", self.cmb_select)

        #对于和事件绑定的函数,会自动给个event参数,所有在定义时要加上event参数
        
        self.find_iid=self.find_yeild()
        ttk.Button(fm0,
                   text='表内查找\下一个', command=self.find_treebom_GUI).pack(padx=20, pady=10, side='right')
        
        ttk.Button(fm0,
                   text='物料/图纸查询',command=self.en1_enter).pack(padx=20, pady=10, side='right')
                       
        self.lab_text = tk.StringVar()
        ttk.Label(fm2, textvariable=self.lab_text,font=("微软雅黑", 12,'italic')).pack(pady=5)
        
        self.tev = ttk.Treeview(fm2, columns=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'), selectmode='browse')

        self.tree = {}
        self.tree_select={}
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

    def creat_cmb_list(self,):   #需要输入self.all_root来生成列表
        '用于生成BOM选择下拉框内容'
        cmb_list={}
        if 'BATCH' in self.all_root:
            for i, j in self.all_root['BATCH'].items():
                cmb_list[i+' '+j+' BATCH']=i
        if 'DESIGN' in self.all_root:
            for i, j in self.all_root['DESIGN'].items():
                cmb_list[i+' '+j+' DESIGN']=i
        
        self.cmb["value"] = ['所有',]+list(cmb_list.keys())        
        self.cmb.current('0')

    def cmb_recently(self,x):
        cmb_re = list(self.en1['value'])
        if not cmb_re:
            cmb_re = []

        if x in cmb_re:
            cmb_re.remove(x)
        cmb_re.insert(0, x)
        if len(cmb_re) > 12:
            del cmb_re[-1]
        self.en1['value'] = cmb_re

    def menu_en1(self,):        # 输入框的右键菜单
        def onpaste(event=None):
            self.en1.event_generate('<<Paste>>')
        def copy(event=None):
            self.en1.event_generate("<<Copy>>")
        def cut(event=None):
            self.en1.event_generate("<<Cut>>")

        self.menu_eny1 = tk.Menu(self.root, tearoff=0)
        self.menu_eny1.add_command(label="剪切", command=cut)
        self.menu_eny1.add_separator()
        self.menu_eny1.add_command(label="复制", command=copy)
        self.menu_eny1.add_separator()
        self.menu_eny1.add_command(label="粘贴", command=onpaste)

    def menu_tree(self,):    # 定义了treeview处的右键菜单内容，但菜单弹出要由post来调用
        def tree_copy(x):
            self.root.clipboard_clear()
            self.root.clipboard_append(x)

        self.menu_tree_code = tk.Menu(self.root, tearoff=0)
        self.menu_tree_code.add_command(
            label="复制", command=lambda: tree_copy(self.tree_select['item']))
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(
            label="复制物料信息", command=lambda: tree_copy(self.tree_select['code']+'; '+self.tree_select['draw']+'; '+self.tree_select['name']))
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(
            label="反查小批BOM", command=lambda: self.find_parent_GUI(self.tree_select['code'], db='BATCH'))
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(
            label="查询小批BOM子件", command=lambda: self.find_child_GUI(self.tree_select['code'],db='BATCH'))
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(
            label="反查设计BOM", command=lambda: self.find_parent_GUI(self.tree_select['code'], db='DESIGN'))
        self.menu_tree_code.add_separator()

        self.menu_tree_code.add_command(
            label="查询设计BOM子件", command=lambda: self.find_child_GUI(self.tree_select['code'], db='DESIGN'))
        self.menu_tree_code.add_separator()        
        self.menu_tree_code.add_command(label="打开图纸", command=self.open_draw_GUI)        
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(label="导出列表",command=self.tree_save)
        self.menu_tree_code.add_separator()
        self.menu_tree_code.add_command(
            label="查看设计更改", command=lambda: self.find_design_change([self.tree_select['code'], self.tree_select['draw']], op='OR'))

        self.menu_tree_path = tk.Menu(self.root, tearoff=0)
        self.menu_tree_path.add_command(label="添加目录", command=lambda: self.edit_path(type='ADD'))
        self.menu_tree_path.add_separator()
        self.menu_tree_path.add_command(label="删除目录", command=lambda: self.edit_path(type='DEL'))
        self.menu_tree_path.add_separator()
        self.menu_tree_path.add_command(label="重新搜索目录", command=lambda: self.edit_path(type='UPDATE'))
        self.menu_tree_path.add_separator()
        self.menu_tree_path.add_command(label="打开", command=lambda: self.open_path(self.tree_select['path']))
        self.menu_tree_path.add_separator()

    def menu_bar(self,):   # 定义菜单栏
        def creat_file_menu():
            m_file = tk.Menu(m_bar, tearoff=0)  # 创建2级菜单组
            m_file.add_separator()
            m_file.add_command(label='导入ERP BOM',command=lambda: self.read_bom_GUI(tp='BATCH'))
            m_file.add_separator()        
            m_file.add_command(label='导入设计BOM',command=lambda: self.read_bom_GUI(tp='DESIGN'))
            m_file.add_separator()
            m_file.add_command(label='导入定制BOM',command=lambda: self.read_bom_GUI(tp='CUSTOM'))
            m_file.add_separator()
            m_file.add_command(label='导入实验BOM',command=lambda: self.read_bom_GUI(tp='EXPER'))
            m_file.add_separator()
            m_file.add_command(label='导入设计更改清单',command=self.read_design_change_GUI)
            m_file.add_separator()            
            m_file.add_command(
                label='仅读取BOM', command=lambda: self.read_temp_GUI(tp='TEMP'))
            m_file.add_separator()
            m_file.add_command(label='更新物料库',command=self.read_code_GUI)
            m_file.add_separator()
            m_file.add_command(label='导出模板', command=self.download_template_GUI)
            m_file.add_separator()
            # mabr上添加一个标签,链接到file_m
            m_bar.add_cascade(label='读取EXCEL文件', menu=m_file)

        def creat_cost_menu():
            m_cost = tk.Menu(m_bar, tearoff=0)
            m_cost.add_separator()
            m_cost.add_command(label='导入成本文件', command=self.read_cost_GUI)
            m_cost.add_separator()
            m_cost.add_command(label='成本变动物料', command=self.view_changed_cost)
            m_cost.add_separator()
            m_cost.add_command(label='重算BOM成本',command=self.recalc_tree_cost_GUI)
            m_cost.add_separator()
            m_cost.add_command(label='查看物料成本', command=self.tree_add_cost)

            m_bar.add_cascade(label='成本', menu=m_cost)

        def creat_view_menu():
            m_view = tk.Menu(m_bar, tearoff=0)  # 创建2级菜单组
            m_view_b = tk.Menu(m_bar, tearoff=0)
            m_view_d = tk.Menu(m_bar, tearoff=0)
            m_view_ex = tk.Menu(m_bar, tearoff=0)
            m_view_cs = tk.Menu(m_bar, tearoff=0)
            m_view_dc = tk.Menu(m_bar, tearoff=0)
            m_view_dc_feeder=tk.Menu(m_bar, tearoff=0)
            m_view_dc_floder = tk.Menu(m_bar, tearoff=0)
            m_view_dc_tf = tk.Menu(m_bar, tearoff=0)
            m_view_dc_other=tk.Menu(m_bar, tearoff=0)

            root_b = tk.StringVar()
            
            if 'BATCH' in self.all_root:
                for root,name in self.all_root['BATCH'].items():
                    # 单选菜单整组有一个variable，每个选项都有一个value。当被选中时，该菜单的value就会赋值给variable。
                    m_view_b.add_radiobutton(label=root +' '+ name, value=root, variable=root_b,
                                        indicatoron=False, command=lambda: self.find_child_GUI(root_b.get()))
                    m_view_b.add_separator()
            if 'DESIGN' in self.all_root:        
                for root,name in self.all_root['DESIGN'].items():
                    m_view_d.add_radiobutton(label=root +' '+ name, value=root, variable=root_b,
                                        indicatoron=False, command=lambda: self.find_child_GUI(root_b.get(),db='DESIGN'))
                    m_view_d.add_separator()
            if 'EXPER' in self.all_root:
                for root, name in self.all_root['EXPER'].items():
                    m_view_ex.add_radiobutton(label=root + ' ' + name, value=root, variable=root_b,
                                            indicatoron=False, command=lambda: self.find_child_GUI(root_b.get(), db='DESIGN'))
                    m_view_ex.add_separator()
            if 'CUSTOM' in self.all_root:
                for root, name in self.all_root['CUSTOM'].items():
                    m_view_cs.add_radiobutton(label=root + ' ' + name, value=root, variable=root_b,
                                            indicatoron=False, command=lambda: self.find_child_GUI(root_b.get(), db='DESIGN'))
                    m_view_cs.add_separator()
            if 'CHANGE' in self.all_root:
                m_view_dc.add_cascade(label='展布机', menu=m_view_dc_feeder)
                m_view_dc.add_cascade(label='折叠机', menu=m_view_dc_floder)
                m_view_dc.add_cascade(label='毛巾折叠机', menu=m_view_dc_tf)
                m_view_dc.add_cascade(label='其它', menu=m_view_dc_other)
                for root, name in self.all_root['CHANGE'].items():
                    if re.findall(r'展布机',root):
                        mu=m_view_dc_feeder
                    elif re.findall(r'折叠机',root):
                        mu=m_view_dc_floder
                    elif re.findall(r'毛巾折叠机', root):
                        mu = m_view_dc_tf
                    else:
                        mu=m_view_dc_other

                    mu.add_radiobutton(label=root, value=root, variable=root_b,
                                            indicatoron=False, command=lambda: self.find_design_change([root_b.get()],))
                    mu.add_separator()

            m_view.add_cascade(label=' 小批 BOM ', menu=m_view_b)
            m_view.add_separator()
            m_view.add_cascade(label=' 设计 BOM ', menu=m_view_d)
            m_view.add_separator()
            m_view.add_cascade(label=' 实验 BOM ', menu=m_view_ex)
            m_view.add_separator()
            m_view.add_cascade(label=' 定制 BOM ', menu=m_view_cs)
            m_view.add_separator()
            m_view.add_cascade(label=' 设计更改单', menu=m_view_dc)
            m_view.add_separator()

            def view_root(type): # 查询所有BOM列表，并在tree中显示
                
                pass

            m_view.add_command(label='小批 BOM', command=lambda:view_root('BATCH'))
            m_view.add_separator()

            m_view.add_command(label='试制 BOM', command=lambda:view_root('DESIGN'))
            m_view.add_separator()

            m_view.add_command(label=' 列表全部展开 ', command=lambda:self.tree_fold(unfold=True))
            m_view.add_separator()
            m_view.add_command(label=' 列表全部折叠 ', command=lambda: self.tree_fold(unfold=False))
            m_view.add_separator()
            m_view.add_command(label='BOM去除装配体', command=self.remove_assemble_GUI)

            m_bar.add_cascade(label=' 查看BOM ', menu=m_view)

        def creat_path_menu():
            m_path = tk.Menu(m_bar, tearoff=0)
            draw_p = tk.StringVar()
            if 'PATH' in self.all_root:
                for key, item in self.all_root['PATH'].items():
                    m_path.add_radiobutton(label=key, value=item, variable=draw_p,
                                        indicatoron=False, command=lambda: self.open_path(draw_p.get()))
                    m_path.add_separator()
            
            m_path.add_command(label='编辑图纸目录', command=self.view_drawpath)        
            m_bar.add_cascade(label='图纸目录', menu=m_path)

        def creat_change_menu():
            m_change = tk.Menu(m_bar, tearoff=0)
            m_change.add_command(label='设计更改查询', command=lambda:design_change_GUI(self.root,self.mod))
            m_bar.add_cascade(label='设计更改', menu=m_change)
        
        def creat_tool_menu():
            m_tool = tk.Menu(m_bar, tearoff=0)
            m_tool.add_separator()
            m_tool.add_command(label='检查Excel编码', command=lambda:self.check_excel_GUI(tp='CHECK'))
            m_tool.add_separator()
            m_tool.add_command(label='计算部件数量', command=lambda: self.check_excel_GUI(tp='QTY'))
            
            m_tool.add_separator()
            m_tool.add_command(label='去除装配体', command=lambda: self.read_temp_GUI(tp='REMOVE'))
            m_tool.add_separator()
            m_tool.add_command(label='数据库操作', command=self.edit_db_GUI2)
            
            m_bar.add_cascade(label='EXCEL工具', menu=m_tool)

        def creat_about_menu():
            m_bar.add_command(label='版本', command=self.ver)

        m_bar = tk.Menu(self.root)  # 创建菜单组
        creat_file_menu()
        creat_cost_menu()
        creat_view_menu()
        creat_path_menu()
        creat_change_menu()
        creat_tool_menu()
        creat_about_menu()
        self.root.config(menu=m_bar)  # 把mbar菜单组 配置到窗体;
 #-----------------以下窗口动作触发------------------------------      
    def R_click_en1(self, event):   # 输入框绑定动作
        self.menu_eny1.post(event.x_root, event.y_root)   # 在事件坐标处,弹出对应的菜单

    def R_click_tree(self, event):   # 鼠标右键绑定的动作，该程序通过前面的bind 和右键绑定在一起
        iid = self.tev.identify_row(event.y)   # 返回事件发生时鼠标坐标对应的行
        n=self.tev.identify_column(event.x)
        if iid:  # 如果鼠标所在是空,则不执行右键动作
            self.tree_select['id'] = iid    # 当右键时选中目前鼠标所在的行id
            self.tev.selection_set(iid)     
            self.tree_select['x'] = event.x_root
            self.tree_select['y'] = event.y_root
            n=int(n.replace('#',''))
            self.tree_select['item'] = self.tev.item(iid, 'values')[n-1]

            if self.tree['type'] in ('CODE','CODE-COST','BOM','BOM-COST','BOM-SINGLE'):                
                self.tree_select['code'] = self.tev.item(self.tev.selection(), 'values')[0]
                self.tree_select['draw'] = self.tev.item(self.tev.selection(), 'values')[1]
                self.tree_select['name'] = self.tev.item(self.tev.selection(), 'values')[2]

                if self.tree_select['code'] == '':
                    self.tree_select['code'] = self.tree_select['draw'] + self.tree_select['name']

                self.menu_tree_code.post(event.x_root, event.y_root)
            elif self.tree['type'] == 'PATH':
                self.tree_select['path'] = self.tev.item(self.tev.selection(), 'values')[1]
                self.tree_select['file'] = self.tev.item(self.tev.selection(), 'values')[0]
                self.menu_tree_path.post(event.x_root, event.y_root)

    def get_input(self,):
        x = self.en1.get()
        if x in ('', ' ', None):
            return

        x = x.upper()  # 转大写，去首尾空格
        x = x.replace('\n', '')  # 去掉换行符        
        xx = x.split()
        root = self.cmb_eny.get().split(" ")[0]
        db1=self.cmb_eny.get().split(" ")[-1]
        option = self.cmb_eny_1.get()

        self.cmb_recently(x)

        return xx,root,option,db1

    def en1_enter(self, event=None):  #和事件绑定的函数,在事件触发时,会自动给一个event参数,所有定义时必须加上
        '当下拉框为 所有或空时，直接进行编码库查询；否则进入选择的BOM中查询'
        en1,en2,en3,db1=self.get_input()
        if en2 == '所有':
            self.find_code_GUI(en1,en3)
        else:
            self.find_child_GUI(en2,db=db1)
            self.find_treebom_GUI(out=True)

    def find_yeild(self,):
        while True:
            try:
                for iid in self.tree['search_iid']:
                    if iid not in self.tree['search_iid']:   #迭代器时不会实时更新
                        break
                    self.tev.selection_set(iid)
                    self.tev.see(iid)
                    yield
            except:
                pass

    def about(self,):
        txt=''
        ver = {'#3.21':'V1.0完成带子层结构BOM的查询功能',
        '# 3.22': '添加读取小批BOM功能,然后写入小批BOM库和原始结构库',
        '# 3.26': '添加物料读取,并写入物料库',
        '# 3.27': '增加在窗口列表查询功能',
        '# 3.29': '读取设计BOM,并匹配编码,在设计BOM中查找物料',
        '# 4.5': '增加成本读取和匹配功能',        
        '# 4.12': '存储格式由JSON改为sqlite数据库,启动时读取数据库到各字典中',       
        '# 4.23': '将designbom改为按小批物料格式存储，新增designcode库，存储15R，16R，24R，28R及没编码物料',       
        '# 4.28': '增加图纸路径读取保存,物料根据图号打开对应的图纸',
        '# 0.51':'增加指定BOM查询功能'}
        ver['2020.12.05 Ver:0.49']='增加对数据库直接编辑功能'
        ver['2020.12.11 Ver:0.50 ']='对excel查询编码功能进行升级，存在多个编码时进行备注'
        ver['2020.12.22 Ver:0.51 '] = '增加版本及更新内容说明'
        for (i,j) in ver.items() :
            txt =  i + '\n\t' + j+ '\n'+txt
            
        tk.messagebox.showinfo(title='关于',message=txt)
    def ver(self,):
        file1=sys.argv[0]
        #file=sys.argv[0]
        f2=path.join(path.dirname(file1),'batchITEM.db')
        t1=datetime.fromtimestamp(path.getmtime(file1))
        t1=str(t1.strftime('%Y-%m-%d'))
        t2=datetime.fromtimestamp(path.getmtime(f2))
        t2=str(t2.strftime('%Y-%m-%d'))
        
        tk.messagebox.showinfo(title='版本',message='程序信息：'+t1+'\n'+'数据库信息：'+t2)

 #-----------------以下窗口动作函数--------------------------------        
    def rst_check(self,rst,tar='bom'):
        if 'error' in rst:
            self.lab_text.set(rst['error'])
        elif 'skip' in rst:
            self.lab_text.set(rst['skip'])
        elif 'itemerror' in rst:
            self.lab_text.set('表格内有如下错误：')
            self.tree_out(rst['itemerror'])
        elif tar in rst:
            return True

    def find_code_GUI(self,x,op='AND'):
        '根据输入框的内容，先在物料库中查询，如果没有则去图纸库查询'
        rst={}
        tp='CODE'
        rst=self.mod.find_code(x,'',op)   #先在小批物料库中进行查找 
        
        if not rst:
            rst = self.mod.find_db('draw', x[0], 'drawPATH')  # 最后在图纸中查找
            if rst:
                rst.sort(key=lambda x: x[0])
                tp = 'PATH'
                rst['code']=rst

        if 'code' in rst:            
            many='共查找到%d条物料'%len(rst['code'])
            if len(rst['code']) > 200:
                many += ',只显示200条'
                
            rst['code'] = [(1,) + tuple(x) for x in rst['code']]
            self.lab_text.set(str(x)+' 的物料查询结果: '+many)
            self.tree_out(rst['code'][:200],type=tp)
        else:
            self.lab_text.set(str(x) + ' 未找到相关物料或图纸:')

    def find_parent_GUI(self,x,db='BATCH'):
        if db=='BATCH':
            rst = self.mod.find_parent_bom(x,db)            
        elif db=="DESIGN":
            rst = self.mod.find_in_bom(x,db,True,False)
        
        if 'bom' in rst:
            self.lab_text.set(str(x)+' 的反查结果:')
            self.tree_out(rst['bom'],unfold=5)            
        else:
            self.lab_text.set('没有BOM中使用此物料：%s'%str(x))

    def find_child_GUI(self,x,db='BATCH'):        
        if db=='BATCH':
            rst = self.mod.find_child_bom(x,db)            
        elif db=="DESIGN":
            rst = self.mod.find_in_bom(x,db, False,True)
             
        if 'bom' in rst:
            self.lab_text.set(str(x)+' 的子项结构查询结果')
            self.tree_out(rst['bom'])
        else:
            self.lab_text.set('%s 物料没有子零件'%str(x))

    def find_design_change(self,itemlist=[],op='AND'):
        if not itemlist:
            return        

        for item in itemlist:
            item=re.sub('[(]A\d[)]','',item)

        x=design_change_GUI(self.root,self.mod)
        x.find_change_GUI(itemlist,op)

    def read_bom_GUI(self,tp='BATCH'):
        #rst={}
        file_name = tk.filedialog.askopenfilename(title='打开BOM文件',filetypes=[('xlsx', '*.xlsx'),])  
        if not file_name:
            return      
        rst = self.mod.read_design_BOM(file_name, tp)
        if self.rst_check(rst,'bom'):
            wr2 = tk.messagebox.askquestion(message='对已存在的小批BOM结构或设计物料信息,是否覆盖?')
            if wr2=='yes':
                tp1 = 'W'
            else:
                tp1='R'
            rst_t1 = self.mod.update_to_bom_db(rst['bom'], tp, tp1)
            self.lab_text.set(rst_t1)

    def read_temp_GUI(self,tp='TEMP'):
        def bom_total(bom):
            # 计算反查物料在顶层的总用量,和本层用量
            lv_num = {0: 1, 1: 1}
            for item in bom:
                lv_num[item[0]] = item[4] * lv_num[item[0] - 1]
                if len(item)>5:
                    item.insert(5,lv_num[item[0]])
                else:
                    item.append(lv_num[item[0]])
            return bom

        file_name = tk.filedialog.askopenfilename(title='打开BOM文件',filetypes=[('xlsx', '*.xlsx'),])        
        rst = self.mod.read_design_BOM(file_name, tp)
        if self.rst_check(rst,'bom'):
            rst['bom']=bom_total(rst['bom'][1:])
            if tp=='TEMP':
                self.tree_out(rst['bom'],)
            elif tp=='REMOVE':
                single_bom,del_bom=self.mod.remove_assemble(rst['bom'])
                file_name = tk.filedialog.asksaveasfilename(title='保存文件',filetypes=[('xlsx', '*.xlsx'),])
                self.mod.save_to_excel(file_name, single_bom,)
                self.tree_out(single_bom,)

    def check_excel_GUI(self,tp='CHECK'):   #查找excel表编码
        def check_bom(bom,col):
            rst={}
            checked={}
            for item in bom:
                if (item[0], item[1], item[2]) in checked:   #对于已查找过物料，直接使用之前查询结果
                    code = checked[(item[0], item[1], item[2])]
                else:
                    code = self.mod.check_code(item[0], item[1], item[2])
                    checked[(item[0], item[1], item[2])]=code

                rst[str(item[-1])+'#'+str(col)]=code                
            return rst
        def check_QTY(bom,col):
            rst={}
            lv_num={0:1}
            for item in bom:
                lv=item[0]
                num=item[2]
                for n in range(lv + 1, 7):
                    lv_num[n]=0
                lv_num[lv] = num * lv_num[lv - 1]
                rst[str(item[-1])+'#'+str(col)]={'new':lv_num[lv],'old':num}
            return rst             

        file_name = tk.filedialog.askopenfilename(title='打开BOM文件',filetypes=[('xlsx', '*.xlsx'),])
        if not file_name:
            return
        rst = self.mod.read_design_BOM(file_name, type=tp)        
        if self.rst_check(rst, 'bom'):
            self.lab_text.set('读取完毕，正在处理数据...')
            self.root.update()
            rst_new={}
            if tp=='CHECK':
                col=rst['col']['code']+2
                rst_new['modify']=check_bom(rst['bom'][1:],col)
                rst_new['insert_col']= col
            elif tp=='QTY':
                col=rst['col']['num']+2
                rst_new={}
                rst_new['modify']=check_QTY(rst['bom'][1:],col)
                rst_new['insert_col']= col
            else:
                return

            self.lab_text.set('正在写入Excel表格...')
            self.root.update()
            r=self.mod.modify_excel(file_name ,rst_new)
            if 'error' in r:
                self.lab_text.set(r['error']) 
            else:
                self.lab_text.set('更新完成;')            
        else:
            self.lab_text.set('发生未知错误')

    def read_cost_GUI(self,):
        day_ = askstring('成本日期', "请输入成本生成的日期，决定了是否覆盖已有成本：", initialvalue=self.mod.today)
        if not day_:
            return
        if not re.match(r'\d{4}-\d{2}-\d{2}', day_):
            tk.messagebox.showerror('输入错误','日期输入错误，正确格式应为：2019-05-05 ')
            return

        file_name = tk.filedialog.askopenfilename(title='打开成本文件',
                                                  filetypes=[('xlsx', '*.xlsx'),])
        
        rst = self.mod.read_design_BOM(file_name,type='COST')
        if self.rst_check(rst, 'bom'):
            rst1 = self.mod.update_to_cost_db(rst['bom'], day_)
            if 'error' in rst1:
                self.lab_text.set(rst1['error'])
            else:
                self.lab_text.set(rst1['info'])
                if 'change' in rst1:                    
                    self.tree_out(rst1['change'])            

    def read_code_GUI(self,):
        self.lab_text.set('读取物料库...')
        self.tree_out([], type='UPDATE')
        
        path = '\\\\Sstech\\erp info\\Code\\2010-12-13开始使用新编码\\'        
        filename = [
            'OEM&集成系统&能效系统加工件新编码.xlsx',
            '槽烫加工件新编码.xlsx',
            '干洗加工件新编码.xlsx',
            '干衣机加工件新编码.xlsx',        
            '滚筒烫平机加工件新编码.xlsx',
            '水洗加工件新编码.xlsx',
            '折叠机加工件新编码.xlsx',
            '备品备件新编码.xlsx',
            '标贴和铭牌新编码.xlsx',
            '各种采购件新编码.xlsx',
            '原材料新编码.xlsx',
            '产成品新编码20101213.xlsx'
            ]
        filename1 = [
            '产成品新编码20101213.xlsx',
            ]
            
        files = [path + x for x in filename]        
        read_code = []
        # 开始读取所有code文件---------------------------------------
        self.tev.insert('', 'end', value=('******开始读取物料库******',))
        self.tev.insert('', 'end', value=('   >>>物料库地址：'+path,))
        
        for file in files:
            name = file.split('\\')[-1]
            iid=self.tev.insert('','end',value=('   >>>'+name,))
            self.root.update()

            rst = self.mod.read_design_BOM(file, type='CODE')
            if 'error' in rst:
                self.tev.set(iid, '3', rst['error'])
            if 'skip' in rst:
                self.tev.set(iid, '3', '跳过的工作表：' + rst['skip'])
            if 'bom' in rst:
                n=len(rst['bom'])-1
                self.tev.set(iid, '2', '读取物料：%d'%n)                
                read_code+=rst['bom']                
            if not rst:
                self.tev.set(iid, '2', '读取失败')
                self.tev.set(iid, '3', '发生未知错误')

        # 开始把读取的编码进行更新-------------------------------------------------
        self.lab_text.set('更新物料库...')
        self.root.update()
        rst={}
        if read_code:
            self.tev.insert('', 'end', value=('******开始更新物料库******',))
            self.root.update()
            rst = self.mod.update_to_code_db(read_code)
        else:
            self.lab_text.set('物料库读取失败，请检查路径或文件名是否正确')
            return
        
        if 'error' in rst:
            self.tev.insert('', 'end', value=('   >>>物料库更新错误:',rst['error']))
            self.lab_text.set('更新失败')
        else:
            self.tev.insert('', 'end', value=('   >>>读取的物料总数:', len(read_code)))
            if 'new' not in rst:
                rst['new']=0
            self.tev.insert('', 'end', value=('   >>>新增的物料数:', rst['new']))

            if 'mod' not in rst:
                rst['mod']=[]
            self.tev.insert('', 'end', value=('   >>>修改的物料数:', (len(rst['mod']) / 2)))
            self.tev.insert('', 'end', value=('******修改的物料如下:******',))
            for item in rst['mod']:
                self.tev.insert('', 'end', value=item)
            
        self.tev.insert('', 'end', value=('******物料库更新结束******',))
            #popcode = POP_readcode(self, self.root)
            #self.root.wait_window(popcode.pop)

    def read_design_change_GUI(self,):
        file_name = tk.filedialog.askopenfilename(title='打开设计更改清单',filetypes=[('xlsx', '*.xlsx'),])  
        if not file_name:
            return
        rst = self.mod.read_design_BOM(file_name,'DESIGN_CHANGE')
        if self.rst_check(rst, 'bom'):
            rst1 = self.mod.update_to_change_db(rst['bom'])
            if 'error' in rst1:
                self.lab_text.set(rst1['error'])
            else:
                self.lab_text.set('已成功导入！')
                self.mod.load_design_change()

    def find_treebom_GUI(self,out=False):
        'OUT 控制查找结果是否重新输出。首先确认查找词是否被查询过，如果是则进入循环显示；否则进入查找，并记录查找词，再进入循环显示'
        en1,en2,en3,db1=self.get_input()
        if 'search' not in self.tree or self.tree['search']!=en1:
            self.tree['search']=en1
            rst=self.mod.find_in_bom(en1,self.tree['bom'],parent=True,opt=en3)
            if 'bom' in rst:
                if out:
                    rst['bom']=[x[:-1] for x in rst['bom']]
                    rst['code']=[x[:-1] for x in rst['code']]
                    self.tree_out(rst['bom'])
                    self.tree_bold(rst['code'])
                else:
                    self.tree['search_iid']=[x[-1] for x in rst['code']]
                    self.tree_bold(rst['code'])
                if 'code' in rst:
                    msg = '该物料在BOM中出现 %d 次' % len(rst['code'])
                if 'sum' in rst:
                    msg = '该物料在BOM中出现 %d 次，总用量为：%d' % (len(rst['code']),rst['sum'])                
            else:
                msg = '在BOM中未找到 :-('
            self.lab_text.set(msg)

        if 'search_iid' in self.tree:
            next(self.find_iid)

    def tree_out(self, bom, type='BOM',unfold=1,tag=[]):
        '向treeview中写入列表内容:  bom为输出的列表;  type参数为输出类型,决定列表样式和绑定的右键菜单;     unfold参数是显示默认展开层级;   如果bom是字典，则是对当前BOM进行修改，如果是列表，则重新生成;  tag是要加粗显示的内容列表'
        # BOM格式[0层次,1编码,2图号,3名称,4数量,5本层数量]
        # 设计BOM格式[0层次,1编码,2图号,3名称,4数量,5本层数量,6材料,7备注]
        # 物料格式[0层次,1编码,2图号,3名称,4日期]
        # 成本格式[0层次,1编码,2图号,3名称,4材料成本,5人工成本,6管理成本,7总成本]
        #self.lab_text.set(self.target)
        def set_tree_title():
            tree_title = {
            'CODE': ('序号', '编码', '图号', '名称', '材料', '重量', '备注',),
            'CODE-COST': ('序号', '编码', '图号', '名称', ' ', ' ', '材料成本', '人工', '费用', '单件成本', ' ', '更新日期',),
            'BOM': ('层次', '编码', '图号', '名称', '数量', '部件数量', '材料', '重量', '备注',),
            'BOM-SINGLE':('序号', '编码', '图号', '名称', '数量', '部件数量', '材料', '重量', '备注',),
            'BOM-COST': ('层次', '编码', '图号', '名称', '数量', '部件数量', '材料成本', '人工', '费用', '单件成本', '合计成本', '更新日期',),
            'PATH': ('序号', '图号', '图纸路径','图纸数量'),
            'UPDATE': ('序号','物料文件', '读取结果', '备注信息'),
            }
            title_width = {
                '序号':60,'层次':120,'编码':120, '图号':140, '名称':260, '材料':100, '重量':60,'数量':60, '部件数量':60, '备注':100,'材料成本':60, '人工':60, '费用':60, '单件成本':100,'合计成本':100, '更新日期':300,'图纸路径':400,'物料文件':300,'读取结果':120,'图纸数量':120,'备注信息':300,' ':10,
            }
            
            for n in range(1, 12):  #初始化列宽
                self.tev.column(str(n), width=40)

            if type in tree_title:
                self.tree['col']=tree_title[type]
                for n, name in enumerate(tree_title[type]):
                    if n == 0:
                        n = '#' + str(n)
                    
                    self.tev.heading(str(n), text=name,command=lambda _n=str(n): tree_sort_2(self.tev, _n, False))
                    self.tev.column(str(n), width=title_width[name])

        def tree_sort(tv, col, reverse):
            '对treeview显示内容进行排序，仅对单层结构有效；'
            if self.tree['type'] not in ('CODE', 'BOM-SINGLE','PATH') :
                return
            
            if col == '#0':
                col='0'
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == '0':
                l.sort(key=lambda t: t[1], reverse=reverse)
            else:
                l.sort(key=lambda t: t[0], reverse=reverse)

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            tv.heading(col,command=lambda: tree_sort(tv, col, not reverse))

        def tree_sort_2(tv, col, reverse):
            '用tree-bom列表的项进行排序，再移动treeview显示内容；对多层次也可使用'            
            if col == '#0':
                col = '0'
            l = [(k[int(col)], k[-1]) for k in self.tree['bom']]
            #l = [(tv.set(k, col), k) for k in tv.get_children('')]   #多层次下只能得到最顶层父项id
            if col == '0':
                pt = {0:''}
                for (lv,k) in l:
                    pt[lv] = k
                    tv.move(k, pt[lv-1], 99999)   #重新构建层次关系               
            else:
                try:
                    l.sort(key=lambda t: t[0], reverse=reverse)
                except:  #如果排序错误，说明存在混合格式，把所有字符串当做0，重新排序
                    for n, (val, k) in enumerate(l):
                        if not isinstance(val, (int, float)):
                            l[n]=(0,k)
                    l.sort(key=lambda t: t[0], reverse=reverse)
                
                for index, (val, k) in enumerate(l):
                    tv.move(k, '', index)    #移动的同时删除了层次关系

            tv.heading(col, command=lambda: tree_sort_2(tv, col, not reverse))
            tv.see(tv.selection())    #把选择的行显示出来

        self.tree.clear()
        iid_bom=[]
        self.tree['type'] = type
        set_tree_title()

        if isinstance(bom,dict):  #当输入为字典时，对当前列表进行修改
            for key,item in bom.items():
                for n,v in enumerate(item[1:-1]):
                    self.tev.set(key,column=str(n+1), value=v)
            b=list(bom.values())
            b.sort(key=lambda x: x[-1])
            self.tree['bom'] = b
            return

        for item in self.tev.get_children():  # 对treeview进行清空
            self.tev.delete(item)
        
        lv = {0: ''}
        if bom:
            a = bom[0][0] - 1
        order_n = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for n,key in enumerate(bom):
            order_n[key[0] + 1:8] = 0,0,0,0,0,0,0,0
            order_n[key[0]] += 1

            i = key[0] - a
            lv[i] = self.tev.insert(lv[i - 1], 'end', text=str(order_n[key[0]]), values=key[1:])
            iid_bom.append(tuple(key[:])+(lv[i],))   #把行ID记录到bom列表中，便于后续修改、查询操作
            if i <= unfold:
                self.tev.item(lv[i], open=True)
            if key in tag:
                self.tev.item(lv[i], tag='tar')

        self.tev.tag_configure(
                'tar', foreground='blue', background='red', font=('宋体', 10, 'bold'))
        self.tree['bom']= iid_bom

    def tree_bold(self,iid_list):
        '将给出的iid加粗显示,并展开'
        if 'bom' not in self.tree:
            return

        for item in self.tree['bom']:
            iid=item[-1]
            self.tev.item(iid, tag='',open=False)

            if item[:len(iid_list[0])] in iid_list:
                self.tev.item(iid, tag='tar',open=True)
                iid_p=iid
                for n in (1,2,3):
                    iid_p=self.tev.parent(iid_p)
                    self.tev.item(iid_p,open=True)

        self.tev.tag_configure(
                'tar', foreground='blue', background='red', font=('宋体', 10, 'bold'))

    def tree_fold(self, unfold=True):
        if self.tree['bom']:
            for k in self.tree['bom']:
                self.tev.item(k[-1], open=unfold)

    def tree_save(self,):
        def get_tev_title():
            t={'name':[],'width':[]}
            for n in range(0, 12):
                if n==0:
                    n='#0'
                t['name'].append(self.tev.heading(str(n),)['text'])
                t['width'].append(self.tev.column(str(n),)['width'])                
            return t
        
        file = tk.filedialog.asksaveasfilename(defaultextension=".xlsx",title='保存文件',
                                                  filetypes=[('xlsx', '*.xlsx')])
        col_tit=get_tev_title()
        rst = self.mod.save_to_excel(file, self.tree['bom'], self.lab_text.get(),col_tit)

        if 'error' in rst:
            self.lab_text.set(rst['error'])
        else:
            self.lab_text.set('已成功导出到文件：' + file)
            startfile('file:'+file)

    def download_template_GUI(self,):
        file = tk.filedialog.asksaveasfilename(defaultextension=".xlsx",title='保存文件',
                                                  filetypes=[('xlsx', '*.xlsx')])
        rst = self.mod.download_template(file)
        if 'error' in rst:
            self.lab_text.set(rst['error'])
        else:
            self.lab_text.set('模板已导出：' + file)
            startfile('file:'+file)    

    def recalc_tree_cost_GUI(self,):
        if 'bom' not in self.tree or 'COST' not in self.tree['type']:
            return
        
        #cost=self.tree['bom'][::-1]
        cost_bom = self.mod.recalc_tree_cost(self.tree['bom'][::-1])        
        if cost_bom:
            self.tree_out(cost_bom, type=self.tree['type'],)
            self.lab_text.set('成本已重新计算,* 表示子零件成本不完整')

    def tree_add_cost(self,):
        '在当前显示的物料后添加成本数据'            
        cost_dict = {}
        if 'bom' not in self.tree or self.tree['type'] not in ('BOM','CODE'):
            return
        
        cost_dict=self.mod.bom_add_cost(self.tree['bom'])
        self.tree_out(cost_dict,type=self.tree['type'] + '-COST')

    def view_changed_cost(self,): # 查看变动的成本
        rst = self.mod.view_changed_cost()
        if rst:
            self.lab_text.set('成本变动过的物料如下:')
            self.tree_out(rst, 'CODE-COST')
        else:
            self.lab_text.set('库中物料成本没有发生变化')

    def open_draw_GUI(self,):
        def meun_drawpath():
            self.menu_path_sect = tk.Menu(self.root, tearoff=0)
            path_1 = tk.StringVar()
            for item in rst:
                self.menu_path_sect.add_radiobutton(label=item[1]+'(%s)'%item[2], value=item[1], variable=path_1,
                                   indicatoron=False, command=lambda: self.open_path(path_1.get()))
                self.menu_path_sect.add_separator()

        rst = {}
        if self.tree_select['draw'] != '' and 'GB' not in self.tree_select['draw']:            
            draw=re.sub('[(]A\d[)]','',self.tree_select['draw'])
            rst = self.mod.find_db('draw', draw, 'drawPATH')
            if rst:
                if len(rst) == 1:
                    self.open_path(rst[0][1])                    
                else:
                    meun_drawpath()
                    self.menu_path_sect.post(self.tree_select['x'], self.tree_select['y'])
            else:
                self.lab_text.set('没有找到对应图纸')

    def open_path(self, path):
        try:
            startfile('file:'+path)
        except Exception as ex:
            tk.messagebox.showerror(title='错误',message=ex)

    def remove_assemble_GUI(self,):
        '制作生产BOM：去除原BOM中组合件（有子零件的）、焊接件子零件、原材料，然后将相同项进行数量合并'
        if self.tree['type'] not in ('BOM',):
            return
        bom,del_bom=self.mod.remove_assemble(self.tree['bom'])
        self.tree_out(bom, type='BOM')
        self.lab_text.set(self.lab_text.get()+'(单层)')

    def view_drawpath(self,):
        all_path = []
        path,root = self.mod.load_drawpath_db()
        
        for key,item in path.items():
            all_path.append((1,key,root[key],'',len(item)))
            for file in item:
                all_path.append((2,)+file)
        if not all_path:
            all_path=[(1,"右键添加文件目录","","")]
            
        self.tree_out(all_path,type='PATH',unfold=0)

    def edit_path(self, type='ADD'):
        '编辑目录,包含新增ADD,删除DEL,更新UPDATE 3种模式'
        def get_name():
            name = askstring('', "请输入产品信息：")
            if not name:
                return
            name = name.upper().strip()  # 转大写，去收尾空格
            name = name.replace('\n', '')  # 去掉换行符
            if name in self.all_root['PATH']:
                tk.messagebox.showerror('产品信息已存在，请重新输入！')
            else:
                return name

        def get_path():
            pathdir = tk.filedialog.askdirectory(title='选择图纸文件夹')
            if pathdir in list(self.all_root['PATH'].values()):
                tk.messagebox.showerror('产品文件夹已存在，请重新选择！')
            else:
                return pathdir

        def del_path(name):
            try:
                self.mod.remove_db(del1=(name,), col1='root', sheet='drawPATH')
                self.mod.db_command('ok')
                self.lab_text.set('已成功删除记录: '+str(name))
            except Exception as ex:
                self.mod.db_command('back')
                self.lab_text.set('删除时出错：' + str(ex))

        if type == 'ADD':   # 新增模式下,需输入name,选择目录
            name = get_name()
            if name:
                pathdir = get_path()

            if not (name and pathdir):
                return

            iid=self.tev.insert('', 'end', values=(name, pathdir))
            self.tev.selection_set(iid)
            self.tev.see(iid)
        else:
            iid=self.tev.selection()
            name = self.tree_select['file']
            pathdir = self.tree_select['path']

        if not (name and pathdir):
            return

        if type in ('ADD', 'UPDATE'):  # 扫描指定的文件夹
            self.lab_text.set('正在查找图纸...')
            self.root.update()
            rst={}
            rst = self.mod.scan_path(pathdir)
            if 'error' in rst:
                self.lab_text.set(rst['error'])           
            elif 'path' in rst:
                if type=='UPDATE':
                    del_path(name)
                self.lab_text.set('正在更新图纸库...')

                self.tev.set(iid,'4',len(rst['path']))
                self.root.update()
                
                rst=self.mod.update_to_drawpath_db(name,pathdir,rst['path'])
                self.lab_text.set(rst['txt'])

        elif type in ('DEL',):  # 删除保存的文件夹和所有图纸路径
            self.tev.delete(self.tev.selection())
            del_path(name)
            del self.all_root['PATH'][name]

    def edit_db_GUI2(self,):
        pop = db_edit(self.root,self.mod)
        #self.wait_window(pop)

    def view_root(self,root_type):
        '查询root列表，并显示'
        pass
#----------------------------------------------------------------------------------------------



