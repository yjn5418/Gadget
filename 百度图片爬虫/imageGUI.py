import queue
import urllib3
import string
import requests,os,re,time
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from urllib.parse import quote 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getPath():
    def FUN(name,page,img_name,xpaths):
        xpaths = xpaths+'\\'
        page = int(page)
        headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39'
        }
        if not os.path.exists(xpaths + img_name):
            os.makedirs(xpaths +img_name)
        cut = 1
        for i in range(page):
            url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + name + '&pn=' + str(i*20)
            post = requests.get(url=url,headers=headers,verify=False)
            html = post.content.decode()
            results = re.findall('"hoverURL":"(.*?)",',html)
            for i in results:
                li.insert(END,str(cut)+' ...OK!!!')
                li.see(END)
                root.update()
                cut += 1
                try:
                    pic = requests.get(i,timeout=10)
                except:

                    li.insert(END,'...Error!!!')
                    continue
                file_full_name = xpaths + img_name + '/' + str(time.time()) + '.jpg'
                with open(file_full_name,'wb') as f:
                    f.write(pic.content)
            li.insert(END,'共计下载 %d 张图片' %(page*60))
            li.see(END)
        return '共计下载 %d 张图片' %(page*60)

    def selectPath():

        path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
        if path_ == "":
            path.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
        else:
            path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
            path.set(path_)

    def openPath():
        dir = os.path.dirname(path.get()+"\\")
        os.system('start ' + dir)

    def xun():
        try:
            name1 = name.get()
            page1 = page.get()
            img_name = name1
            xpaths = path.get()
            name1 = quote(name1, safe = string.printable)
        except:
            showinfo(title='提示', message='请输入完整信息')
        FUN(name1,page1,img_name,xpaths)

    # 创建主窗口
    root = Tk()
    root.geometry('750x500')
    root.resizable(False,False)
    root.title("图片爪巴虫")
    # photo = PhotoImage(file ="D:\\downOK\\code new\\练习\\GUI\\back.gif")

    root.configure(background='gray')
    root.attributes("-alpha", 0.85)


    path = StringVar()
    path.set(os.path.abspath("."))
    tishi= StringVar()

    #Label(root,image=photo,bg='gray').place(x=0,y=0,relwidth=1,relheight=1)
    Label(root,text="此爬虫检索引擎为http://image.baidu.com/").grid(row=0, column=0,columnspan=2)
    Label(root, text="目标路径:",bg='red').grid(row=1, column=0,sticky=E)  
    pathx = Entry(root, textvariable=path,state="readonly")
    pathx.grid(row=1, column=1,ipadx=150)
    Button(root, text="路径选择", command=selectPath).grid(row=1, column=2)
    Button(root, text="打开文件位置", command=openPath).grid(row=1, column=3)
    Label(root, text="搜索关键字:").grid(row=2, column=0,sticky=E)
    name = Entry(root,fg='red')
    name.grid(row=2, column=1,ipadx=100,sticky='w')
    Label(root, text="页数(1页=60张):").grid(row=3, column=0)
    page=Entry(root)
    page.grid(row=3,column=1,sticky='w')
    Label(root, text="提示:下载尽量不要超过5000张,否则可能会被封IP  ").grid(row=3, column=1,sticky=E)
    go = Button(root, text="爬取开始",height=2,bg='white',bd='1',command= lambda: xun())
    go.grid(row=2, column=2,rowspan=2,columnspan=2,ipadx=50)
    Label(root, text="提示:").grid(row=4, column=0)
    li = Listbox(root, listvariable = tishi,height = 15,width=100)
    li.grid(row=5,column=0,columnspan=4) 
    root.mainloop()# 在这里添加主循环

if __name__ == "__main__":

    getPath()