# coding=utf-8
import os       #引入操作系统模块
import sys      #用于标准输入输出
from glob import *
import shutil
import zipfile
from subprocess import Popen, PIPE

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

def coppylinux(lista):
    x = os.getcwd()
    for i in lista:
        a = find_last(i,'/')
        j = i[a + 1:(len(i) + 1)]
        shutil.copyfile(i,x + "/test/" + j)

def coppywindows(lista):
    x = os.getcwd()
    for i in lista:
        a = find_last(i,'\\')
        j = i[a + 1:(len(i) + 1)]
        shutil.copyfile(i,x + "\\\\test\\\\" + j)

def main():
    oss = input("please input your sys(Windows or Linux):")
    
    if oss == "Linux":
        path = input("please input path(for example:/usr/bin):")

        os.mkdir(os.getcwd() + "/test/")

        mes = getIfconfig()
        mes1 = gethostname()
        mes2 = getos()

        with open(os.getcwd() + "/test/message.txt", "wb+") as f:
            f.write(mes)
            f.write(mes1)
            f.write(mes2)
            f.close()

        lis = matchWildcard(path, "*.pptx")
        lis1 = matchWildcard(path, "*.docx")
        lis2 = matchWildcard(path, "*.xlsx")

        coppylinux(lis)
        coppylinux(lis1)
        coppylinux(lis2)
    
        e = os.getcwd()
        zipDir(e + "/test/",e + "/1.zip")
    elif oss == "Windows":
        path = input("please input path(for example:D:\\\\):")

        os.mkdir(os.getcwd() + "\\\\test\\\\")

        mes = getipconfig()
        mes1  = getosname()
        mes2 = getver()

        with open(os.getcwd() + "\\\\test\\\\message.txt", "w", encoding='utf-8') as f:
            f.write(mes)
            f.write(mes1)
            f.write(mes2)
            f.close()

        lis = matchWildcard(path, "*.pptx")
        lis1 = matchWildcard(path, "*.docx")
        lis2 = matchWildcard(path, "*.xlsx")

        coppywindows(lis)
        coppywindows(lis1)
        coppywindows(lis2)

        e = os.getcwd()
        zipDir(e + "\\\\test\\\\",e + "\\\\1.zip")
    
if __name__ == "__main__":
    main()