
import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import  businessCommon
import random

xls = common.get_xls("h5.xlsx", "手机号更换绑定")   #excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*xls)
class mobileupadta(unittest.TestCase):
    def setParameters(self, case_name,url, method,customerId,mobile,typeId,optType,codeId,validCode, msg):

        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.customerId=str(customerId)
        self.mobile = str(mobile)
        self.typeId= str(typeId)
        self.optType=str(optType)
        self.codeId=str(codeId)
        self.validCode=str(validCode)
        self.msg = str(msg)
        self.return_json = None  #返回值
        self.info = None  #json结果



    def description(self):

        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")  #log启动

    def testmobileupdata(self):

        # 拼接url，也可以从excel中获取
        #self.url = comm.get_url_from_xml('login')
        configHttp.set_h5url(self.url)
        print("第1步：设置url  "+self.url)

        # 设置参数
        if self.customerId == "":
            self.customerId=ReadConfig.get_patient('patient_customerid')
        account = random.randint(11111, 98878)
        #self.mobile = "15011270128"
        self.mobile = "127001"+str(account)
        code = businessCommon.h5_changemobilecode(self,self.mobile)
        self.codeId = code[0]
        self.validCode=code[1]
        paramJson = {"customerId":self.customerId,"mobile":self.mobile,
                     "typeId":self.typeId,"optType":self.optType,"codeId":self.codeId,
                     "validCode":self.validCode,
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
        ReadConfig.set_patient('mobile',self.mobile)  #新mobile写入ini
        # 显示返回结果
        common.show_return_msg(self.return_json)
        self.assertEqual(self.return_json.status_code,200)
        #self.assertEqual(self.info['responseObject']['responseMessage'],self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True )







