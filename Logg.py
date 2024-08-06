import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

class Log(tk.Frame):
    def __init__(self,_master):
        super().__init__()
        self.log = ""
        self.logText = ScrolledText(_master,font=('Consolas', 10))
        self.logText["state"] = "disable"
        self.logText.place(relx=0,rely=0.1,relwidth=1,relheigh=0.9)

    def write(self,content,warn:bool = False):
        self.logText.tag_config('warn',foreground="red")
        self.currentTime = datetime.now().strftime("[%H:%M:%S] ")
        self.logText["state"] = "normal"
        self.logText.insert("end",self.currentTime)
        self.logText.insert("end","[warn] ","warn") if warn else None
        self.logText.insert("end",content+"\n")
        self.logText["state"] = "disable"
        self.log = self.logText.get("1.0","end")


    def clear(self):
        self.logText["state"] = "normal"
        self.logText.delete("1.0","end")
        self.logText["state"] = "disable"

    def getText(self):
        return self.log