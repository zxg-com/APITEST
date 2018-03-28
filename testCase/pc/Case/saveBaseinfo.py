
import unittest
from json import *
import json
import paramunittest
import readConfig as readConfig
from comm.Log import MyLog
from comm import common
from comm import configHttp as ConfigHttp
from comm import businessCommon

xls = common.get_xls("pc.xlsx", "患者基本信息保存")  # excel取值

ReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*xls)
class saveBaseinfo(unittest.TestCase):
    def setParameters(self, case_name, url, method,nativeProvinceId,nativeProvince,nativeCityId,nativeCity,nativeDistrictId,nativeDistrict,birthplaceProvinceId,birthplaceProvince,birthplaceCityId,birthplaceCity,birthplaceDistrictId,birthplaceDistrict,patientId,id,address,telephone,socialId,socialAddress,nation,isMarriage,homeAddress,workplace,spouseStatus,childrenStatus,fertility,marriageAge,isSmoke,isDrink,isNarcotics,parentStatus,siblingsStatus,isInfection,isHeredopathia, msg, ):
        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.msg = str(msg)
        self.return_json = None  # 返回值
        self.info = None  # json结果
        self.nativeProvinceId = str(nativeProvinceId)
        self.nativeProvince = str(nativeProvince)
        self.nativeCityId = str(nativeCityId)
        self.nativeCity = str(nativeCity)
        self.nativeDistrictId = str(nativeDistrictId)
        self.nativeDistrict = str(nativeDistrict)
        self.birthplaceProvinceId = str(birthplaceProvinceId)
        self.birthplaceProvince = str(birthplaceProvince)
        self.birthplaceCityId = str(birthplaceCityId)
        self.birthplaceCity = str(birthplaceCity)
        self.birthplaceDistrictId = str(birthplaceDistrictId)
        self.birthplaceDistrict = str(birthplaceDistrict)
        self.address = str(address)
        #self.telephone = str(telephone)
        self.socialId = str(socialId)
        self.socialAddress = str(socialAddress)
        self.nation = str(nation)
        self.isMarriage = str(isMarriage)
        self.homeAddress = str(homeAddress)
        self.workplace = str(workplace)
        self.spouseStatus = str(spouseStatus)
        self.childrenStatus = str(childrenStatus)
        self.fertility = str(fertility)
        self.marriageAge = str(marriageAge)
        self.isSmoke = str(isSmoke)
        self.isDrink = str(isDrink)
        self.isNarcotics = str(isNarcotics)
        self.parentStatus = str(parentStatus)
        self.siblingsStatus = str(siblingsStatus)
        self.isInfection = str(isInfection)
        self.isHeredopathia = str(isHeredopathia)

    def description(self):
        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")  # log启动

    def testsaveBaseinfo(self):
        # 拼接url，也可以从excel中获取
        # self.url = comm.get_url_from_xml('login')
        configHttp.set_pcurl(self.url)
        print("第1步：设置url  " + self.url)

        # 设置参数
        patientId = ReadConfig.get_patient('patientid')
        baseinfo_id = ReadConfig.get_patient('baseinfo_id')
        telephone = ReadConfig.get_patient('mobile')
        paramJson = {"nativeProvinceId":self.nativeProvinceId,
                     "nativeProvince":self.nativeProvince,
                     "nativeCityId":self.nativeCityId,
                     "nativeCity":self.nativeCity,
                     "nativeDistrictId":self.nativeDistrictId,
                     "nativeDistrict":self.nativeDistrict,
                     "birthplaceProvinceId":self.birthplaceProvinceId,
                     "birthplaceProvince":self.birthplaceProvince,
                     "birthplaceCityId":self.birthplaceCityId,
                     "birthplaceCity":self.birthplaceCity,
                     "birthplaceDistrictId":self.birthplaceDistrictId,
                     "birthplaceDistrict":self.birthplaceDistrict,
                     "patientId":patientId,
                     "id":baseinfo_id,
                     "address":self.address,
                     "telephone":telephone,
                     "socialId":self.socialId,
                     "socialAddress":self.socialAddress,
                     "nation":self.nation,
                     "isMarriage":self.isMarriage,
                     "homeAddress":self.homeAddress,
                     "workplace":self.workplace,
                     "spouseStatus":self.spouseStatus,
                     "childrenStatus":self.childrenStatus,
                     "fertility":self.fertility,
                     "marriageAge":self.marriageAge,
                     "isSmoke":self.isSmoke,
                     "isDrink":self.isDrink,
                     "isNarcotics":self.isNarcotics,
                     "parentStatus":self.parentStatus,
                     "siblingsStatus":self.siblingsStatus,
                     "isInfection":self.isInfection,
                     "isHeredopathia":self.isHeredopathia
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

#
# if __name__ == '__main__':
#     unittest.main()




