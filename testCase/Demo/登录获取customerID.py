'''

    #登录时获取customerId
    info={}
    info = response.json()
    customer_id = info['responseObject']['responseMessage']['userId']
    ReadConfig.set_customer("customerid", customer_id)
    #获取配置文件中customerID
    s = ReadConfig.get_customer('customerid')

'''