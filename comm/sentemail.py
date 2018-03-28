# -- coding:utf-8 --
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

# # 输入Email地址和口令:
# from_addr = "zxg_com@163.com"
# password = "zxg680210"
# # 输入SMTP服务器地址:
# smtp_server ="smtp.163.com"
# # 输入收件人地址:
# to_addr ="zxg_com@163.com"
# to_addr1="342509492@qq.com"
# receivelist=[to_addr1,to_addr]
#
# log = MyLog.get_log()
# reportpath = log.get_result_path()
# logger = log.get_logger()
# msg = MIMEMultipart('related')  #email content
#
# def _format_addr(s):
#     name, addr = parseaddr(s)
#     return formataddr((Header(name, 'utf-8').encode(), addr))   #初始化收发件人信息
#
# msg['From'] = _format_addr('报告发送人 <%s>' % from_addr)
# msg['Subject'] = Header('测试报告', 'utf-8').encode()

# #内容模板
# f = open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt'))
# content = f.read()
# f.close()
# content_plain = MIMEText(content, 'html', 'UTF-8')
# msg.attach(content_plain)  #msg内容模板引入
#
#
# # resultPath = os.path.join(readConfig.proDir,"result","20180305132237")
# files = glob.glob(reportpath + r'/*')  #获取目录下所有文件  指定log格式文件 +"\*.log"
#
# zippath = os.path.join(readConfig.proDir, "result", "test.zip")
# f=zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)  #r读zip  w写zip
#
# for file in  files:
#     f.write(file,os.path.basename(file))
# f.close()
# reportfile = open(zippath, 'rb').read()
# filehtml = MIMEText(reportfile, 'base64', 'utf-8')
# filehtml['Content-Type'] = 'application/octet-stream'
# filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
# msg.attach(filehtml)
#
#发送
# server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
# server.set_debuglevel(1)
# server.login(from_addr, password)
# server.sendmail(from_addr, receivelist, msg.as_string())
# server.quit()
# print("邮件发送成功")

import datetime

localReadConfig = readConfig.ReadConfig()
resultpath = os.path.join(readConfig.proDir,"result")
class Email:
    def __init__(self):
        global smtp_server, user, password, port, sender, title,content
        smtp_server = localReadConfig.get_email("smtp_server")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        content = localReadConfig.get_email('content')
        # 获取接收者列表信息
        self.receiver = localReadConfig.get_email("receiver")
        #print(self.receiver)
        self.receivelist = []
        for n in  str(self.receiver).split(';'):   #分号区分收件人
            self.receivelist.append(n)
        #print(self.receivelist)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = "接口测试报告" + " " + date
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')  #混合类型


    def config_header(self):
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to']= str(self.receiver)  #显示收件人


    def config_content(self):
       #内容模板  不用摸板可以直接套用ini文件中的信息
        f = open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)


    def config_file(self):
        reportpath = self.log.get_result_path()
        #将所有文件夹打包
        # files = glob.glob(reportpath + r'/*')  # 获取目录下所有文件  指定log格式文件 +"\*.log"
        # zippath = os.path.join(readConfig.proDir, "result", "report.zip")
        # f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)  # r读zip  w写zip
        # for file in files:
        #     f.write(file, os.path.basename(file))
        # f.close()
        # reportfile = open(zippath, 'rb').read()


        #最后创建的html和log文件打包
        lists = os.listdir(reportpath)
        lists.sort(key=lambda fn:os.path.getmtime(reportpath+"/"+fn)) #创建时间排序
        file =  os.path.join(reportpath,lists[-1])
        file1 = os.path.join(reportpath,lists[-2])
        zippath = os.path.join(readConfig.proDir, "result", "report.zip")
        f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)  # r读zip  w写zip
        f.write(file, os.path.basename(file))  #写进压缩包
        f.write(file1,os.path.basename(file1))
        f.close()
        reportfile = open(zippath, 'rb').read() #读取压缩文件

        #添加为邮件附件
        filehtml = MIMEText(reportfile, 'base64', 'utf-8')
        filehtml['Content-Type'] = 'application/octet-stream'
        filehtml['Content-Disposition'] = 'attachment; filename="report.zip"'
        self.msg.attach(filehtml)

    def send_email(self):
        self.config_header()
        self.config_content()
        self.config_file()
        try:

            smtp = smtplib.SMTP(smtp_server,port)
            smtp.connect(smtp_server)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receivelist, self.msg.as_string())
            smtp.quit()
            self.logger.info("报告已发送至邮箱.")
            print("报告已发送至邮箱")
        except Exception as ex:
            self.logger.error(str(ex))
            print(str(ex))

class MyEmail:    #线程
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
