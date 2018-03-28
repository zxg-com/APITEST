import os
import codecs
import configparser
import email

#当前项目路径
proDir = os.path.split(os.path.realpath(__file__))[0]

#定义路径
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()
        #初始化对象
        self.cf = configparser.ConfigParser()
        #读取配置文件
        self.cf.read(configPath)

    def get_email(self, name):
        #根据name读取内容
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):

        #存储headers
        self.cf.set("HEADERS", name, value)
        # 打开文件
        f = open(configPath, 'w+')
        #写入
        self.cf.write(f)
        f.close()


    def get_cookie(self, name):
        value = self.cf.get("COOKIE", name)
        return value

    def set_cookies(self, name, value):

        #存储headers
        self.cf.set("COOKIE", name, value)
        # 打开文件
        f = open(configPath, 'w+')
        #写入
        self.cf.write(f)
        f.close()

    def set_customer(self, name, value):

        #存储customer
        self.cf.set("CUSTOMER", name, value)
        # 打开文件
        f = open(configPath, 'w+')
        #写入
        self.cf.write(f)
        f.close()

    def get_customer(self,name):
        value=self.cf.get("CUSTOMER",name)
        return value

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db_huizhen(self, name):
        value = self.cf.get("DATABASE_huizhen", name)
        return value

    def get_db_weiyi(self, name):
        value = self.cf.get("DATABASE_allin", name)
        return value

    def get_case(self, name):
        value = self.cf.get("CASE", name)
        return value

    def set_case(self, name, value):

        #存储headers
        self.cf.set("CASE", name, value)
        # 打开文件
        f = open(configPath, 'w+')
        #写入
        self.cf.write(f)
        f.close()

    def get_patient(self, name):
        value = self.cf.get("PATIENT", name)
        return value

    def set_patient(self, name, value):

        #存储headers
        self.cf.set("PATIENT", name, value)
        # 打开文件
        f = open(configPath, 'w+')
        #写入
        self.cf.write(f)
        f.close()

    def get_im(self, name):
        value = self.cf.get("IM", name)
        return value

    def set_im(self, name, value):

        #存储headers
        self.cf.set("IM", name, value)
        # 打开文件
        f = open(configPath, 'w+')
        #写入
        self.cf.write(f)
        f.close()

    def get_doctor(self,name):
        value = self.cf.get("DOCTOR",name)
        return value

    def set_doctor(self,name,value):
        self.cf.set("DOCTOR",name,value)
        f=open(configPath,'w+')
        self.cf.write(f)
        f.close()
