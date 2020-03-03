from ftplib import FTP
import os

ip = '192.168.16.176'
port = 2121
timeout = 30

ftp = FTP()

ftp.set_debuglevel(2)
ftp.connect(ip, port, timeout)
ftp.login('kali', '123456')
print (ftp.getwelcome())
bufsize = 1024
filename = 'a.txt'
fh = open(filename, 'rb')
ftp.storbinary('STOR %s' % os.path.basename(filename), fh, bufsize)
ftp.set_debuglevel(0)
fh.close()
ftp.quit()

