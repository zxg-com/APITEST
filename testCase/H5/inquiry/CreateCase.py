
import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import  businessCommon

xls = common.get_xls("h5.xlsx", "创建病例")   #excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*xls)
class CreateCase(unittest.TestCase):
    def setParameters(self, case_name,url, method,visitSiteId,operatorType,caseType,
                      customerId,patientId,illnessHistoryId,illnessHistory,treatmentHospital,
                      treatmentHospitalId,affectedAttId,inspectionAttId,takeMedicine,height,
                      weight,descriptionDisease,needHelp,optionList,msg):

        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.msg = str(msg)
        self.return_json = None  #返回值
        self.info = None  #json结果
        self.visitSiteId=str(visitSiteId)
        self.operatorType=str(operatorType)
        self.caseType = str(caseType)
        self.illnessHistoryId = str(illnessHistoryId)
        self.illnessHistory = str(illnessHistory)
        self.treatmentHospital = str(treatmentHospital)
        self.treatmentHospitalId = str(treatmentHospitalId)
        self.affectedAttId = str(affectedAttId)
        self.takeMedicine = str(takeMedicine)
        self.height = str(height)
        self.weight = str(weight)
        self.descriptionDisease = str(descriptionDisease)
        self.needHelp = str(needHelp)
        self.optionList = str(optionList)

    def description(self):

        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")  #log启动
        # businessCommon.h5_login()

    def testCreateCase(self):

        # 拼接url，也可以从excel中获取
        #self.url = comm.get_url_from_xml('login')
        configHttp.set_h5url(self.url)
        print("第1步：设置url  "+self.url)

        # 设置参数
        customerId=ReadConfig.get_patient('patient_customerid')
        patientId=ReadConfig.get_patient('patientid')
        picName = "testpicture.png"
        r=businessCommon.uploadPic(picName)
        paramJson ={"visitSiteId":self.visitSiteId,
                    "operatorType":self.operatorType,
                    "caseType":self.caseType,
                    "customerId":customerId,
                    "patientId":patientId,
                    "illnessHistoryId":self.illnessHistoryId,
                    "illnessHistory":self.illnessHistory,
                    "treatmentHospital":self.treatmentHospital,
                    "treatmentHospitalId":self.treatmentHospitalId,
                    "affectedAttId":self.affectedAttId,
                    "inspectionAttId":r[0],
                    "takeMedicine":self.takeMedicine,
                    "height":self.height,
                    "weight":self.weight,
                    "descriptionDisease":self.descriptionDisease,
                    "needHelp":self.needHelp,
                    "optionList":self.optionList}
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
        #self.assertEqual(self.info['responseObject']['responseMessage'],self.msg)
        self.assertEqual(self.info['responseObject']['responseStatus'],True )
        ReadConfig.set_case('caseid',self.info['responseObject']['responsePk'])







