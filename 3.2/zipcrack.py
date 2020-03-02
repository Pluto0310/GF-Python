import zipfile
import optparse
from threading import Thread

def extractFile(zFile,password):
    try:
        # print(passwd_list[i])
        zFile.extractall(pwd=password.encode("ascii"))
        print ('[+] Password ='+ password +'\n')
        # exit(0)
    except:
        pass

def main():
    parser=optparse.OptionParser("usage%prog "+\
        "-f <zipfile> -d <dictionary>")
    parser.add_option('-f',dest='zname',type='string',\
        help='specify zip file')
    parser.add_option('-d',dest='dname',type='string',\
        help='specify dictionary file')
    (options,args)=parser.parse_args()
    if (options.zname ==None) | (options.dname ==None):
        print (parser.usage)
        exit(0)
    else:
        zname=options.zname
        dname=options.dname
    zFile = zipfile.ZipFile(zname)
    passFile=open(dname)
    for line in passFile.readlines():
        password=line.strip('\n')
        passwd_list=password.split()
        for i in range(4):
            t=Thread(target=extractFile,args=(zFile,passwd_list[i]))
            t.start()

if __name__ == "__main__":
    main()
