import tkinter as tk

class StatusBar(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='0000').place(x=0, y=0, relwidth=1,bordermode=tk.OUTSIDE)
        self.m=6  #有6个子栏
        self.l=[]
        self.l1 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='状态栏',justify=tk.CENTER)
        self.l1.pack(side=tk.LEFT,padx=2,pady=1)
        self.l.append(self.l1)
        self.l2 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='')
        self.l2.pack(side=tk.LEFT,padx=2,pady=1)
        self.l.append(self.l2)
        self.l3 = tk.Label(self, bd=1, anchor=tk.W,relief=tk.SUNKEN,text='')
        self.l3.pack(side=tk.LEFT,padx=2,pady=1)
        self.l.append(self.l3)
        self.l4 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='')
        self.l4.pack(side=tk.LEFT,padx=2,pady=1)
        self.l5 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='')
        self.l5.pack(side=tk.LEFT,padx=2,pady=1)
        self.l6 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='')
        self.l6.pack(side=tk.LEFT,padx=2,pady=1)
        self.l.append(self.l4)
        self.l.append(self.l5)
        self.l.append(self.l6)

    def text(self,i,t): #输出文字信息
        self.l[i].config(text=t)
        self.l[i].update_idletasks()

    def config(self,i,**kargs):  #配置长度 和 颜色
        for x,y in kargs.items():
            if x=='text':
                self.l[i].config(text=y)
            if x=='color':
                self.l[i].config(fg=y)
            if x=='width':
                self.l[i].config(width=y)

    def clear(self):  #清除所有信息
        for i in range(0,self.m):
            self.l[i].config(text='')
            self.l[i].update_idletasks()

    def set(self,i, format, *args):   #输出格式信息
        self.l[i].config(text=format % args)
        self.l[i].update_idletasks()

