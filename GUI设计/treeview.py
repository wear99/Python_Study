from tkinter import *
from tkinter import ttk
 
def itemClicked(*args):
    print("click")
 
root = Tk()
# root.geometry("400x400+30+150") 
#ttk.Style().theme_use('clam')
#ttk.Style().configure("Treeview", background="black", fieldbackground="black", foreground="white")
tree = ttk.Treeview(root,columns=('size', 'modified'))
tree['columns'] = ('size', 'modified', 'owner')
 
tree.column('size', width=100, anchor='center')
tree.heading('size', text='Size')
tree.heading('modified', text='modified')
tree.heading('owner', text='owner')
 
tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))
 
# Inserted at the root, program chooses id:
tree.insert('', 'end', 'widgets', text='Widget Tour')
# tree.set('widgets', 'size', '12KB')
size = tree.set('widgets', 'size')
 
# Same thing, but inserted as first child:
tree.insert('', 0, 'gallery', text='Applications', values=("20KB Today jim"))
 
# Treeview chooses the id:
id = tree.insert('', 'end', text='Tutorial')
 
# Inserted underneath an existing node:
tree.insert('widgets', 'end', text='Canvas')
tree.insert(id, 'end', text='Tree')
 
tree.move('widgets', 'gallery', 'end')  # move widgets under gallery
 
# tree.detach('widgets')  # 去除了widgets
#
# tree.delete('widgets')   # 删除widgets
 
tree.item('widgets', open=TRUE)
isopen = tree.item('widgets', 'open')
 
tree.insert('', 'end', text='button', tags=('ttk', 'simple'))
tree.tag_configure('ttk', foreground='blue', background='yellow')

tree.tag_bind('ttk', '<1>', itemClicked)  # the item clicked can be found via tree.focus()
 
tree.pack()
 
root.mainloop()