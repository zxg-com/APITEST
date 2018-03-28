'''
# ---------------------存cookie--------------
response = ConfigHttp.post()
s = response.cookies
# 将jar包形式cookie 转换为字典dict
cookies = requests.utils.dict_from_cookiejar(s)
# 存入cookie进配置文件
ReadConfig.set_cookies("JSESSIONID", cookies["JSESSIONID"])
ReadConfig.set_cookies("SPRING_SECURITY_REMEMBER_ME_COOKIE", cookies["SPRING_SECURITY_REMEMBER_ME_COOKIE"])


#-------------------获取cookie------------------
    j = ReadConfig.get_cookie("jsessionid")
    c = ReadConfig.get_cookie("spring_security_remember_me_cookie")
    cookie = "JSESSIONID=" + j + "; SPRING_SECURITY_REMEMBER_ME_COOKIE=" + c
'''