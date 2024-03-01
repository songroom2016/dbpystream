import requests
import time as t
import json
import pandas as pd

import itertools
import random
import toml
import sys
import dbpystream
import dbpystream.utils as utils
import threading
from requests.exceptions import RequestException


class LDClient(object):

    _threading_local = threading.local() 
    _auth_params = {}  
    _token = None
    _host  = "http://47.122.40.16" 
    _port  = 8080 
    _urls = utils.get_urls_from_methods(_host)
    _request_id_generator = itertools.count(random.choice(range(0, 100000, 100)))
    
    def __init__(self,username,password) -> None:

        self.client = None
        self.username = username
        self.password = password
        

    def get_login_header(self) -> dict:
        return {"Content-Type":"application/json"}

    def get_query_headers(self) -> dict:
        if self._token:
            headers = {"Content-Type": "application/json",
                "Authorization": self._token,
                "mac": utils.get_mac_address(),
                "request_id": str(next(self._request_id_generator)),
                "lang":"python",
                "compression":"zstd",
                }
            return headers
        else:
            raise Exception("token:为空，请确认账户和密码是否正确 或登陆是否正常！")
    
   
    def get_method_url(self,method):
        assert method in self._urls,f"{method} 不在{self._urls}中！"
        return self._urls[method]

       
    def get_login_params(self) -> bytes:
       mac = utils.get_mac_address()
       request_id = str(next(self._request_id_generator))
       params = {"username":self._auth_params["username"],"password":self._auth_params["password"],"mac":mac,"request_id":request_id}
       js_params = json.dumps(params)
       return js_params

    def get_token(self) -> str:
        url = self.get_method_url("auth")
        #print(f" url -> : {url}")
        headers = self.get_login_header()
        _params = self.get_login_params()
        token =""
        try:
            response = requests.post(url,data = _params,headers = headers)# params 
        except RequestException as e:
            raise Exception(f"get_token -> 请求出现异常，具体原因：{str(e)}")
        except Exception as e:  
            raise Exception(f"get_token -> 系统出现异常，具体原因 :{str(e)}")
        else:
            if response.status_code == 200:
                token = response.text
            else:
                _str_msg = f'get_token -> 请求错误：{str(response.status_code)} 原因：{str(response.reason)}'
                raise Exception(_str_msg)
        return token
    
    
    @classmethod
    def auth(cls,**params) : 
        cls.set_auth_params(**params)
        token = cls.instance().get_token()
        if token :
            cls.set_token(token)
            print("登陆成功！")
        else:
            raise Exception("登陆失败！请确认账户和密码是否正确！")
    
    @classmethod
    def set_token(cls,token) -> None:
        if token:
            cls._token = token

    @classmethod
    def set_auth_params(cls, **params):
        if params != cls._auth_params and cls.instance():
            cls._threading_local._instance = None
        #login(username=None,password=None,from_env =True) -> None: 
        if params["username"] and params["password"]: # 即有账户，又有密码
            cls._auth_params = params 
        else:
            params = utils.get_account_info_from_env()
            assert params["username"] and  params["password"],"从环境变量中没有取到相应的账户和密码！请确认是否已设置正确！或在auth函数中输入账户和密码！"
            cls._auth_params = params
    
    @classmethod
    def instance(cls):
        _instance = getattr(cls._threading_local, '_instance', None)
        if _instance is None:
            if not cls._auth_params:
                params =  utils.get_account_info_from_env()
                cls._auth_params = params
              
            if cls._auth_params:
                _instance = LDClient(**cls._auth_params) ##初始化
                cls._threading_local._instance = _instance
        return _instance

    def __call__(self, method, **kwargs):

        return self.query(method, kwargs)
        print('query ok!')

    def  __getattr__(self, method):
        return lambda **kwargs: self(method, **kwargs)
       
    def query(self,method_name,params) -> pd.DataFrame:
        url = self.get_method_url(method_name)
        #print(f"query -> url :  {url} ")
        headers = self.get_query_headers()
        data = json.dumps(params) ## 不能少
        #print(f"query -> data : {data} method_name: {method_name}")
        
        assert utils.check_method_params(params,method_name),"请确认该函数是否上线、或输入参数顺序或参数设置是否正确！"
        #print(f"query     :  -> token : {self.token} auth_params :{self._auth_params}")
        #print(f"headers   :  {headers}")
        
        df = pd.DataFrame()
        try:
            response = requests.post(url,data = data,headers = headers) 
        except RequestException as e:
            print(f"请求出现异常，具体原因：{str(e)}")
        except Exception as e:  
            print("系统出现异常，具体原因 :{str(e)}")
        else:
            if response.status_code == 200:
                result = response.content
                df = utils.parse_response_data(result)
            else:
                print(f'请求错误：{str(response.status_code)} 原因：{str(response.reason)}')
        return df
 








