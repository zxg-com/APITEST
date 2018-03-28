#coding=utf-8
import os
import unittest
from comm.Log import MyLog as Log
import readConfig as readConfig
from comm import HTMLTestReportCN
from comm.sentemail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        #on_off = localReadConfig.get_email("on_off") #on 发送给开发  off不发报告
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")   #用例汇总
        self.caseFile = os.path.join(readConfig.proDir, "testCase")  #用例路径
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        #取case列表文件caselist中的用例列表
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        print("用例数量%d" % len(self.caseList))
        fb.close()


    def set_case_suite(self):
        #用例组件
        self.set_case_list() #汇总case，形成组件
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print(case_name+".py")
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            #discover = unittest.defaultTestLoader.discover(self.caseFile, pattern='H5/Ad/getadlist.py', top_level_dir=None)
            suite_module.append(discover)
        print(suite_module)

        # for testsuite in  discover:
        #     for test_case in  testsuite:
        #         test_suite.addTest(test_case)

        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
            # print(test_suite)
        else:
            return None
        return test_suite



    def run(self):
        fp = open(resultPath, 'wb')
        try:
            suit = self.set_case_suite() #跑casesuite

            if suit is not None:
                logger.info("********开始测试********")
                fp = open(resultPath, 'wb')
                #报告生成
                runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)  #执行suite
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********测试 结束*********")
            fp.close()
            # 发邮件
            #self.email.send_email()



if __name__ == '__main__':
    obj = AllTest()
    obj.run()
