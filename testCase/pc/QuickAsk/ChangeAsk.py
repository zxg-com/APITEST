

import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon

xls = common.get_xls("pc.xlsx", "修改快捷提问")  # excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*xls)
class ChangeAsk(unittest.TestCase):
    def setParameters(self, case_name, url, method,customerId,treeLevel	,isValid,id,questionDesc,questionId,fullPath,questionType,msg ):
        self.case_name = str(case_name)
        self.method = str(method)
        self.isValid = str(isValid)
        self.treeLevel=int(treeLevel)
        self.questionDesc = str(questionDesc)
        self.questionType = int(questionType)
        self.msg = str(msg)
        self.return_json = None  # 返回值
        self.info = None  # json结果
        self.url = str(url)

    def description(self):
        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        businessCommon.login()
        businessCommon.getwebuser()
        print(self.case_name + "测试开始前准备")  # log启动

    def testChangeAsk(self):

        # 拼接url，也可以从excel中获取
        # self.url = comm.get_url_from_xml('login')
        configHttp.set_pcurl(self.url)
        print("第1步：设置url  " + self.url)

        # 设置参数
        customerid=ReadConfig.get_customer('customerid')
        questionId=ReadConfig.get_im('questionid')
        groupId=ReadConfig.get_im('question_groupid')
        fullpath=str(groupId+","+questionId)
        paramJson={'customerId':customerid,
                   'treeLevel':self.treeLevel,
                   'isValid':self.isValid,
                   'id':questionId,
                   'questionDesc':self.questionDesc,
                   'questionId':questionId,
                   'fullPath':fullpath,
                   'questionType':self.questionType}
        data = {'paramJson':str(paramJson)
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

        # 把casename，url,返回值传入log打印
        self.log.build_case_line(self.case_name, self.url, self.return_json.text)

        businessCommon.logout()
        print("测试结束，输出log完结\n\n")


    # 断言
    def checkResult(self):
        self.info = self.return_json.json()

        # 显示返回结果
        common.show_return_msg(self.return_json)
        #存入分组id
        #ReadConfig.set_im('questionid', self.info['responseObject']['responseData']['dataList']['questionId'])
        self.assertEqual(self.return_json.status_code, 200)
        #self.assertEqual(self.info['responseObject']['responseMessage'], self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True )



# if __name__=='__main__':
#     unittest.main()




