import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon
import requests
triage1_xls = common.get_xls("pc.xlsx", "患者列表搜索")   #excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()

info = {}

@paramunittest.parametrized(*triage1_xls)
class Triagelist_search(unittest.TestCase):
    def setParameters(self, case_name,url,method,conType,triageType,sortType,selectName,msg):

        self.case_name = str(case_name)
        self.method = str(method)
        self.url = str(url)
        #self.customerID = int(customerID)
        self.conType = int(conType)
        self.triageType = int(triageType)
        self.sortType = int(sortType)
        self.msg = str(msg)
        self.selectName=str(selectName)
        self.return_json = None  #返回值
        self.info = None  #json结果

    def description(self):

        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")  #log启动
        businessCommon.login()
        businessCommon.getwebuser()

    def testTriagelist_search(self):

        # 拼接url，从excel中获取

        configHttp.set_pcurl(self.url)
        print("第1步：设置url  "+self.url)

        # 设置参数customerID,conType,triageType,sortType
        customerid=ReadConfig.get_customer('customerid')

        s={"customerId":customerid,"conType":self.conType,"triageType":self.triageType,"sortType":self.sortType,"selectName":self.selectName}
        data={"paramJson":str(s)}
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
        businessCommon.logout()



    #断言
    def checkResult(self):

        self.info = self.return_json.json()
        # 显示返回结果
        common.show_return_msg(self.return_json)
        self.assertEqual(self.return_json.status_code,200)
        #self.assertEqual(self.info['responseObject']['responseMessage'],self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True )
        #ReadConfig.set_case('caseid',self.info['responseObject']['responseData']['dataList'][0]['caseId'])
        #ReadConfig.set_patient('patientid', self.info['responseObject']['responseData']['dataList'][0]['patientId'])
        #ReadConfig.set_patient('patientname', self.info['responseObject']['responseData']['dataList'][0]['patientName'])


if __name__=='__main__':
    unittest.main()
