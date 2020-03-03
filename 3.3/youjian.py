# coding=utf-8
from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email.utils import parseaddr,formataddr#设置编码格式
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os



from_addr='******@qq.com'
password="" #注意此处输入的密码是自己设置的协议密码
to_addr='******@163.com'
smtp_server='smtp.qq.com'

msg=MIMEMultipart()
msg['From']="******@qq.com <******@qq.com>"
msg['To']="******@163.com <******@163.com>"
msg['Subject']=Header('实验验证','utf-8').encode()

msg.attach(MIMEText('实验验证','plain','utf-8'))

x = os.getcwd()
x = x + "\\1.zip"
# print(x)
with open(x,'rb') as f:
    mime=MIMEBase('application','zip',filename='1.zip')
    mime.add_header('Content-Disposition','attchment',filename='1.zip')
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