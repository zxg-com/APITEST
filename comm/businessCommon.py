from comm import common
from comm import configHttp
import readConfig as readConfig
from comm.Log import MyLog
import requests
from comm import configDB
import re
import os
import base64

ReadConfig = readConfig.ReadConfig()
ConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls("pc.xlsx", "login")
db=configDB.MyDB

# login
def login():
    """
    login
    :return: token
    """
    # set url登录
    url = common.get_url_from_xml('login')
    ConfigHttp.set_pcurl(url)
    # set header

    # set data
    data = {'j_username': "website;" + localLogin_xls[0][3] + ";" + localLogin_xls[0][4] + ";mobile",
            'j_password': localLogin_xls[0][4],
            'rememberMe': "true"
            }
    #print(data)
    ConfigHttp.set_data(data)

    # login
    response = ConfigHttp.post()
    info = response.json()
    #print(response.text)
    s=response.cookies
    cookies=requests.utils.dict_from_cookiejar(s) #cookie 转字典
    ReadConfig.set_cookies("JSESSIONID",cookies["JSESSIONID"])
    ReadConfig.set_cookies("SPRING_SECURITY_REMEMBER_ME_COOKIE",cookies["SPRING_SECURITY_REMEMBER_ME_COOKIE"])
    if info['responseObject']['responseStatus'] == True:
        print("登录成功")
    else:
        print(info['responseObject']['responseMessage'])

def getwebuser():
    #set url getwebuser
    url=common.get_url_from_xml('getWebUser')
    ConfigHttp.set_pcurl(url)
    #读cookie
    j = ReadConfig.get_cookie("jsessionid")
    c = ReadConfig.get_cookie("spring_security_remember_me_cookie")
    cookie = "JSESSIONID=" +j+"; SPRING_SECURITY_REMEMBER_ME_COOKIE="+ c
    #print(cookie)
    headers = {'Cookie':cookie}  #cookie放入header中传输
    # print

    ConfigHttp.set_headers(headers)
    response=ConfigHttp.post()
    #print(response.json())
    info=response.json()
    customer_id=info['responseObject']['responseMessage']['userId']
    trueName = info['responseObject']['responseMessage']['trueName']
    #存入congif
    ReadConfig.set_customer("customerid",customer_id)
    ReadConfig.set_customer("customername",trueName)



# logout
def logout():

    # set url
    url = common.get_url_from_xml('logout')
    ConfigHttp.set_pcurl(url)

    # set header
    data = {'paramJson': "undefined"}
    #读cookie
    j = ReadConfig.get_cookie("jsessionid")
    c = ReadConfig.get_cookie("spring_security_remember_me_cookie")
    cookie = "JSESSIONID=" +j+"; SPRING_SECURITY_REMEMBER_ME_COOKIE="+ c
    #print(cookie)
    headers = {'Cookie':cookie}
    # print(cookies)
    ConfigHttp.set_data(data)

    # logout
    response=ConfigHttp.post()
    #print(response.text)


def  h5_Rigistsendcode(self,mobile):

    url = common.get_url_from_xml('h5_sendcode')
    ConfigHttp.set_h5url(url)
    #data
    paramJson = {"userType":1,"account":str(mobile),"accountType":0,"siteId":21}
    data = {'paramJson' : str(paramJson)}
    ConfigHttp.set_data(data)
    #post
    return_json = ConfigHttp.post()
    info = return_json.json()
    #存codeid
    # ReadConfig.set_patient('codeid', info['responseObject']['responsePk'])
    # print("请求验证码返回值："+return_json.text)
    codeid=info['responseObject']['responsePk']
    #从数据库中取验证码
    sql = common.get_sql('tocure_platform', 'tocure_customer_send_code', 'select_code')
    #print(sql)
    # sql参数化
    result = db.executeSQL(self, sql=sql, params=mobile)
    s = db.get_one(self, result)  # 返回结果eg.（'1234'，）
    db.closeDB(self)
    code = re.findall(r"'(.+?)'", str(s))[0]  # 正则取验证码  findall返回元祖，取第一个元素
    # ReadConfig.set_patient('code', code)
    # print("验证码为："+result)
    return codeid,code

# def  h5_Fastlogincode(self,mobile):
#     url = common.get_url_from_xml('h5_sendcode')
#     ConfigHttp.set_h5url(url)
#     #data
#     paramJson = {"userType":1,"account":str(mobile),"accountType":0,"operateType":8,"codeLength":4,"siteId":21,"typeId":3}
#     data = {'paramJson' : str(paramJson)}
#     ConfigHttp.set_data(data)
#     return_json = ConfigHttp.post()
#     info = return_json.json()
#     # 存codeid
#     # ReadConfig.set_patient('codeid', info['responseObject']['responsePk'])
#     # print("请求验证码返回值："+return_json.text)
#     codeid = info['responseObject']['responsePk']
#     # 从数据库中取验证码
#     sql = common.get_sql('tocure_platform', 'tocure_customer_send_code', 'select_code')
#     # print(sql)
#     # sql参数化  执行语句
#     result = db.executeSQL(self, sql=sql, params=mobile)
#     s = db.get_one(self, result)  # 返回结果eg.（'1234'，）
#     db.closeDB(self)
#     code = re.findall(r"'(.+?)'", str(s))[0]  # 正则取验证码  findall返回元祖，取第一个元素
#     # ReadConfig.set_patient('code', code)
#     # print("验证码为："+result)
#     return codeid, code

#
# def  h5_restpasswdcode(self,mobile):
#     url = common.get_url_from_xml('h5_sendcode')
#     ConfigHttp.set_h5url(url)
#     #data
#     paramJson = {"userType":1,"account":str(mobile),"accountType":0,"operateType":3,"codeLength":4,"siteId":21,"typeId":1}
#     data = {'paramJson' : str(paramJson)}
#     ConfigHttp.set_data(data)
#     return_json = ConfigHttp.post()
#     info = return_json.json()
#     # 存codeid
#     # ReadConfig.set_patient('codeid', info['responseObject']['responsePk'])
#     # print("请求验证码返回值："+return_json.text)
#     codeid = info['responseObject']['responsePk']
#     # 从数据库中取验证码
#     sql = common.get_sql('tocure_platform', 'tocure_customer_send_code', 'select_code')
#     # print(sql)
#     # sql参数化
#     result = db.executeSQL(self, sql=sql, params=mobile)
#     s = db.get_one(self, result)  # 返回结果eg.（'1234'，）
#     db.closeDB(self)
#     code = re.findall(r"'(.+?)'", str(s))[0]  # 正则取验证码  findall返回元祖，取第一个元素
#     # ReadConfig.set_patient('code', code)
#     # print("验证码为："+result)
#     return codeid, code

def  h5_changemobilecode(self,mobile):
    url = common.get_url_from_xml('h5_sendcode')
    ConfigHttp.set_h5url(url)
    #data
    paramJson = {"typeId":2,"accountType":0,"siteId":21,"userType":1,"operateType":2,"account":str(mobile),"codeLength":4}
    data = {'paramJson' : str(paramJson)}
    ConfigHttp.set_data(data)
    return_json = ConfigHttp.post()
    info = return_json.json()
    # 存codeid
    # ReadConfig.set_patient('codeid', info['responseObject']['responsePk'])
    print("请求验证码返回值："+return_json.text)
    codeid = info['responseObject']['responsePk']
    # 从数据库中取验证码
    sql = common.get_sql('tocure_platform', 'tocure_customer_send_code', 'select_code')
    # print(sql)
    # sql参数化
    result = db.executeSQL(self, sql=sql, params=mobile)
    s = db.get_one(self, result)  # 返回结果eg.（'1234'，）
    db.closeDB(self)
    code = re.findall(r"'(.+?)'", str(s))[0]  # 正则取验证码  findall返回元祖，取第一个元素
    # ReadConfig.set_patient('code', code)
    # print("验证码为："+result)
    return codeid, code


#无效H5账号
def deleteAccount(mobile):
    #后台查询账号id
    selecturl=common.get_url_from_xml('selectAccount')
    ConfigHttp.set_backgrounturl(selecturl)
    #data
    queryJson={"mobile": mobile, "sortType": "1"}
    data={ "queryJson":str(queryJson),
           "_search": "false",
           "rows": "10",
           "page": "1",
           "sort": "id",
           "order": "desc"}

    ConfigHttp.set_data(data)
    return_json=ConfigHttp.post()
    info = return_json.json()
    id= info['rows'][0]['id']
    nickname = info['rows'][0]['nickname']
    email = info['rows'][0]['email']
    siteId=info['rows'][0]['siteId']
    customerId=info['rows'][0]['customerId']
    # print(return_json.text)

    #无效患者账号
    url= common.get_url_from_xml('deleteAccount')
    ConfigHttp.set_backgrounturl(url)
    #data
    queryJson1={"id": id, "customerId": customerId, "nickname": nickname, "mobile": mobile, "email": email,
                "customerType": "0", "siteId": siteId, "isValid": "0"}
    data1 = {"queryJson":str(queryJson1)}
    ConfigHttp.set_data(data1)
    result = ConfigHttp.post()
    # print(result.url)
    print("无效账号请求返回值"+result.text)



# def h5_login():
#     url=common.get_url_from_xml('h5_login')
#     ConfigHttp.set_h5url(url)
#     #data
#     mobile = ReadConfig.get_patient('mobile')
#     password = ReadConfig.get_patient('password')
#     paramJson={"siteId":21,"account":mobile,"password":password}
#     data={'paramJson':str(paramJson)}
#     ConfigHttp.set_data(data)
#     return_json=ConfigHttp.post()
#     info=return_json.json()
#
#     customer_id=info['responseObject']['responseData']['customerId']
#     # print(customer_id)
#     ReadConfig.set_patient('patient_customerid',str(customer_id))
#     if info['responseObject']['responseStatus'] == True:
#         print("登录成功")
#     else:
#         print(info['responseObject']['responseMessage'])

def h5_logout():
    url=common.get_url_from_xml('h5_logout')
    ConfigHttp.set_h5url(url)
    #data
    paramJson={}
    data={"paramJson": str(paramJson)}
    ConfigHttp.set_data(data)
    return_json=ConfigHttp.post()
    info = return_json.json()
    if info['responseObject']['responseStatus'] == True:
     print("退出登录成功")
    else:
     print(info['responseObject']['responseMessage'])


def uploadPic(picName):
    url = common.get_url_from_xml('h5_getpicurl')
    ConfigHttp.set_h5url(url)
    #data
    # 截取格式
    type = picName.split('.')[1]
    # 路径定义
    picDir = os.path.join(readConfig.proDir, "testFile", "img", picName)
    # 图片base64处理
    # 打开文件
    f = open(picDir, 'rb')
    # base64加密
    content = base64.b64encode(f.read())
    # 解密为字符串
    content_str = content.decode('utf-8')
    f.close()
    # print(content)

    paramJson = {"fileContent": content_str,
                 "fileName": picName,
                 "extName": type,
                 "caseId": "",
                 "imageType": 0,
                 "caseCategoryId": ""
                 }
    data = {
        'paramJson': str(paramJson)
    }
    ConfigHttp.set_data(data)
    return_json=ConfigHttp.post()
    print("上传图片结果"+return_json.text)
    info=return_json.json()
    picurl=info['responseObject']['responseData']['logoUrl']
    id= info['responseObject']['responsePk']
    return id,picurl