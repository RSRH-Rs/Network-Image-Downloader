import tkinter as tk
from tkinter import ttk,scrolledtext
from os import system
from threading import Thread
from pathlib import Path

BASEPATH = str(Path(__file__).resolve().parent)
class Terminal(tk.Frame):
    def __init__(self,_master):
        super().__init__()
        self.waiting = False
        self.commandsList = {
            "help":self.__help,
            "clear":self.__clearPrompt,
            "quit":quit,
            "restart":lambda:(_master.master.master.destroy(),system(__file__)),
            "pwd":lambda:(self.insertMessage(__file__)),
            "openCurrentPwd":lambda:(Thread(target=lambda:system("start "+BASEPATH)).start(),self.insertMessage("")),
        }

        self.commandsHelpList = {
            "help":"查看所有指令,或 /help <指令> 获取帮助",
            "clear":"清除所有输出",
            "quit":"退出程序",
            "restart":"重启程序",
            "pwd":"查看当前工作目录",
            "openCurrentPwd":"打开当前工作目录",
        }

        self["relief"] = 'sunken'
        self["bd"] = 1

        self.outPutFrame = tk.Frame(_master,relief='sunken',bd=1)
        self.outPutFrame.place(relx=0,rely=0,relwidth=1,relheigh=.8)

        self.commandEntry = tk.Entry(_master)
        self.commandEntry.place(relx=0,rely=0.83,relwidth=0.78,relheigh=.17)
        self.commandEntry.bind("<Return>", self.__send)


        self.sendCommand = tk.Button(_master,text="Enter",command=self.__send)
        self.sendCommand.place(relx=0.8,rely=0.83,relwidth=0.2,relheigh=.17)

        self.output = scrolledtext.ScrolledText(self.outPutFrame,font=('Consolas', 9),state="disable")
        self.output.place(relwidth=1,relheight=1)


    def __send(self, *args):
        self.command = self.commandEntry.get()
        if not self.command:
            return
        if not self.waiting:
            if self.command[0] == "/" and self.command[1:].split(" ")[0] in self.commandsList:
                self.command = self.command[1:].split(" ")[0]
                self.commandsList[self.command]()

            elif self.command[0] == "/":
                self.command = self.command[1:]
                meantCommand = ""
                for i in self.commandsList:
                    for j in i:
                        if self.command[0] == j:
                            meantCommand = i
                            break
                self.insertMessage(message=f"'{self.command}' 不是一个可执行命令，您的意思是: /{meantCommand} ?")
            else:
                self.insertMessage(message=f"你是想输入 /{self.command} 吗? 用 /help 指令来查看所有命令")

            self.command = self.command[1:]

        if self.waiting:
            self.waiting = False
            return self.command

        try:
            self.commandEntry.delete(0,"end")
        except:
            pass

    def insertMessage(self,message):
        self.output["state"] = "normal"
        self.output.insert("end",">>>"+self.commandEntry.get()+"\n")
        self.output.insert("end",message+("\n" if message else ""))
        self.output["state"] = "disable"
        self.output.see("end")

    def justInsert(self,message):
        self.output["state"] = "normal"
        self.output.insert("end",">>>"+message+"\n")
        self.output["state"] = "disable"
        self.output.see("end")



    def __help(self):
        if len(self.commandEntry.get().split(" ")) == 1:
            self.insertMessage("指令列表:\n"+"\n".join([_ for _ in map(lambda x:"/"+x+" -> "+self.commandsHelpList[x],self.commandsList)]))
        elif len(self.commandEntry.get().split(" ")) == 2:
            self.insertMessage(self.commandsHelpList[self.commandEntry.get().split(" ")[1]])
        else:
            self.insertMessage("该指令语法错误，请重新输入或者输入/help 查询指令")

    def __clearPrompt(self):
        self.output["state"] = "normal"
        self.output.delete("1.0","end")
        self.output["state"] = "disable"



