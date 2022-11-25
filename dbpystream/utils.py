import uuid
import sys 
import pandas as pd
import pickle
import pyzstd
import os
from os import getenv
import dbpystream.method as method
import time as t

def get_username_from_env():
    value  = None
    for name in ["username", "user", "account", "mob"]:
        for prefix in ["dbpystream","dbpystreamapi","dbpystream_api","dbpystream_sdk"]:
            value = getenv('_'.join([prefix, name]).upper())
            if value:
                return value 
    return value        

def get_password_from_env():
    value =  None
    for name in ["password", "passwd","pwd"]:
        for prefix in ["dbpystream","dbpystreamapi","dbpystream_api","dbpystream_sdk"]:
            value = getenv('_'.join([prefix, name]).upper())
            if value:
                return value 
    return None
def get_account_info_from_env() -> dict:

    username = get_username_from_env()
    password = get_password_from_env()
    _dict = {"username":username,"password": password}
    return _dict

def get_mac_address() -> str:
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return f'{mac[0:2]}-{mac[2:4]}-{mac[4:6]}-{ mac[6:8]}-{mac[8:10]}-{mac[10:]}'

def parse_response_data(raw_data,decompress_mode ="zstd") -> pd.DataFrame :
    t0 = t.time()
    df = pd.DataFrame()
    #print(f"raw_data -> size : {sys.getsizeof(raw_data)} bytes! ")

    if not raw_data or isinstance(raw_data,str):
        print(f"response raw_data : {raw_data} is str! 或为空！")
        return df
    if decompress_mode =="zstd":
         _msg = pyzstd.decompress(raw_data)
    else :
        _msg = raw_data

    #print(f"decompress _msg -> size : {sys.getsizeof(_msg)} bytes! ")

    if raw_data :
        decompress_data = pickle.loads(_msg) # dict
        assert isinstance(decompress_data,dict),"parse_response_data解压后数据格式不是dict类型！"
        t1 = t.time()
        #print(f"parse_response_data [get_price] cost time：{t1-t0} ")    
        df   = pd.DataFrame(decompress_data)
    return df

   
def get_urls_from_methods(host) -> dict:
    _methods = method.get_methods()
    _urls = {}
    for _method in _methods:
        assert "url" in _methods[_method], "method.py文件中的url字段设置请确认是否正确!"
        url = host +_methods[_method]['url']
        _urls[_method] = url
    return _urls

def get_fields(cls):
    return  dir(cls)

def check_code(security_code) -> bool:

    if "." in security_code:
        code,exchange = security_code.split(".",1) 
        print(f"code : {code} exchange : {exchange}")
        if exchange not in ["XSHG","XSHE","CCFX","XDCE","XSGE","XZCE","XINE"]:

            return False
        else:
            if exchange in ["XSHG","XSHE"]:#股票交易所，沪深交易所

                return code.isdigit()     # str.isdigit() 判断所有字符都是数字
            elif exchange in ["CCFX","XDCE","XSGE","XZCE","XINE"]: #期货交易所

                return code.isalnum()     # str.isalnum() 判断所有字符是字母或数字两种构成
            else:
                return False # 北交所，新三板之类，债券市场
    else:

        return security_code.isalnum()    


def is_valid_date(date) -> bool:
    try:
        if ":" in date:
            t.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            t.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def check_get_price_params(params) ->bool:
    '''
    data : 
    {
        "security"  : "000005.XSHE", 
        "start_date": "2022-01-01", 
        "end_date"  : "2022-10-05", 
        "frequency" : "minute", 
        "fields"    : []
        "fq"        : "post","pre",None
    }
    '''
    is_all_valid = True 
    fields = ["code","datetime","open","close","low","high","volume","money","factor","high_limit","low_limit","avg","pre_close","paused","open_interest"]
    if not isinstance(params,dict):
        print("--------------------error-----------------------\n")
        print(f"params : {params} 不是dict类型！")
        print("--------------------error-----------------------\n")
        is_all_valid = False
    
    if  "start_date" in params and not is_valid_date(params["start_date"]):
        print("--------------------error-----------------------\n")
        print(f"start_date : {params['start_date']} 格式不对！")
        print("--------------------error-----------------------\n")
        is_all_valid = False
        
    if "end_date" in params and not  is_valid_date(params["end_date"]):
        print("--------------------error-----------------------\n")
        print(f"end_date : {params['end_date']} 格式不对！")
        print("--------------------error-----------------------\n")
        is_all_valid= False
    if "security" in params and isinstance(params["security"],str) and not check_code(params["security"]):
        print("--------------------error-----------------------\n")
        print(f"security : {params['security']} 请确认是否正确！")
        print("--------------------error-----------------------\n")
        is_all_valid= False
    if "frequency" in params and params["frequency"] not in ["minute","daily"]:
        print("--------------------error-----------------------\n")
        print(f"frequency : {params['frequency']} 请确认是否正确！")
        print("--------------------error-----------------------\n")
        is_all_valid= False
    # fields
    if "fields" in params and params["fields"] :
        for field in params["fields"] :
            if  field not in fields:
                print("--------------------error-----------------------\n")
                print(f"fields中字段 : {field} 不在指定fields {fields} 内！")
                print("--------------------error-----------------------\n")
                is_all_valid= False
                break
    
    if "fq" in params :
        if params["fq"] not in ["pre","post",None]:
            print("--------------------error-----------------------\n")
            print(f"fq 复权参数: {params['fq'] }!")
            print("--------------------error-----------------------\n")
            is_all_valid= False
    return is_all_valid

def check_all_securities_params(params)-> bool:
    """_summary_
      type: stock
      date: date
    """
    if "types" not in params :
        return False
    else:
        for _type in params["types"]:
            if _type not in ["stock","futures","etf","index"]:
                return False
    if "date" in params and not is_valid_date(params["date"]):
        return False
    return True

def check_index_weights_params(params) -> bool:
    """_summary_
      index_code: code
      date: date
    """
    print(f"params : {params}")
    if "index_id" not in params :
        return False

    if "date" in params and not is_valid_date(params["date"]):
        return False
    
    return True

def check_industry_stock_params(params) ->bool:
    """_summary_
      industry_code: code
      date: date
    """
    print(f"params : {params}")
    if "industry_code" not in params :
        return False

    if "date" in params and not is_valid_date(params["date"]):
        return False
    return True

def check_industry_params(params) -> bool:
    if "security" not in params :
        return False

    if "date" in params and not is_valid_date(params["date"]):
        return False
    return True

def check_trade_days_params(params) ->bool:

    if "start_date" in params and not is_valid_date(params["start_date"]):
        return False
    
    if "end_date" in params and not is_valid_date(params["start_date"]):
            return False
    return True

def check_all_trade_days_params() ->bool:
    return True
def check_security_info_params(params) ->bool:

    if "code" not in params or not check_code(params["code"]):
        return False
    return True

def check_index_stocks_params(params) ->bool:
    
    if "index_id" not in params :
            return False

    if "date" in params and not is_valid_date(params["date"]):
        return False
    
    return True
def check_method_params(params,method_name) -> bool : 

    if method_name == "get_price":
        return check_get_price_params(params)
    elif method_name == "get_all_securities":
        return check_all_securities_params(params)
    elif method_name =="get_index_weights":
        return check_index_weights_params(params)
    elif method_name == "get_industry":
        return check_industry_params(params)
    elif method_name == "get_industry_stocks":
        return check_industry_stock_params(params)
    elif method_name == "get_trade_days":
        return check_trade_days_params(params)
    elif method_name =="get_all_trade_days":
        return True
    elif method_name =="get_security_info":
        return check_security_info_params(params)
    elif method_name =="get_index_stocks":
        return check_index_stocks_params(params)
    else:
        return False
    
