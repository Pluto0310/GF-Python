#coding:utf-8
import linecache

num_list=[338,630,440,596,287,943,716,793,447,897]
filename='/Users/deng/Desktop/network attack&defense/program/zipcrack/password/password1.txt'

for i in range(len(num_list)):
    line_num=int(num_list[i]/4)
    remind=num_list[i]%4
    # if (remind!=0):
    #     line_num= line_num+1
    count = linecache.getline(filename,line_num)
    count_list=count.split()
    passwd=count_list[(remind-1)%4]
    print ('第'+str(num_list[i])+'个密码是：'+passwd)