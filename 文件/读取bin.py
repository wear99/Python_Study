import re,tkinter
import tkinter.filedialog
from tkinter import ttk



def openfile():    
    f=tkinter.filedialog.askopenfilename()
    with open(f, 'rb') as file:
        txt = file.read()

    txt = str(txt).replace(r'\n','').replace(r'\t','').replace(r'\r','')

    pn = re.compile(r'\\xff\\xff.*?\\xfe\\xff')

    for item in re.findall(pn, txt):
        item = item.split(r'\x')
        item.reverse()
        d1 = int(item[2] + item[3] + item[4] + item[5], 16)
        d0 = int(item[6][:2] + item[7][:2], 16)
        index = int(item[8] + item[9] + item[10] + item[11], 16)
        #rs.append([index, d0, d1, item])
        tev.insert('', 'end', values=(index, d0, d1, item))
        #print('index= ',index,'\td0=',d0,'\td1=',d1,'\t',item)

root = tkinter.Tk()
root.title('物料查询')
root.geometry('800x600')
l1 = tkinter.StringVar()
tkinter.Button(root,text='选择文件',command=openfile).pack()
tev = ttk.Treeview(root, show='headings',columns=('1', '2', '3','4'),selectmode='browse')
tev.heading('1', text='index')
tev.heading('2', text='d0')
tev.heading('3', text='d1')
tev.heading('4', text='数据')
tev.pack()

root.mainloop()