
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

#随机数 random.randint(0,9)

xls = common.get_xls("h5.xlsx", "发送验证码")   #excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*xls)
class Sendcode(unittest.TestCase):
    def setParameters(self, case_name,url, method,userType	,account	,accountType	,operateType	,codeLength	,siteId	,typeId	,msg):

        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.msg = str(msg)
        self.return_json = None  #返回值
        self.info = None  #json结果
        self.userType=int(userType)
        self.accountType=int(accountType)
        self.operateType = int(operateType)
        self.codeLength = int(codeLength)
        self.siteId = int(siteId)
        self.typeId = int(typeId)
        #self.account=str(account)


    def description(self):

        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")  #log启动

    def test(self):

        # 拼接url，也可以从excel中获取
        #self.url = comm.get_url_from_xml('login')
        configHttp.set_h5url(self.url)
        print("第1步：设置url  "+self.url)

        # 设置参数
        a = random.randint(12345, 99009)  #随机数
        account = "127000" + str(a)
        paramJson = {"userType":self.userType,
                     "account":account,
                     "accountType":self.accountType,
                     "operateType":self.operateType,
                     "codeLength":self.codeLength,
                     "siteId":self.siteId,
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
        ReadConfig.set_patient('codeid',self.info['responseObject']['responsePk'])
        self.assertEqual(self.return_json.status_code,200)
        self.assertEqual(self.info['responseObject']['responseMessage'],self.msg)
        #self.assertEqual(self.info['responseObject']['responseStatus'],True )



# if __name__=='__main__':
#     unittest.main()



