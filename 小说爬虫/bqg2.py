import requests,os,threading,time
from lxml import html
from tkinter import *
from tkinter.filedialog import askdirectory

#pyinstaller --clean --win-private-assemblies -Fw -i shu.ico bqg2.py

def gui():
    haders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    def get_html(): #搜索结果页
        global xsURL
        url = 'http://www.biquw.com/modules/article/search.php?action=login&searchkey='
        names = name.get()
        if names=='':
            tishiE.set('无内容')
            return
        url = url + names
        response = requests.get(url, headers=haders)
        response.encoding = 'utf-8'
        respons = html.fromstring(response.text)
        xsURL = respons.xpath('//*[@id="content"]/div[2]/ul/li[*]/p[1]/a/@href')
        xsname = respons.xpath('//*[@id="content"]/div[2]/ul/li[*]/p[1]/a/text()')
        if xsURL==[]:
            nameE_no.set('无此书名')
            return
        nameE_no.set(xsname)

    def get_html2(xsname,xsurl,times): #下载小说
        try:
            xpth = paths.get()
            response = requests.get(xsurl, headers=haders)
            response.encoding = 'utf-8'
            respons = html.fromstring(response.text)
            xsURL = respons.xpath('//*[@id="info"]/div[1]/a[1]/@href')
            if not os.path.exists(str(xpth)):
                os.mkdir(str(xpth))
            time.sleep(int(timeouts.get())*times)
            f=requests.get(xsURL[0],headers=haders)
            with open(xpth+'./'+xsname+'.txt',"wb") as code:
                code.write(f.content)
                tishi.insert(END,[xsname+'完成'])
        except Exception as e:
            tishi.insert(END,['下载出错',e])

    def move(*args):
        try:
            global xsURL,num_id
            xnum = li1.curselection()[0]
            num_id.append(xnum)
            li2.insert(END,nameE_no.get().split(',')[xnum][2:-1])
        except Exception:
            pass

    def delet(*args):
        try:
            global num_id
            num_id.pop(li2.curselection()[0])
            li2.delete(first=li2.curselection(),last=None)
        except Exception:
            pass
    
    def down():
        global xsURL,num_id
        try:
            th_li = []
            cuu = 0
            for i in num_id:
                cuu += 1
                th = threading.Thread(target=get_html2,args=(nameE_no.get().split(',')[i][2:-1],xsURL[i],cuu))
                th.setDaemon(True)
                th.start()
                th_li.append(th)
            tishiE.set('请稍等。。。')
        except Exception as e:
            tishiE.set(['无内容',e])

    def openPath():
        xpth = paths.get()
        if not os.path.exists(str(xpth)):
                os.mkdir(str(xpth))
        dir = os.path.dirname(paths.get()+"\\")
        os.system('start ' + dir)

    def selectPath():
        path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
        if path_ == "":
            paths.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
        else:
            path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
            paths.set(path_)

    root = Tk()
    root.title("novel")
    root.geometry("540x305+600+200")
    root.resizable(False,False)
    root.protocol("WM_DELETE_WINDOW",root.quit())


    
    #容器组
    name = StringVar()
    paths = StringVar()
    paths.set("D:\\novel")
    nameE_no = StringVar()
    nameE_ok = StringVar()
    tishiE = StringVar()
    global num_id
    num_id = []
    shuoming = ['双击名称添加、删除','下载小说1kb时,','单个下,或者','将time值设置大一点,有问题qq','2511750237']
    
    #listbox组
    li1 = Listbox(root,width=25,height=8,listvariable=nameE_no)
    li1.grid(row=4,column=0)
    
    li2 = Listbox(root,width=25,height=8,listvariable=nameE_ok)
    li2.grid(row=4,column=1)

    tishi = Listbox(root,width=25,height=8,listvariable=tishiE)
    tishi.grid(row=4,column=2)

    timeouts = StringVar()
    timeouts.set(5)
    
    #绑定组

    li1.bind('<Double-Button-1>',move)
    li2.bind('<Double-Button-1>',delet)

    #标签组
    Label(text='书   名:').grid(row=0,column=0)
    Label(text='路   径:').grid(row=1,column=0)
    Label(text='查询结果:').grid(row=3,column=0)
    Label(text='下载选择:').grid(row=3,column=1)
    Label(text='提示:').grid(row=3,column=2)
    Label(root,text='小说来源笔趣阁').grid(row=5,column=0,columnspan=3)
    Label(root,text='👇time👇').grid(row=0,column=2,sticky=W)

    #文本框组
    nameE = Entry(textvariable=name)
    nameE.grid(row=0,column=0,columnspan=2)
    pathE = Entry(textvariable=paths)
    pathE.grid(row=1,column=0,columnspan=2)
    timeoutsE = Entry(textvariable=timeouts,width=5)
    timeoutsE.grid(row=1,column=2,sticky=W)

    #按钮组
    Button(root,text='查询',width=9,command=lambda:get_html()).grid(row=0,column=1,sticky=E)
    Button(root,text='下载',width=9,bg='MediumSpringGreen',command=lambda:down()).grid(row=0,column=2)
    Button(root,text='保存路径',width=9,command=lambda:selectPath()).grid(row=1,column=1,sticky=E)
    Button(root,text='已下载小说',width=9,command=lambda:openPath()).grid(row=1,column=2)
    Button(root,text='说明',command=lambda:tishiE.set(shuoming)).grid(row=5,column=2)
    



    root.mainloop()
gui()