import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon

xls = common.get_xls("pc.xlsx", "患者列表case获取备注信息")  # excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*xls)
class caseRemark(unittest.TestCase):
    def setParameters(self, case_name, url, method,caseId,firstResult,maxResult,isValid ,msg ):
        self.case_name = str(case_name)
        self.method = str(method)
        self.firstResult = int(firstResult)
        self.maxResult = int(maxResult)
        self.isValid = int(isValid)
        self.msg = str(msg)
        self.return_json = None  # 返回值
        self.info = None  # json结果
        self.url = str(url)

    def description(self):
        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")  # log启动

    def testcaseRemark(self):

        # 拼接url，也可以从excel中获取
        # self.url = comm.get_url_from_xml('login')
        configHttp.set_pcurl(self.url)
        print("第1步：设置url  " + self.url)
        caseid=ReadConfig.get_case("caseid")
        s={"caseId":caseid,
           "firstResult":self.firstResult,
           "maxResult":self.maxResult,
           "isValid":self.isValid
           }
        # 设置参数
        data = {"ParamJson":str(s)
        }

        configHttp.set_data(data)
        print("第2步：设置发送请求的参数")
        print(data)

        # 测试接口
        self.return_json = configHttp.post()
        method = self.method
        print("第3步：发送请求\n\t\t请求方法：" + method)

        # 校验结果
        self.checkResult()
        print("第4步：检查结果")


    def tearDown(self):
        info = self.info
        # 把casename，url,返回值传入log打印
        self.log.build_case_line(self.case_name, self.url, self.return_json.text)
        businessCommon.logout()
        print("测试结束，输出log完结\n\n")


    # 断言
    def checkResult(self):
        self.info = self.return_json.json()
        # 显示返回结果
        common.show_return_msg(self.return_json)
        self.assertEqual(self.return_json.status_code, 200)
        #self.assertEqual(self.info['responseObject']['responseMessage'], self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True )



# if __name__=='__main__':
#     unittest.main()




