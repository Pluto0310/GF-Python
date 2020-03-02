# coding=UTF-8
import itertools as its
import sys
import getopt
import math
def main(argv):

    strr = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM".strip()

    try:
        opts, args = getopt.getopt(argv, "hl:s")
    except getopt.GetoptError:
        print("ERROR: *.py -l <length of password> -s <calc store space>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("*.py -l <length of password> -s <calc store space>")
        elif opt == "-l":
            len = int(arg)
            r = its.product(strr,repeat=len) 
            dic = open("pass.txt",'a')
            for i in r:
                dic.write(''.join(i)+"\n")
            dic.close()
        elif opt == "-s":
            print("password space is:%d"%((len + 1) * (pow(62,len)) / 1000) + "Kb")


if __name__ == "__main__":
    main(sys.argv[1:])