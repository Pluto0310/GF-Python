import rarfile
import optparse
from threading import Thread

def extractFile(rFile,password):
    try:
        # print(passwd_list[i])
        rFile.extractall(pwd=password)
        print ('[+] Password ='+ password +'\n')
        # exit(0)
    except:
        pass

def main():
    parser=optparse.OptionParser("usage%prog "+\
        "-f <rarfile> -d <dictionary>")
    parser.add_option('-f',dest='rname',type='string',\
        help='specify zip file')
    parser.add_option('-d',dest='dname',type='string',\
        help='specify dictionary file')
    (options,args)=parser.parse_args()
    if (options.rname ==None) | (options.dname ==None):
        print (parser.usage)
        exit(0)
    else:
        rname=options.rname
        dname=options.dname
    rFile = rarfile.RarFile(rname)
    passFile=open(dname)
    for line in passFile.readlines():
        password=line.strip('\n')
        passwd_list=password.split()
        for i in range(4):
            t=Thread(target=extractFile,args=(rFile,passwd_list[i]))
            t.start()

if __name__ == "__main__":
    main()
