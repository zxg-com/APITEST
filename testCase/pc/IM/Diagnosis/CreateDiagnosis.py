import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon

xls = common.get_xls("pc.xlsx", "创建初诊建议")  # excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*xls)
class CreateDiagnosis(unittest.TestCase):
    def setParameters(self, case_name, url, method, customerId,caseId,patientId,diagnosisType,majorId,majorName,
                      illnessId,illnessName,operationId,operationName,degreeType,positionId,positionName,msg ):
        self.case_name = str(case_name)
        self.method = str(method)
        self.diagnosisType = str(diagnosisType)
        self.illnessName = str(illnessName)
        self.degreeType = int(degreeType)
        self.majorId=int(majorId)
        self.majorName=str(majorName)
        self.illnessId=str(illnessId)
        self.operationId=str(operationId)
        self.operationName=str(operationName)
        self.positionId=str(positionId)
        self.positionName=str(positionName)
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

    def testCreateDiagnosis(self):
        # 拼接url，也可以从excel中获取
        # self.url = comm.get_url_from_xml('login')
        configHttp.set_pcurl(self.url)
        print("第1步：设置url  " + self.url)

        # 设置参数
        customerId = ReadConfig.get_customer('customerid')
        caseId = ReadConfig.get_case('caseid')
        patientId = ReadConfig.get_patient('patientid')
        paramJson = {'customerId': customerId, 'caseId': caseId, 'patientId': patientId,
                     'diagnosisType': self.diagnosisType, 'majorId': self.majorId, 'majorName': self.majorName,
                     'illnessId': self.illnessId, 'illnessName': self.illnessName, 'operationId': self.operationId,
                     'operationName': self.operationName, 'degreeType': self.degreeType, 'positionId': self.positionId,
                     'positionName': self.positionName}
        data = {
            'paramJson': str(paramJson)
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
        dianosisId=self.info['responseObject']['responsePk']
        ReadConfig.set_case("dianosisId",str(dianosisId))
        # 显示返回结果
        common.show_return_msg(self.return_json)
        self.assertEqual(self.return_json.status_code, 200)
        #self.assertEqual(self.info['responseObject']['responseMessage'], self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True )


#
# if __name__=='__main__':
#     unittest.main()




