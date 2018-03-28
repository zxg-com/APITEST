import pymysql
import readConfig as readConfig
from comm.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class MyDB:
    global host, username, password, port, database, config,cursor
    #从config.ini取数据库相关参数值
    host = localReadConfig.get_db_huizhen("host")
    username = localReadConfig.get_db_huizhen("username")
    password = localReadConfig.get_db_huizhen("password")
    port = localReadConfig.get_db_huizhen("port")
    database = localReadConfig.get_db_huizhen("database")

    #配置内容已dic记录
    config = {
        'host': str(host),
        'user': username,
        'passwd': password,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        #启log
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectDB(self):   #链接数据库

        try:
            # 连接数据库
            self.db = pymysql.connect(**config)  #连接  **将config参数变为（a=1,b=2）
            # 创建光标
            self.cursor = self.db.cursor()
            print("数据库链接成功!")
        except ConnectionError as ex:
            self.logger.error(str(ex))
            print("数据库连接错误")



    def executeSQL(self,sql, params):   #执行语句
        #连接db
        MyDB.connectDB(self)
        # 执行sql
        self.cursor.execute(sql, params)
        # 执行sql提交到数据库
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):

        value = cursor.fetchall()   #获取所有查询结果
        return value

    def get_one(self, cursor):
        #执行完毕后取结果
        value = cursor.fetchone() #获取单个结果
        return value

    def closeDB(self):     #关闭链接
         #执行完毕关闭db
        self.db.close()
        print("数据库关闭")

