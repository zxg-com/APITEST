
import smtplib
import email
import os
import readConfig
import smtplib
from comm.Log import MyLog
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import zipfile
import glob
import threading

# 输入Email地址和口令:
from_addr = "zxg_com@163.com"
password = "zxg680210"
# 输入SMTP服务器地址:
smtp_server ="smtp.163.com"
# 输入收件人地址:
to_addr ="zxg_com@163.com"
to_addr1="342509492@qq.com"
receivelist=[to_addr1,to_addr]

log = MyLog.get_log()
reportpath = log.get_result_path()
logger = log.get_logger()
msg = MIMEMultipart('related')  #email content

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))   #初始化收发件人信息

msg['From'] = _format_addr('报告发送人 <%s>' % from_addr)
msg['Subject'] = Header('测试报告', 'utf-8').encode()
msg['To'] = _format_addr('报告接受者<%s><%s>'%(to_addr,to_addr1))

#内容模板
f = open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt'))
content = f.read()
f.close()
content_plain = MIMEText(content, 'html', 'UTF-8')
msg.attach(content_plain)  #msg内容模板引入


# resultPath = os.path.join(readConfig.proDir,"result","20180305132237")
files = glob.glob(reportpath + r'/*')  #获取目录下所有文件  指定log格式文件 +"\*.log"

zippath = os.path.join(readConfig.proDir, "result", "测试报告.zip")
f=zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)  #r读zip  w写zip

for file in  files:
    f.write(file,os.path.basename(file))
f.close()
reportfile = open(zippath, 'rb').read()
filehtml = MIMEText(reportfile, 'base64', 'utf-8')
filehtml['Content-Type'] = 'application/octet-stream'
filehtml['Content-Disposition'] = 'attachment; filename="测试报告.zip"'
msg.attach(filehtml)

# 发送
server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, receivelist, msg.as_string())
server.quit()
print("邮件发送成功")