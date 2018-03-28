import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon

xls = common.get_xls("pc.xlsx", "现病史保存")  # excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*xls)
class saveHpi(unittest.TestCase):
    def setParameters(self, case_name, url, method, id,caseId,produceReason,produceSymptomsId,produceSymptomsName,produceLevelId,produceLevelName,produceSharpenId,produceSharpenName,produceRemitId,produceRemitName,produceTreatment,aggravateReason,aggravateSymptomsId,aggravateSymptomsName,aggravateLevelId,aggravateLevelName,aggravateSharpenId,aggravateSharpenName,aggravateRemitId,aggravateRemitName,aggravateTreatment,sleepId,sleepName,spiritId,spiritName,appetiteId,appetiteName,weightId,weightName,excretionId,excretionName,remark,patientId,visualInspection,activityState	,muscleStrength,msg):
        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.msg = str(msg)
        self.return_json = None  # 返回值
        self.info = None  # json结果
        self.produceReason = str(produceReason)
        self.produceSymptomsId = str(produceSymptomsId)
        self.produceSymptomsName = str(produceSymptomsName)
        self.produceLevelId = str(produceLevelId)
        self.produceLevelName = str(produceLevelName)
        self.produceSharpenId = str(produceSharpenId)
        self.produceSharpenName = str(produceSharpenName)
        self.produceRemitId = str(produceRemitId)
        self.produceRemitName = str(produceRemitName)
        self.produceTreatment = str(produceTreatment)
        self.aggravateReason = str(aggravateReason)
        self.aggravateSymptomsId = str(aggravateSymptomsId)
        self.aggravateSymptomsName = str(aggravateSymptomsName)
        self.aggravateLevelId = str(aggravateLevelId)
        self.aggravateLevelName = str(aggravateLevelName)
        self.aggravateSharpenId = str(aggravateSharpenId)
        self.aggravateSharpenName = str(aggravateSharpenName)
        self.aggravateRemitId = str(aggravateRemitId)
        self.aggravateRemitName = str(aggravateRemitName)
        self.aggravateTreatment = str(aggravateTreatment)
        self.sleepId = str(sleepId)
        self.sleepName = str(sleepName)
        self.spiritId = str(spiritId)
        self.spiritName = str(spiritName)
        self.appetiteId = str(appetiteId)
        self.appetiteName = str(appetiteName)
        self.weightId = str(weightId)
        self.weightName = str(weightName)
        self.excretionId = str(excretionId)
        self.excretionName = str(excretionName)
        self.remark = str(remark)
        self.visualInspection = str(visualInspection)
        self.activityState=str(activityState)
        self.muscleStrength=str(muscleStrength)



    def description(self):
        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")  # log启动

    def testsaveHpi(self):
        # 拼接url，也可以从excel中获取
        # self.url = comm.get_url_from_xml('login')
        configHttp.set_pcurl(self.url)
        print("第1步：设置url  " + self.url)

        # 设置参数
        hpiid = ReadConfig.get_case('hpi_id')
        caseId = ReadConfig.get_case('caseid')
        patientId = ReadConfig.get_patient('patientid')
        paramJson = {
            "id": hpiid,
            "caseId": caseId,
            "produceReason": self.produceReason,
            "produceSymptomsId": self.produceSymptomsId,
            "produceSymptomsName": self.produceSymptomsName,
            "produceLevelId": self.produceLevelId,
            "produceLevelName": self.produceLevelName,
            "produceSharpenId": self.produceSharpenId,
            "produceSharpenName": self.produceSharpenName,
            "produceRemitId": self.produceRemitId,
            "produceRemitName": self.produceRemitName,
            "produceTreatment": self.produceTreatment,
            "aggravateReason": self.aggravateReason,
            "aggravateSymptomsId": self.aggravateSymptomsId,
            "aggravateSymptomsName": self.aggravateSymptomsName,
            "aggravateLevelId": self.aggravateLevelId,
            "aggravateLevelName": self.aggravateLevelName,
            "aggravateSharpenId": self.aggravateSharpenId,
            "aggravateSharpenName": self.aggravateSharpenName,
            "aggravateRemitId": self.aggravateRemitId,
            "aggravateRemitName": self.aggravateRemitName,
            "aggravateTreatment": self.aggravateTreatment,
            "sleepId": self.sleepId,
            "sleepName": self.sleepName,
            "spiritId": self.spiritId,
            "spiritName": self.spiritName,
            "appetiteId": self.appetiteId,
            "appetiteName": self.appetiteName,
            "weightId": self.weightId,
            "weightName": self.weightName,
            "excretionId": self.excretionId,
            "excretionName": self.excretionName,
            "remark": self.remark,
            "patientId": patientId,
            "visualInspection":self.visualInspection,
            "activityState":self.activityState,
            "muscleStrength":self.muscleStrength

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
        self.assertEqual(self.info['responseObject']['responseStatus'],True )


# if __name__ == '__main__':
#     unittest.main()




