#coding=UTF-8
import os
import threading
import queue
import getopt
import sys
import PyPDF4
import msoffcrypto
import time

wover = False

def spplit_linux(source_dir):
    # source_dir = input("Please input your password's path(for example:/usr/bin/1.txt):")
    x = os.getcwd()
    os.mkdir(x + '/pass')
    target_dir = x + '/pass/'

    flag = 0
    name = 2
    datalist = []

    print("分割密码文件中……")

    with open(source_dir, 'r') as f_source:
        for line in f_source:
            flag += 1
            datalist.append(line)
            if flag == 10000:
                with open(target_dir + "pass_" + str(name) + ".txt", 'w+') as f_target:
                    for data in datalist:
                        f_target.write(data)
                name += 1
                flag = 0
                datalist = []
                with open(target_dir + "pass_" + str(name) + ".txt", 'w+') as f_target:
                    for data in datalist:
                        f_target.write(data)  

    print("分割结束，开始爆破")

def spplit_windows(source_dir):
    # source_dir = input("Please input your password's path(for example:D:\\\\1.txt):")
    x = os.getcwd()
    os.mkdir(x + '\\\\pass')
    target_dir = x + '\\\\pass\\\\'

    flag = 0
    name = 2
    datalist = []

    print("分割密码文件中……")

    with open(source_dir, 'r') as f_source:
        for line in f_source:
            flag += 1
            datalist.append(line)
            if flag == 10000:
                with open(target_dir + "pass_" + str(name) + ".txt", 'w+') as f_target:
                    for data in datalist:
                        f_target.write(data)
                name += 1
                flag = 0
                datalist = []   
                with open(target_dir + "pass_" + str(name) + ".txt", 'w+') as f_target:
                    for data in datalist:
                        f_target.write(data)

    print("分割结束，开始爆破")

def walkFile(file):
    results = []
    for root, dirs, files in os.walk(file):
        for f in files:
            results.append(os.path.join(root,f))
    return(results)

def pdfcrack(ppath,q):
    pdfReader = PyPDF4.PdfFileReader(open(ppath, 'rb'))
    global wover
    count = 0
    while not q.empty():
        passwd = q.get()
        # print(threading.current_thread().name+' 测试密码： '+passwd)
        try:
            count = count + 1
            number = pdfReader.decrypt(passwd)
            if number == 1:
                print ('[+]pasword =='+passwd)
                q.queue.clear()
                wover = True
        except Exception  as e:
            if count%10 == 0:
                print(threading.current_thread().name+' 测试密码： '+passwd)
            pass   

def officecrack(spath,q):
    ofile = msoffcrypto.OfficeFile(open(spath, "rb")) #打开文件
    p,f = os.path.split(spath)
    new_name='new_'+f
    new_path=os.path.join(p,new_name)  #新文件路径
    global wover
    while wover!=True:
        if not q.empty():
            passwd = q.get()
            # print(passwd)
            try:
                ofile.load_key(password=passwd)
                ofile.decrypt(open(new_path, "wb"))
                print ('[+]pasword =='+passwd)
                q.queue.clear()
                wover = True
                exit(0)
            except Exception as e:
                pass

def pdfthreadcreate(f,passlist):
    lines = []
    with open(passlist,'r') as s:
        lin = s.readlines()
        for w in lin:
            w = w.strip('\n')
            lines.append(w)
    threadlist = []
    qlen = 0
    q = queue.Queue()
    for y in lines:
        q.put(y)
        qlen+=1
    for t in range(0,9):
        th = threading.Thread(target = pdfcrack,args=(f,q,))
        threadlist.append(th)
        # print("thread %d 建立"%t)
    threadlist.append(threading.Thread(target=show_test, args=(q, qlen,)))
    for x in threadlist:
        x.start()
    for x in threadlist:
        x.join()

def officethreadcreate(f,passlist):
    lines = []
    with open(passlist,'r') as s:
        lin = s.readlines()
        for w in lin:
            w = w.strip('\n')
            lines.append(w)
    threadlist = []
    qlen = 0
    q = queue.Queue()
    for y in lines:
        q.put(y)
        qlen+=1
    for t in range(0,9):
        th = threading.Thread(target = officecrack,args=(f,q,))
        threadlist.append(th)
    threadlist.append(threading.Thread(target=show_test, args=(q, qlen,)))
    for x in threadlist:
        x.start()
    for x in threadlist:
        x.join()

def progressbar(nowprogress, toyal):
    get_progress = int((nowprogress+1)*(50/toyal))   # 显示多少>
    get_pro = int(50-get_progress)  # 显示多少-
    percent = (nowprogress+1)*(100/toyal)
    if percent > 100:
        percent = 100
    print("\r"+"["+">"*get_progress+"-"*get_pro+']'+"%.2f" %
          percent + "%", end="")

def show_test(q, qlen):
    while not q.empty():
        # print(q.qsize(),q.unfinished_tasks,qlen )
        progressbar(q.unfinished_tasks-q.qsize(), qlen)
        time.sleep(0.2)
    progressbar(qlen, qlen)

def main(argv):
    if os.name == "posix":
        try:
            opts,args = getopt.getopt(argv,"ha:f:p:")
        except getopt.GetoptError:
            print("ERROR:*.py -a <pdf,doc,ppt,xls> -f <filepath> -p <passwordpath>")
            sys.exit(2)

        for opt,arg in opts:
            if opt == "-h":
                print("*.py -a <pdf,doc,ppt,xls> -f <filepath> -p <passwordpath>")
            elif opt == "-a":
                # print(1)
                filepath = sys.argv[4]
                passpath = sys.argv[6]
                # print(filepath)
                # print(passpath)
                spplit_linux(passpath) #对密码文件的切割
                path = os.getcwd() + "/pass/"
                x = walkFile(path)
                if arg == "pdf":
                    for i in x:
                        pdfthreadcreate(filepath,i)
                else:
                    for i in x:
                        officethreadcreate(filepath,i)
    elif os.name == "nt":
        try:
            opts,args = getopt.getopt(argv,"ha:f:p:")
        except getopt.GetoptError:
            print("ERROR:*.py -a <pdf,doc,ppt,xls> -f <filepath> -p <passwordpath>")
            sys.exit(2)

        for opt,arg in opts:
            if opt == "-h":
                print("*.py -a <pdf,doc,ppt,xls> -f <filepath> -p <passwordpath>")
            elif opt == "-a":
                filepath = sys.argv[4]
                passpath = sys.argv[6]
                spplit_windows(passpath) #对密码文件的切割
                path = os.getcwd() + "\\\\pass\\\\"
                x = walkFile(path)
                if arg == "pdf":
                    for i in x:
                        pdfthreadcreate(filepath,i)
                else:
                    for i in x:
                        officethreadcreate(filepath,i)

if __name__ == '__main__':
    main(sys.argv[1:])
    