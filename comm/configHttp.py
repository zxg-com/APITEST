import requests
import readConfig as readConfig
from comm.Log import MyLog as Log
import json

#定义对象调用ReadConfig.py中方法
localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, pchost,h5host, port, timeout,backhost
        #从config.ini中取值
        scheme = localReadConfig.get_http("scheme")
        pchost = localReadConfig.get_http("pcurl")
        h5host = localReadConfig.get_http("h5url")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        backhost = localReadConfig.get_http("backgroundurl")
        #log
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        #初始化
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.cookies={}
        self.state = 0
    #定义url拼接
    def set_pcurl(self, url):
        self.url = scheme+'://'+ pchost  +url

    def set_h5url(self, url):
        self.url = scheme+'://'+h5host +url

    def set_backgrounturl(self,url):
        self.url = 'http://'+backhost+url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data


    #图片文件
    def set_files(self, filename):
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # 定义get方法
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params,timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers,data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # json接口
    def postWithJson(self):
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

