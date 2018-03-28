import requests
import readConfig as readConfig
import os
from xlrd import open_workbook  #操作Excel文件
from xml.etree import ElementTree as ElementTree   #根据不同参数取得xml文件中的内容
import json
from comm.Log import MyLog as Log
from comm import configHttp as ConfigHttp

localReadConfig = readConfig.ReadConfig()
#获取当前路径
proDir = readConfig.proDir
localConfigHttp = ConfigHttp.ConfigHttp()
#启动log

log = Log.get_log()
logger = log.get_logger()

caseNo = 0

#获取toen
# def get_visitor_token():
#
#     host = localReadConfig.get_http("BASEURL")
#     response = requests.get(host+"/v2/User/Token/generate")
#     info = response.json()
#     token = info.get("info")
#     logger.debug("Create token:%s" % (token))
#     return token

#存token到config.ini
# def set_visitor_token_to_config():
#
#     token_v = get_visitor_token()
#     localReadConfig.set_headers("TOKEN_V", token_v)


# def get_value_from_return_json(json, name1, name2):
#
#     info = json['info']
#     group = info[name1]
#     value = group[name2]
#     return value

#返回值显示
def show_return_msg(response):

    url = response.url
    msg = response.text
    print("\n请求地址："+url)
    # 可以显示中文
    print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))

# ****************************** read testCase excel文件 ********************************


def get_xls(xls_name, sheet_name):

    cls = []
    # xls 路径
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # 打开表格
    file = open_workbook(xlsPath)
    # 通过sheet名称获取表内容
    sheet = file.sheet_by_name(sheet_name)
    # 逐行获取内容
    nrows = sheet.nrows
    cols = sheet.ncols
    for i in range(nrows):
        #首行不获取
        if sheet.row_values(i)[0] != u'case_name':

            #for i in range(1, nrows):  # 指定从1开始，到最后一列，跳过表头
             cls.append(sheet.row_values(i))
    return cls


# ****************************** read SQL xml文件 ********************************
#数据库字典声明为空
database = {}
#遍历xml中sql语句
def set_xml():

    if len(database) == 0:
        #取sql.xml文件路径
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        #打开xml文件
        tree = ElementTree.parse(sql_path)
        #查找database字段
        for db in tree.findall("database"):
            #查找后获取name
            db_name = db.get("name")

            table = {}
            #查找db的子元素table
            for tb in db.getchildren():
                #获取表名字
                table_name = tb.get("name")

                sql = {}
                #从表中再查询sql元素
                for data in tb.getchildren():
                    #获取sql——id
                    sql_id = data.get("id")
                    #根据id取sql语句内容
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table

#根据数据库名、表名查数据
def get_xml_dict(database_name, table_name):
    #找到对应数据
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):

    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql

# ****************************** read interfaceURL xml文件 ********************************

#获取接口连接地址url
def get_url_from_xml(name):

    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')  #定义路径
    tree = ElementTree.parse(url_path)   #定义xml操作对象
    for u in tree.findall('url'):   #查找所有的url标签
        url_name = u.get('name')  #获取所有的name
        if url_name == name:      #存在改name
            for c in u.getchildren():   #取出url
                url_list.append(c.text)

    url = '/'.join(url_list)  #以/来拼接url_list中的元素 a/b/c
    return url

# if __name__ == "__main__":
#     print(get_xls("login"))
#     set_visitor_token_to_config()
