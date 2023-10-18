import os,threading,socket as sk
from tkinter import *
from http.server import SimpleHTTPRequestHandler, HTTPServer                                                                                                                       

#pyinstaller --clean --win-private-assemblies -Fw -i ftp.ico local_server.py


def open_http():
    try:
        global httpd
        if not os.path.exists(str(paths.get())):
            os.mkdir(str(paths.get()))
        os.chdir(str(paths.get()))                                                                                                                                                                                      
        server_address = ('', int(port.get()))                                                                                                                                                                   
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)                                                                                                                                   
        httpd.serve_forever()
    except Exception as e:
        tishi.set('open错误')
    


def close_http():
    try:
        global httpd
        httpd.shutdown()
    except Exception as e:
        tishi.set('close_http')
    
def th_http(zl):
    try:
        if zl == 1:
            threading.Thread(target=open_http).start()
            # local_ip = sk.gethostbyname(sk.gethostname())
            local_ip = '192.168.1.145'
            tishi.set('已开启服务站：\n'+local_ip+':'+str(port.get()))
        else:
            threading.Thread(target=close_http).start()
            tishi.set('已关闭服务站')
    except Exception:
        pass



root = Tk()
root.title("Share")
root.geometry("429x230+600+200")
root.resizable(False,False)
root.protocol("WM_DELETE_WINDOW",root.quit() and os._exit(0))


port = StringVar()
port.set(8080)
paths = StringVar()
paths.set("D:\server_web")
tishi = StringVar()

Label(root,text='',width=2).grid(row=1,column=0)
Label(root,text='',width=1).grid(row=1,column=3)


Label(root,text='共享路径： ').grid(row=1,column=1)
Entry(root,width=5,textvariable=port).grid(row=1,column=2)
Entry(root,width=25,textvariable=paths).grid(row=1,column=3)

Button(root,text='开启共享',command=lambda:th_http(1)).grid(row=1,column=5)
Button(root,text='关闭共享',command=lambda:th_http(0)).grid(row=1,column=6)

Listbox(root,listvariable=tishi,width=60).grid(row=2,column=0,columnspan=7)
root.mainloop()