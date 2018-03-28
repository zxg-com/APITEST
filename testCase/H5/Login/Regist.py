
import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import  businessCommon
from comm import configDB
import random
import random
import re
import time
#随机数 random.randint(0,9)

xls = common.get_xls("h5.xlsx", "注册")   #excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
db=configDB.MyDB
info = {}

@paramunittest.parametrized(*xls)
class Regist(unittest.TestCase):
    def setParameters(self, case_name,url, method,account,password,validCode,siteId,codeId,optType,typeId,msg):

        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.msg = str(msg)
        self.return_json = None  #返回值
        self.info = None  #json结果
        self.password=str(password)
        self.siteId=int(siteId)
        self.optType = int(optType)
        self.typeId = int(typeId)
        self.account=str(account)
        self.validCode=str(validCode)




    def description(self):

        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")  #log启动


    def testRegist(self):

        # 拼接url，也可以从excel中获取
        #self.url = comm.get_url_from_xml('login')
        configHttp.set_h5url(self.url)
        print("第1步：设置url  "+self.url)

        # 设置参数
        ran = random.randint(11111, 98878)
        if self.account == "":
            self.account = "127000" + str(ran)  # 手机号
        r = businessCommon.h5_Rigistsendcode(self, self.account)  # 发注册验证码


        if self.validCode == "":
            self.validCode = r[1]

        paramJson = {"account":self.account,
                     "password":self.password,
                     "validCode":self.validCode,
                     "siteId":self.siteId,
                     "codeId":r[0],
                     "optType":self.optType,
                     "typeId":self.typeId
                     }
        data = {
            'paramJson': str(paramJson)
        }


        configHttp.set_data(data)
        print("第2步：设置发送请求的参数")
        print(data)


        # 测试接口
        self.return_json = configHttp.post()
        method = self.method
        print("第3步：发送请求\n\t\t请求方法："+method)



        # 校验结果
        self.checkResult()
        print("第4步：检查结果")



    def tearDown(self):

        info = self.info
        #把casename，url,返回值传入log打印
        self.log.build_case_line(self.case_name, self.url, self.return_json.text)

        print("测试结束，输出log完结\n\n")





    #断言
    def checkResult(self):

        self.info = self.return_json.json()
        # 显示返回结果
        common.show_return_msg(self.return_json)
        self.assertEqual(self.return_json.status_code,200)
        self.assertEqual(self.info['responseObject']['responseMessage'],self.msg)
        #self.assertEqual(self.info['responseObject']['responseStatus'],True )
        customerID=info['responseObject']['responsePk']
        if self.info['responseObject']['responseStatus'] == True:
            #执行无效账号
            businessCommon.deleteAccount(customerID,self.account)








