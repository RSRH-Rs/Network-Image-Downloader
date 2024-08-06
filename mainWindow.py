import json
import tkinter as tk
from tkinter import filedialog
from Logg import Log
from terminal import *
from random import choice
from requests import get
from urllib.parse import quote
from json import loads
from useragents import rua
import asyncio
import aiohttp
from random import choice
from lxml import etree
import aiofile
from pathlib import Path
import os
from threading import Thread
import requests
import sys
from progressBa import StatusBar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Downloader:
    def __init__(self):
        self.createDefaultVars()
        self.createDefaultFiles()
        self.createWidgets()
        self.root.geometry("650x400")
        self.root.geometry(
            "%dx%d+%d+%d"
            % (self.width, self.height, self.displayX, self.displayY)
        )
        self.log.write(content="程序开始 :>")
        self.terminal.justInsert("python" + sys.version)
        self.root.protocol("WM_DELETE_WINDOW", self.saveExit)
        if not os.path.exists(self.saveDir):
            # os.mkdir(self.saveDir)
            pass

    def createWidgets(self):
        self.labelSaveDirVar = tk.StringVar()
        self.labelSaveDirVar.set(f"当前保存路径：{self.saveDir}")
        tk.Label(self.root, bd=1, textvariable=self.labelSaveDirVar).place(
            relx=0, rely=0, relwidth=1, relheigh=0.1
        )

        self.statusBar = StatusBar(self.root)
        self.statusBar.place(
            relx=0, rely=1, relwidth=1, relheight=0.05, anchor="sw"
        )
        self.statusBar.text(0, "状态栏")
        self.statusBar.text(1, "网络图片下载器 v1.0.0")
        self.statusBar.text(2, "作者:只会for循环的小白！")
        self.statusBar.text(
            3, "请勿用于商业用途，一切后果作者概不承担任何责任！"
        )
        self.statusBar.text(4, "❤")
        self.statusBar.text(5, "❤")

        self.downloadFrame = tk.Frame(self.root, bd=1, relief="sunken")
        self.downloadFrame.place(
            relx=0.02, rely=0.1, relwidth=0.5, relheigh=0.8
        )

        self.logFrame = tk.Frame(self.root, bd=1, relief="sunken")
        self.logFrame.place(relx=0.6, rely=0.1, relwidth=0.38, relheigh=0.8)
        self.log = Log(self.logFrame)

        self.L1 = tk.Label(
            self.logFrame, text="输出日记：", font=("Consolas", 10)
        )
        self.L1.place(relwidth=1, relheight=0.1)

        self.searchFrame = tk.Frame(self.downloadFrame, bd=1, relief="sunken")
        self.searchFrame.place(relx=0, rely=0, relwidth=1, relheigh=0.1)

        self.sourcedFrame = tk.Frame(self.searchFrame)
        self.sourcedFrame.place(relx=0, rely=0, relwidth=0.25, relheight=1)
        self.sourced = ttk.Combobox(
            self.sourcedFrame,
            state="readonly",
            values=["随机", "百度图片", "搜狗图片", "必应图片"],
        )
        self.sourced.place(relwidth=1, relheight=1)
        self.sourced.current(self.setSearchEngine)

        self.searchEntry = tk.Entry(
            self.searchFrame, font=("Consolas", 10), bd=1
        )
        self.searchEntry.place(relx=0.29, rely=0, relwidth=0.5, relheight=1)
        self.searchEntry.bind(
            "<Return>",
            lambda x: self.search(
                searchContent=self.searchEntry.get(),
                searchEngine=self.sourced.get(),
            ),
        )

        self.searchButtonFrame = tk.Frame(self.searchFrame, bd=1)
        self.searchButtonFrame.place(
            relx=0.8, rely=0, relwidth=0.2, relheight=1
        )

        self.searchButton = tk.Button(
            self.searchButtonFrame,
            text="搜索",
            bd=1,
            command=lambda: self.search(
                searchContent=self.searchEntry.get(),
                searchEngine=self.sourced.get(),
            ),
        )
        self.searchButton.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.configFrame = tk.Frame(self.downloadFrame, bd=1, relief="sunken")
        self.configFrame.place(relx=0, rely=0.1, relwidth=1, relheigh=0.4)

        tk.Label(self.configFrame, text="数量:", font=("Consolas", 10)).place(
            relx=0, rely=0.1
        )
        self.imageAmount = tk.Entry(self.configFrame, width=7)
        self.imageAmount.place(relx=0.12, rely=0.1)
        self.imageAmount.insert("end", self.setAmount)

        self.asyncDownloadButtonState = tk.IntVar()
        self.asyncDownloadButtonState.set(self.setAsyncDownload)
        self.asyncDownloadButton = tk.Checkbutton(
            self.configFrame,
            text="异步下载",
            onvalue=1,
            offvalue=0,
            variable=self.asyncDownloadButtonState,
            command=self.setVarFunc(self.asyncDownloadButtonState),
        )
        self.asyncDownloadButton.place(relx=0, rely=0.3)

        self.saveLogButtonState = tk.IntVar()
        self.saveLogButtonState.set(self.setSaveLog)
        self.saveLogButton = tk.Checkbutton(
            self.configFrame,
            text="保存日记",
            onvalue=1,
            offvalue=0,
            variable=self.saveLogButtonState,
            command=self.setVarFunc(self.saveLogButtonState),
        )
        self.saveLogButton.place(relx=0, rely=0.5)

        self.activeTerminalButtonState = tk.IntVar()
        self.activeTerminalButtonState.set(1)
        self.activeTerminalButton = tk.Checkbutton(
            self.configFrame,
            text="启用控制台",
            onvalue=1,
            offvalue=0,
            variable=self.activeTerminalButtonState,
            command=self.setVarFunc(self.activeTerminalButtonState),
        )
        self.activeTerminalButton.place(relx=0.3, rely=0.3)

        self.debugModeState = tk.IntVar()
        self.debugModeState.set(0)

        self.debugModeButton = tk.Checkbutton(
            self.configFrame,
            text="Debug模式",
            onvalue=1,
            offvalue=0,
            command=self.debugMode,
            variable=self.debugModeState,
        )
        self.debugModeButton.place(relx=0.3, rely=0.1)

        self.logAutoScrollDownState = tk.IntVar()
        self.logAutoScrollDownState.set(self.setLogAutoScrollDown)
        self.logAutoScrollDown = tk.Checkbutton(
            self.configFrame,
            text="日记自动滚动",
            onvalue=1,
            offvalue=0,
            variable=self.logAutoScrollDownState,
            command=self.setVarFunc(self.logAutoScrollDownState),
        )
        self.logAutoScrollDown.place(relx=0.3, rely=0.3)

        self.rememberChoicesButtonState = tk.IntVar()
        self.rememberChoicesButtonState.set(self.setRememberChoices)
        self.rememberChoicesButton = tk.Checkbutton(
            self.configFrame,
            text="记住选择",
            onvalue=1,
            offvalue=0,
            variable=self.rememberChoicesButtonState,
            command=self.setVarFunc(self.rememberChoicesButtonState),
        )
        self.rememberChoicesButton.place(relx=0.3, rely=0.5)

        tk.Button(
            self.configFrame, text="打开保存路径", command=self.openSaveDir
        ).place(relx=0, rely=1, relwidth=0.3, relheigh=0.25, anchor="sw")

        tk.Button(
            self.configFrame, text="设置保存路径", command=self.chooseSaveDir
        ).place(relx=0.3, rely=1, relwidth=0.3, relheigh=0.25, anchor="sw")

        tk.Button(
            self.configFrame,
            text="重新启动",
            command=lambda: (self.root.destroy(), system(__file__)),
        ).place(relx=0.6, rely=1, relwidth=0.2, relheigh=0.25, anchor="sw")

        tk.Button(self.configFrame, text="退出", command=exit).place(
            relx=0.8, rely=1, relwidth=0.2, relheigh=0.25, anchor="sw"
        )

        tk.Button(
            self.configFrame, text="终止下载", command=self.setStopDownload
        ).place(relx=1, rely=0, relwidth=0.2, relheigh=0.25, anchor="ne")
        tk.Button(self.configFrame, text="联系作者", command=exit).place(
            relx=1, rely=0.25, relwidth=0.2, relheigh=0.25, anchor="ne"
        )
        tk.Button(self.configFrame, text="恢复默认", command=exit).place(
            relx=1, rely=0.5, relwidth=0.2, relheigh=0.25, anchor="ne"
        )

        self.terminalFrame = tk.Frame(self.downloadFrame)
        self.terminalFrame.place(relx=0, rely=0.5, relwidth=1, relheigh=0.5)

        self.terminal = Terminal(self.terminalFrame)

    def saveExit(self):
        if self.rememberChoicesButtonState.get() == 0:
            self.root.destroy()
            file = open(self.path + "\\settings.json", mode="w")
            file.write(json.dumps(self.defaultJsonFile))
            file.close()
            return

        saveData = {
            "amount": self.imageAmount.get(),
            "searchEngine": list(self.sourced["values"]).index(
                self.sourced.get()
            ),
            "asyncDownload": self.asyncDownloadButtonState.get(),
            "saveLog": self.saveLogButtonState.get(),
            "logAutoScrollDown": self.logAutoScrollDownState.get(),
            "saveDir": self.saveDir,
            "rememberChoices": self.rememberChoicesButtonState.get(),
        }
        with open(self.path + "\\settings.json", mode="w") as f:
            f.write(json.dumps(saveData))
        self.root.destroy()
        f.close()

        # if self.saveLogButtonState.get():
        #     if not os.path.exists(self.path+"\Log"):
        #         os.mkdir(self.path+"\Log")
        #     currentTime = datetime.now().strftime('%Y-%m-%d-%H-%M:%S')
        #     with open(self.path+f"\Log\\{currentTime}.log",mode="w") as a:
        #         a.write(str(self.log.getText()))

    def setVarFunc(self, var):
        var.set(1 if var.get() else 0)

    def setStopDownload(self):
        self.stopDownload = True
        self.log.write("所有任务已停止！", warn=True)
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )

    def createDefaultVars(self):
        self.root = tk.Tk()
        self.height = 400
        self.width = 650
        self.displayX, self.displayY = self.centerDisplay(
            self.root, self.width, self.height
        )
        self.onCrawling = False
        self.totalUrls = []
        self.illegal_symbol = '|?/\\:"<>,!！“《》'
        self.path = str(Path(__file__).resolve().parent)

        self.folderName = "\Images"
        self.saveDir = self.path + self.folderName

        self.searchEngines = {
            "百度图片": self.Baidu_image_crawler,
            "搜狗图片": self.Sougou_image_crawler,
            "必应图片": self.Bing_image_crawler,
        }
        self.defaultJsonFile = {
            "amount": 0,
            "searchEngine": 0,
            "asyncDownload": True,
            "saveLog": False,
            "logAutoScrollDown": True,
            "saveDir": self.saveDir,
            "rememberChoices": False,
        }
        self.stopDownload = False

    def createDefaultFiles(self):
        if not os.path.exists(self.path + "\\settings.json"):
            file = open(self.path + "\\settings.json", mode="w")
            file.write(json.dumps(self.defaultJsonFile))
            file.close()
        try:
            file = open(self.path + "\\settings.json", mode="r").read()
            data = json.loads(file)
            self.setAmount = data["amount"] if data["amount"] else 0
            self.setSearchEngine = (
                data["searchEngine"] if data["searchEngine"] else 0
            )
            self.setAsyncDownload = data["asyncDownload"]
            self.setSaveLog = data["saveLog"]
            self.setLogAutoScrollDown = data["logAutoScrollDown"]
            self.saveDir = data["saveDir"]
            self.setRememberChoices = data["rememberChoices"]
        except:
            try:
                os.remove(self.path + "\\settings.json")
                self.createDefaultFiles()
            except:
                pass

    def debugMode(self):
        self.debugModeState.set(1 if self.debugModeState.get() else 0)
        self.log.logText["state"] = (
            "normal" if self.debugModeState.get() else "disable"
        )
        self.terminal.output["state"] = (
            "normal" if self.debugModeState.get() else "disable"
        )

    def search(self, searchContent, searchEngine):
        if not searchContent or self.onCrawling:
            self.log.write(
                "输入的内容不能为空！"
                if not searchContent
                else "正在搜索中，请勿频繁搜索。"
            )
            (
                self.log.logText.see("end")
                if self.logAutoScrollDownState.get()
                else None
            )
            return

        random = choice(self.sourced["values"])
        self.searchEngine = (
            searchEngine
            if searchEngine != "随机"
            else random if random != "随机" else self.sourced["values"][1]
        )
        self.searchContent = searchContent

        self.totalImageAmount = 0
        try:
            if not int(self.imageAmount.get()) > 0:
                self.log.write("请输入数字！范围1~500！")
                (
                    self.log.logText.see("end")
                    if self.logAutoScrollDownState.get()
                    else None
                )
                return
            self.totalImageAmount = (
                int(self.imageAmount.get())
                if int(self.imageAmount.get()) <= 500
                else 500
            )

        except:
            self.log.write("请输入数字！范围1~500！")
            (
                self.log.logText.see("end")
                if self.logAutoScrollDownState.get()
                else None
            )
            return

        self.onCrawling = True
        self.log.write(
            f"使用了搜索引擎[{self.searchEngine}]，搜索了[{self.searchContent}]。数量为:{self.totalImageAmount}"
        )
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )
        try:
            Thread(
                target=self.searchEngines[self.searchEngine],
                args=(self.searchContent, self.totalImageAmount),
            ).start()
        except Exception as e:
            self.log.write(e, warn=True)

    def Baidu_image_crawler(self, keyword, amount, **kwargs):
        self.log.write("正在获取Url", warn=True)
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )
        self.Baidu_baseUrl = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8568459494179828495&ipn=rj&ct=201326592&is=&fp=result&fr=&word={quote(keyword)}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn=0&rn={amount}&gsm=96&1639707796619="
        try:
            response = get(
                url=self.Baidu_baseUrl, headers={"user-agent": rua()}
            )
        except Exception as e:
            self.log.write(str(e), warn=True)
            self.onCrawling = False
            self.stopDownload = False
            return
        response.encoding = response.apparent_encoding
        json_data = loads(response.text)
        for data in json_data["data"]:
            try:
                self.totalUrls.append(
                    [data["thumbURL"], data["fromPageTitleEnc"]]
                )
            except:
                self.log.write(
                    f"Url获取完毕，总共{len(self.totalUrls)}条Url", warn=True
                )
                (
                    self.log.logText.see("end")
                    if self.logAutoScrollDownState.get()
                    else None
                )
                break

        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.startAllTasks(urls=self.totalUrls))
        self.totalUrls.clear()

    def Bing_image_crawler(self, keyword, amount, **kwargs):
        headers = {
            "user-agent": rua(),
            "referer": "https://www.bing.com/images/search?q=%e7%8b%97&form=QBIR&first=1&tsc=ImageHoverTitle",
            "cookie": "MMCA=ID=4C0EEE89857B4C31BF0490193AB18B7C; _IDET=MIExp=0&VSNoti2=20211015&HSNoti2=20220307; MUID=0A9B5E5D5CD76D9205F04E2A5D7D6CAD; MUIDB=0A9B5E5D5CD76D9205F04E2A5D7D6CAD; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=C5CA1BC55CFA4C7BA5BFD2D2C782D827&dmnchg=1; MSCCSC=1; PPLState=1; _UR=QS=1; _EDGE_CD=u=en-us; BFBUSR=BAWAS=1&BAWFS=1; ANON=A=276256C33217709D631122F2FFFFFFFF&E=1a50&W=1; NAP=V=1.9&E=19f6&C=biSlEktadZrkVXaZq8YQWkPIlZ7lSS-W5Ed-ziUGWMIoA9EtoJIISQ&W=1; KievRPSSecAuth=FABqBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACEeB2sF0bWDhKASPaDLAJ2OuPON5nlyxivi0RQavlJg8dG/Wgdejhv720pltYqg0AZpcI8Bad7iu8V4J2yTOhSHOu00ln4eSmziHVDJJGUePwTvL4n3B1BNqsGNAw3zPlPxTkqdEskbW7IAFj81LJJ9kEa7rWInHuMtDhNcdapCitJwln2ewEuI65ddVo/BsovyMRl5YVYWkWsKq4dYdi1cSIcTWQmk8InWKffaFzQR+CjbdkLV1uIN7DSd+ICiZvDQP2prxQy0FmsUZ+FJqGRv+jTJdsi/R5OGf2B4ycImHTY8PiE+bmkSou2IbJJPfpMKihBYSl1KDga56Iso12kHjIhIibguzI/p8KjfTnH2XtLSQpnm+GGSbJXQQxZ7ZBNsNwWqfFCFUF0PaWrWnxj8KD8RKsX78R1XuXSWYxRUYNFhOPeJrCupd0TdsmerTDrUDANkkMOUzS7OEAJnb5cwu4qpEjcz0ofjO3lFH3EZ0fh8K1lWaSdZo49SFCgqlUledQbEcbgVozd90yatHLPLGd8w9KYXriEqWlkwXhxdXBLP0lQzsVkvjaas3ru+7JEpffBtbrz1yUBmaJN5UipeYhhnaZUt5aXk6Lz1l0JBb0lNChvgOiM/9hYBJCXbuIwhH28GORx0CQLG8rdiwJz4JZMTgV7Z0+HkjnD5KgHhGylDmivSp+M0QEOdfs57Hr6AoZ2k95YWJYdOeTIir9dijK04ot+p0foiqhoeKqwtqnKffNwh97XBJC9rJbOR+cggeTWWKB3Mvr3KVGi5YDB0QfAc5NWGbOIdc218VsKDUY7Gxgj3G8hPjYemZdpgZ9DhUiyGVYO8mhW8mn7Llcf1SJzy7gkWRWN8lt27d55JtkrTUEiw1OyVmzH4WXgopA3FgexbwhBr/gqIGpKnwt41c4HXSHKXkaaY7Xm/a44pe6C5VmT1471/Z6KabWgWIfryNPsE/wih9XbQSm0pAUx3xw4/wrk93+ZPK9cghwpGNoup8eW0hJzodW0BLB4Ounzu3ZWY4ayEbp0gmH4OMRiVCJvYLotZ2RnnkL5ZlVjSsVjqo3rfiTdeg2nEQxLAUrZ/0Q5fJzQPjfHwjjn+iK3Tk6Fh+Tm4uLcwZV+ePCWqHKj+NYrAejefOmRQqiT7kXHj6eFngd/z2Ali0w0q4ruMY7PSjUaQVsn+T6g21e44mRMAJXSwUoDwF0lORMFR5xnCbqr9eq2//Y5bwg8aynW9pNq2x5yiOgUf8quLRAUbapc0GzFWv2TNTxrc0Gq+OrNelcuixMjecQvrHBznPPzmBnTt8B1yxQp9/p96VJmX4MFVcP4rKjaj7CRDvlfcpMJpR39R/FbKGsQy4LortPNOonRvhsgDth7m91hxmRhKNGRbjWaobo2cvYVjP9URf7rPIqh5/3Q1Le2zNqXrjww0HMBQAg5l3uLoMV8+akbWCwEDN4tIn5Lg=; TTRSL=zh-Hans; _TTSS_IN=hist=WyJ6aC1IYW5zIiwiZW4iLCJhdXRvLWRldGVjdCJd; _TTSS_OUT=hist=WyJhZiIsImVuIiwiemgtSGFucyJd; _tarLang=default=zh-Hans; ABDEF=V=13&ABDV=11&MRNB=1646172989836&MRB=0; SUID=A; SRCHS=PC=U316; BFB=AhDDqXRa0dyygy7jnkS63dB-UN_5dJwK2wlnTcneFA50cXsIfVSbKVchRsitYEvhnCEmsN5dKNvbNxR3pFW7MkUf8NVJdU4YplsJEnwnTwwgUMmInrpPWSftMBitqZZVn87Wimav-gbCtUg32rty7BT2v93PD6ZG4Tghj6MVoS3A4A; _SS=SID=38CC984CD89068B72C86892DD93A695C&PC=U316&R=200&RB=0&GB=0&RG=200&RP=200; ipv6=hit=1646709098092&t=4; SRCHUSR=DOB=20210717&T=1632621929000&TPC=1646705615000; OID=AhDy1fXSq1uMSO1ReJL5ctM0RJMww2b3BLTjrwkZhLh9gvCTtGLWP0GItrTVNJ5ge874kuqyOA7YzKziedP70sdgNI6oqYONtLrEgknqEexfRupqT0wBtxZJHDLu624X-V7eOh-2i160RYd35VoY-cFH; OIDR=ghCK-v-BIH-nyPMkrkLEQdny_AwXhcSDyZUOK3uQ2bUgN-jDqfoEP7zFtAgRvp5T9DrGNqZ2QVj5xgWst2JXu44ILShksICSAEy_161FE_sqIrviGi_1PdjanWIgir09DWPdwbiC4g4HtzttJekfgJ7uAhbhkcQdF9QHMDV2SfIYiC5lv7iW13L9LFaSBEhrK4rgjcvbovFOy-ShbSBmLJnqBdhQhaDt_Z6vUlfgOgi3p9FdECpTBysNXjpYhuqjOdFqFuwJvIZu29eHlayFfCmfQOgLiFtDXsi6obxNgqdxdzZxJk8lhjUdC-HKQqcnGaFRmPxq9Ow9S9PduTYtMcXJw9xrPltn3Pb9g0k3eC5sqd3bm_Ogzl1fyWtrzReUHuU_z251QhGKhDI9GU6AMBMROHT8nOPjmlBs3o7YXNwZ_ep1JB-DUUy40wjw2IlZ4HNOPHR_EjpBa6hAVbuRWl3cEbAroTUZgvSgV2OdkP3r1bjsdwld9KleTMcAUI4ZnUFHunqn1M6TQAsOj2tEvZ4I0DReZVU9mopWDYkyggHl-zjBREJl1-piocLLeUzktjge7k7sC83ek6HCOQYQKuriXJtD7hEdMv0xWpib5i2jCrTd1WL24dRvZ8D61JCky6irUu2jmRoG3sRBldPpmkb6IE7SaOraaeBd7RMvLFWBCWhiswLmRAP8xBZQiEGJ_bLj_F18N-Gq4OIUQv6poyQWTlXw02QLsIQyvZPmtmvijlkEchtWt935NhB3ZIvkjVOxWEN8GUSnWeJoXvRTNPdTbCGO2X4jeooivMT92YkNiItHgfETGVaqvPPUeiCwdD-A5bz0vz_MMTqLeOiN8ATFJ4WG4HZGafVCbKvjyEal054LmT4-ICac6Yg91rthQmGm_RKGqJqdKsHU5yGBQ-MxS8VVtzAejCvGtgvhvfSBpe1v0W2uRAXongvpA9TkuK96Z3EbaL-jR-_oTG0ZgosRGWjH2pHULzt6bsMGzj1Y_tpRbZTL4Q-IdEqxLTjLbTphPqdYJtApsdmHKKrolM8mWJ8Ezr_0frV9UG5grlPFi6aPYXISc51aBUsTwn7C1YkkB-NlVdXhGE51DzR6krhGq5RiNxZjMgpPW7HZRYoYK2CwpGJD4Vn5xo6La-wrLvaVWa56x-y8aB1NCZ5Fqb57lAAxAvVF65TFwyMgSOKrIrQ9gXwbjzPenyAktHxMWHe3Z8D44TUuu3zEh2p0vBsn; OIDI=ghCgH48CNZMkNaRMSAUkcM2XLsAS4EGzx5WBV5qpIS6gBLOvkmqq1wd7I4EnC6U-j3GGOpgiqUKiveFFIB1P9_Xq0M59gaKCk26TTFQSFkJvp0C6LUAprrJ-ljLRPpsn9SxQM3FOl0C_BWC-pLQGmvwlZq6QC0Y5TueugpzhK7--pqO2tq-ZQFiDi7cC7YSo3c55rBpEwQM7qNJTKg1KmjQkCdPDWF-toHAWErJibAwNtC0JF1yxVJZ8cKceETa0T1x_ZpqE3RmUEvid_mWcoR7st9fie5gIZhHEvfmCJ-MfmsLExR0BEHjyZ9ziE-E0Xu-GefA_IqolIPsgPxvi6h6IdS-9QmxjyZVBwiKpjn9rjv-hi5MVley5YvHzzR981IZQbX-p7t3CrCPmqiYkhVPDnEnCMy7z4QNIHOuC9_mTWd57L67YHQ9kKc14se4PV7U8nB2Lqz1E_6Pv2xpG5iXSlnbhdWeHbnW2VWuLSDPoectdYch8bLAwxjE5i78yO1Mu8ly_YGuJFpiDeLLIga8pn-p_kUVvKR9GKZ5XxpW317UA7LMioF8MPHcHNJm20vv-AKbrxifarc56X4ZKdxXsZHLlE4L9z3eVZ5RA_O08RfDL6xhz32iPMUHF-uY0fzc898LBUZuuCYZQK1AhYy__t11tAut2Tb-EqJmDEho0-lTHvQHk6h0P9SHcvEIYlz_FR_OzLETBPVqcnVes1Wnxm-Os4Hrf7_jiKOEMF2C8nens1d6FxfFY0s-6fQhbS7OL2VsJoiRT6vjrFI-FVOykUd6pKhUngOCDh1PMAEq2rb8Eb-HqM-AjKZgGj5438ti_T9NVuF8Nv0RrCuwP8YgfHGuYwZGCNUEY1O3Ry7kdhzBrmYiAwDThuwfMSBRfXF6KsfOcS3oo-6smHkgfmwb43p01l_WFf3oUQ168agpBm6wyXXmdedlyYPzeEVvtzzuC0chhMqkq4mCqYvsNZ1uuveNae7xpnj6q7BCdTqbnzp-WlzDc16qX1KdsqMxbCSG6seViN7zahgvWlYeiqLsf8-oHDvGqS03gsvQcoEPPVvw5Shxxc3epiDGvKx-6UvUtfLowSHtBPhKrA69MdnuCSTISPlzkVdXe71znjdmlNrmYPRdrweGvUoBVGG1l_HkM3QPmyuVC4cjujakWfjo1m-WBIR9P2mXtztyBofBLioa4SDwJUDBupV34YxDs2V105ATCe4UBYQ2C5-jyb7sGaIPDSJU9gmgRXJptJKVyaXP2TDMHMJy6CjP_c9z_paVB87HoCc7KHYk3jvCOmTfkAXV42xuk2vvjd6vtZhUui7wkx2Q9eBDvgtyKD6V1W7-LZfn5q0ygwID4omF_iOnY3aXYoP5V-MIV2SKIM85143M8ZapFB7TqyQ57yKdbro1RCad5UDVCQHtjHOLJ2QPJoGQzNyVosV1wEKp32q-GJAewXFlVJcsHXVqx_255SCPfmv3T-r1IB-hssyiS0YqZQZTj8XZfzFXWhYF9WxlYUcTS-appLt4UsDuY8Zm7dIqLuLJPfpwJ785thKnacD0he51Sa8mMxc3CYBZb8e5dOlrOBTXQ2l24ERGAxyyLj0pkyg4C9nXOoVSkhTy5N2tJ-hb2483LIpFLpZ159DoXsagnEbkenoB7VHSy2uEoRgdYRLHfI7kt2qJ_9UEyWmaAdNUshdwa0AYpWnTdfdH7Eb3lBdDD33555f2JPJv_q6QPCkivfQZPAZhgNb5WjtpfFMEYq0HbV3fbCvtDqQiIZsvEJNQPscmG4txPwFNuTIyYtFW2zPz7YPdv1X6WEzAtCqZpcYqKaNR2md4Otpz3kXH_80U_dt-DIcHJu7cgMW9e8L_7FmdkSoUruCJotgUogn82cbSCne0uQBYvd_lp08vb1t1VZHd_PnDk0gNY-nyxy8Z5h6yq233NqvwKUwL2; _ITAB=STAB=TR; imgv=flts=20220308; _HPVN=CS=eyJQbiI6eyJDbiI6MCwiU3QiOjIsIlFzIjoxLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MTc2LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjoxNzcsIlN0IjoxLCJRcyI6MCwiUHJvZCI6IlQifSwiQXAiOnRydWUsIk11dGUiOnRydWUsIkxhZCI6IjIwMjItMDMtMDhUMDA6MDA6MDBaIiwiSW90ZCI6MCwiR3diIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjEzMzV9; _EDGE_S=SID=38CC984CD89068B72C86892DD93A695C&mkt=en-ca&ui=en-us; _RwBf=mtu=0&g=0&cid=&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2022-03-08T02:18:56.2698708+00:00&rwred=0&ilt=1667&ihpd=0&ispd=3&v=9&l=2022-03-07T08:00:00.0000000Z&lrat=0001-01-01T00:00:00.0000000&lft=20211117&aof=0&rc=200&rb=0&gb=0&rg=200&pc=200&rbb=0&clo=0; SRCHHPGUSR=SRCHLANG=en&BRW=XW&BRH=S&CW=1536&CH=244&SW=1536&SH=864&DPR=1.25&UTC=-300&DM=0&WTS=63768218733&HV=1646705936&NEWWND=0&NRSLT=-1&LSL=0&AS=1&ADLT=DEMOTE&NNT=1&HAP=0&VSRO=1&ULOC=LAT=43.79174041748047|LON=-79.24651336669922|N=Scarborough, M1S 4R9, Canada|C=|S=|TS=210717200538|LT=|ETS=|&VCW=1519&VCH=722",
        }

        self.log.write("正在获取Url", warn=True)
        self.BingBaseUrl = f"https://www.bing.com/images/async?q={quote(keyword)}&first=0&count={amount}&cw=1536&ch=218&relp=35&tsc=ImageHoverTitle&datsrc=I&layout=RowBased&mmasync=1"
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )
        response = get(url=self.BingBaseUrl, headers=headers)
        response.encoding = response.apparent_encoding
        selector = etree.HTML(response.text)
        childrenElements = selector.xpath(
            '//div[@id="mmComponent_images_2"]//ul'
        )

    def Sougou_image_crawler(self, keyword, amount, **kwargs):
        self.log.write("正在获取Url", warn=True)
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )
        self.amount = 0
        self.amount += int(amount / 48) + 1 if amount % 48 > 0 else amount / 48

        for index in range(self.amount + 1):
            self.SougouBaseUrl = f"https://pic.sogou.com/napi/pc/searchList?mode=1&start={index*48}&xml_len=48&query={quote(keyword)}"
            try:
                response = requests.get(
                    url=self.SougouBaseUrl, headers={"user-agent": rua()}
                )
            except Exception as e:
                self.log.write(str(e), warn=True)
                self.onCrawling = False
                self.stopDownload = False
                return
            response.encoding = response.apparent_encoding
            json_data = loads(response.text)
            for data in json_data["data"]["items"]:
                self.totalUrls.append([data["locImageLink"], data["title"]])
        self.totalUrls = self.totalUrls[:amount]
        self.log.write(
            f"Url获取完毕，总共{len(self.totalUrls)}条Url", warn=True
        )
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.startAllTasks(urls=self.totalUrls))
        self.totalUrls.clear()

    async def startAllTasks(self, urls):
        if not os.path.exists(f"{self.path}\\{self.folderName}"):
            os.mkdir(f"{self.path}\\{self.folderName}")
        self.img_tasks = [
            self.async_download_images(value[0], value[1], index)
            for index, value in enumerate(urls)
        ]
        await asyncio.wait(self.img_tasks)
        (
            self.log.write("全部图片下载完成", warn=True)
            if not self.stopDownload
            else None
        )
        (
            self.log.logText.see("end")
            if self.logAutoScrollDownState.get()
            else None
        )
        self.onCrawling = False
        self.stopDownload = False

    async def async_download_images(self, image_url, image_name, index):
        if not os.path.exists(
            f"{self.path}\\{self.folderName}\\{self.searchContent}"
        ):
            os.mkdir(f"{self.path}\\{self.folderName}\\{self.searchContent}")
        for symbol in self.illegal_symbol:
            if symbol in image_name:
                image_name = str(image_name.replace(symbol, "_"))
        image_name = image_name.split("_")[0]
        async with aiohttp.ClientSession() as session:
            if self.stopDownload:
                return
            self.log.write(f"正在请求{image_name}！")
            (
                self.log.logText.see("end")
                if self.logAutoScrollDownState.get()
                else None
            )
            async with session.get(
                image_url, headers={"user-agent": rua()}
            ) as response:
                data = await response.read()
                async with aiofile.async_open(
                    f"{self.path}\\{self.folderName}\\{self.searchContent}\\{index}{image_name}.png",
                    mode="wb",
                ) as save:
                    await save.write(data)
                    if self.stopDownload:
                        return
                    self.log.write(f"{image_name}保存成功！")
                    (
                        self.log.logText.see("end")
                        if self.logAutoScrollDownState.get()
                        else None
                    )

    def chooseSaveDir(self):
        self.setPath = filedialog.askdirectory()
        self.saveDir = self.setPath
        self.labelSaveDirVar.set(f"当前保存路径：{self.saveDir}")

    def openSaveDir(self):
        Thread(target=lambda: system("start " + self.saveDir)).start()

    def run(self):
        return self.root.mainloop()

    @staticmethod
    def centerDisplay(widget, width, height):
        windowWidth = widget.winfo_screenwidth()
        windowHeight = widget.winfo_screenheight()
        x, y = (windowWidth / 2) - (width / 2), (windowHeight / 2) - (
            height / 2
        )
        return x, y


if __name__ == "__main__":
    app = Downloader()
    app.run()
