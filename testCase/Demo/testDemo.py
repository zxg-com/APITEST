import unittest
from json import *
import json
import paramunittest
import readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
import requests
from comm import businessCommon
import random
from comm import configDB
import glob
#businessCommon.login()
#businessCommon.getwebuser()
#businessCommon.logout()


# url="https://triage9.allinmed.cn/call/customer/case/consultation/v1/getMapListForCase/"
#
# s={"triageType":1,"conType":0,"sortType":-6}
#
# data={'paramJson':str(s)}
# #"paramJson=%7B%22customerId%22%3A%221510534730272%22%2C%22conType%22%3A0%2C%22triageType%22%3A1%2C%22sortType%22%3A-6%7D"
#
# s=requests.post(url=url,data=data)
# print(s.json())
#

# import unittest
# from json import *
# import json
# import paramunittest
# import readConfig as readConfig
# import re

# from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import  businessCommon

# login_xls = comm.get_xls("pc.xlsx", "login")   #excel取值
# ReadConfig = readConfig.ReadConfig()
# ReadConfig.set_patient('codeid','1000')
# codeId = ReadConfig.get_patient('codeid')
# print(codeId)

#sql
# db=configDB.MyDB
# class A():
#     def A(self):
#         mobile = "12700000082"
#         sql = comm.get_sql('tocure_platform', 'tocure_customer_send_code', 'select_code')
#         print(sql)
#
#          #sql参数化
#         result=db.executeSQL(self,sql=sql,params=mobile)
#         s=db.get_one(self,result)    #返回结果eg.（'1234'，）
#         db.closeDB(self)
#         p = re.findall(r"'(.+?)'",str(s))[0]   #正则取验证码  findall返回元祖，取第一个元素
# a=A()
# a.A()

#图片base64编码处理
# import os
# import base64
# picName = "testpicture.png"
# type = picName.split('.')[1]
# Dir = os.path.join(readConfig.proDir,"testFile","img",picName)
# f=open(Dir,'rb')
# content = base64.b64encode(f.read())
# content_str = content.decode('utf-8')
# print(content_str)

# url="https://m9.allinmed.cn/mcall/customer/patient/case/v2/create/"
#
# paramJson = {}
# data = {"paramJson":str(paramJson)}
# s=requests.post(url,data)
# print(s.text)

import os
import zipfile
from comm import Senttowechat

# log = MyLog.get_log()
# #resultPath = log.get_result_path()
# resultPath = os.path.join(readConfig.proDir,"result","20180305132237")
# files = glob.glob(resultPath + r'/*')  #获取目录下所有文件  指定log格式文件 +"\*.log"
#
# zippath = os.path.join(readConfig.proDir, "result", "test.zip")
# f=zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)  #r读zip  w写zip
#
# for file in  files:
#     f.write(file,os.path.basename(file))
# f.close()
# #

# zippath = os.path.join(readConfig.proDir, "result", "test.zip")
# # zip file
# files = glob.glob(reportpath + '\*')
# f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
# for file in files:
# # 修改压缩文件的目录结构
# f.write(file, os.path.basename(file))  #("文件全路径", "归档文件全路径(也就是写入压缩包的相对路径)")
# f.close()
# reportfile = open(zippath, 'rb').read()
# filehtml = MIMEText(reportfile, 'base64', 'utf-8')
# filehtml['Content-Type'] = 'application/octet-stream'
# filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
# self.msg.attach(filehtml)

#
# def threeNums_method1():
#     '''take out a digit from the four digits'''
#     L = [i for i in range(1,5)]
#     print(L)
#     cnt = 0
#     for index in range(4):
#         L1 = L[:]
#         del L1[index]
#         for index1 in range(3):
#             print ('%d%d%d'%(L1[index1%3],L1[(index1+1)%3],L1[(index1+2)%3]))
#             cnt += 1
#     print ('count : %d'%cnt)
#
# threeNums_method1()

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
import re



L=[0,1,2,3,4,5,6,7,'a','b']
print("数量%d" % len(L))