import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon

xls = common.get_xls("pc.xlsx", "全部医生列表搜索")  # excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*xls)
class Searchcustomerlist(unittest.TestCase):
    def setParameters(self, case_name, url, method, isMatch,isValid,logoUseFlag,firstResult,maxResult,illnessId	,areasExpertise,patientId,searchParam,searchAreasExpertise,degreeType,searchOnlineState,searchRegion,searchDoctorType,msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.isMatch = str(isMatch)
        self.isValid = str(isValid)
        self.logoUseFlag = str(logoUseFlag)
        self.firstResult = int(firstResult)
        self.maxResult = int(maxResult)
        self.illnessId = str(illnessId)
        self.areasExpertise = str(areasExpertise)
        self.searchParam = str(searchParam)
        self.searchAreasExpertise = str(searchAreasExpertise)
        self.degreeType = int(degreeType)
        self.searchOnlineState = str(searchOnlineState)
        self.searchRegion = str(searchRegion)
        self.searchDoctorType=str(searchDoctorType)
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

    def testSearchcustomerlist(self):
        # 拼接url，也可以从excel中获取
        # self.url = comm.get_url_from_xml('login')
        configHttp.set_pcurl(self.url)
        print("第1步：设置url  " + self.url)
        patientId = ReadConfig.get_patient('patientid')
        # 设置参数
        paramJson = {'isMatch': self.isMatch, 'isValid': self.isValid, 'logoUseFlag': self.logoUseFlag,
                     'firstResult': self.firstResult, 'maxResult': self.maxResult, 'illnessId': self.illnessId,
                     'areasExpertise': self.areasExpertise, 'patientId': patientId, 'searchParam': self.searchParam,
                     'searchAreasExpertise': self.searchAreasExpertise, 'degreeType': self.degreeType,
                     'searchOnlineState': self.searchOnlineState,"searchRegion":self.searchRegion,"searchDoctorType":self.searchDoctorType}
        data = {'paramJson': str(paramJson)}

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

        print("测试结束，输出log完结\n\n")

    # 断言
    def checkResult(self):
        self.info = self.return_json.json()
        # 显示返回结果
        common.show_return_msg(self.return_json)
        self.assertEqual(self.return_json.status_code, 200)
        #self.assertEqual(self.info['responseObject']['responseMessage'], self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True)



# if __name__=='__main__':
#      unittest.main()
