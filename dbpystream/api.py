
import sys
import requests
import time as t
import pandas as pd

import dbpystream
from  dbpystream.client import LDClient

# 如果username和password都不选，表示会从环境变量中来取相关的账户和密码
def auth(username=None,password=None) -> None: 
    return LDClient.instance().auth(**locals())

# 获取历史数据，可查询多个标的多个数据字段，返回数据格式为 DataFrame
def get_price(security,start_date,end_date,frequency,fq='pre',fields=None) -> pd.DataFrame:
    return LDClient.instance().get_price(**locals())

    '''
    security: 一支股票代码或者一个股票代码的list
    start_date: 与 count 二选一，不可同时使用. 字符串或者 datetime.datetime/datetime.date 对象, 开始时间.
    end_date: 格式同上, 结束时间, 默认是'2015-12-31', 包含此日期. 注意: 当取分钟数据时, 如果 end_date 只有日期, 则日内时间等同于 00:00:00, 所以返回的数据是不包括 end_date 这一天的.
    frequency: 'daily'(等同于'1d'), 'minute'(等同于'1m'),  默认值是daily
    fields: 
     None  :只支持['code','datetime','open', 'close', 'high', 'low', 'volume', 'money']
     'all' : 全选，即[code","datetime","open","close","low","high","volume","money","factor","high_limit","low_limit","avg","pre_close","paused","open_interest"]
     list: all全部字段中选取部分字段，比如
    fq: 'pre',"post",None,默认值，"pre"

    get_price(["000005.XSHE"], "2022-01-01", "2022-10-05", "minute", "post")
    
                datetime   open  close   high    low   volume      money
    1 2022-01-04 09:31:00  23.51  23.51  23.51  23.41  54328.0  1276801.0
    2 2022-01-04 09:32:00  23.51  23.41  23.51  23.41   6730.0   157603.0
    3 2022-01-04 09:33:00  23.41  23.41  23.41  23.41  13704.0   320829.0
    4 2022-01-04 09:34:00  23.41  23.41  23.41  23.41   5507.0   128928.0

    '''

# 获取指定日期区间内的限售解禁数据
def get_locked_shares(stock_list, start_date, end_date, forward_count):
    return LDClient.instance().get_locked_shares(**locals())
    '''
    获取指定日期区间内的限售解禁数据

    参数

        stock_list: 一个股票代码的 list
        start_date: 开始日期
        end_date: 结束日期
        forward_count: 交易日数量， 可以与 start_date 同时使用， 表示获取 start_date 到 forward_count 个交易日区间的数据

    返回值

        pandas.DataFrame， 各 column 的含义如下:
            day: 解禁日期
            code: 股票代码
            num: 解禁股数
            rate1: 解禁股数/总股本
            rate2: 解禁股数/总流通股本

    示例

    # 在策略中获取个股未来500天的解禁情况
    get_locked_shares(stock_list=['000001.XSHE', '000002.XSHE'], start_date=context.current_dt, forward_count=500)
    '''

#获取指数成份股
def get_index_stocks(index_symbol, date=None)->list:
    return LDClient.instance().get_index_stocks(**locals())
    
    '''
    get_index_stocks(index_symbol, date=None)
    参数
    - index_symbol, 指数代码
    - date: 查询日期, 一个字符串(格式类似’2015-10-15’)或者[datetime.date]/[datetime.datetime]对象, 可以是None, 使用默认日期. 这个默认日…
    '''

#获取指数成分股权重
def get_index_weights(index_id, date=None) ->pd.DataFrame:
    return LDClient.instance().get_index_weights(**locals())
    '''
    参数

        index_id: 代表指数的标准形式代码， 形式：指数代码.交易所代码，例如"000001.XSHG"。
        date: 查询权重信息的日期，形式："%Y-%m-%d"，例如"2018-05-03"；date可以是None，当date=None时，返回最近一次更新的指数成份股权重。

    返回

        查询到对应日期，且有权重数据，返回 pandas.DataFrame， code(股票代码)，display_name(股票名称), date(日期), weight(权重)；
        查询到对应日期，且无权重数据， 返回距离查询日期最近日期的权重信息；
        找不到对应日期的权重信息， 返回距离查询日期最近日期的权重信息；
   
    '''

#获取行业板块成分股
def get_industry_stocks(industry_code, date=None) ->list:
    return LDClient.instance().get_industry_stocks(**locals())

    '''
    参数

        industry_code: 行业编码

        date: 查询日期, 一个字符串(格式类似’2015-10-15’)或者[datetime.date]/[datetime.datetime]对象, 可以是None, 使用默认日期. 这个默认日期在回测和研究模块上有点差别:

        回测模块: 默认值会随着回测日期变化而变化, 等于context.current_dt
        研究模块: 默认是今天

    返回

        返回股票代码的list
    '''


# 按照行业分类获取行业列表。
def get_industries(name, date=None) -> pd.DataFrame:
    return LDClient.instance().get_industries(**locals())
    '''
    # get_industries 获取行业列表
    from jqdata import *
    get_industries(name, date=None)

    按照行业分类获取行业列表。

    参数

        name: 行业代码， 取值如下：
            "sw_l1": 申万一级行业
            "sw_l2": 申万二级行业
            "sw_l3": 申万三级行业
            "jq_l1": 聚宽一级行业
            "jq_l2": 聚宽二级行业
            "zjw": 证监会行业

        date: 获取数据的日期，默认为None，返回历史上所有行业；传入date，返回date当天存在的行业；研究和回测中返回结果相同；

    返回值

        pandas.DataFrame， 各 column 的含义如下:
            index: 行业代码
            name: 行业名称
            start_date: 开始日期 

    示例

    from jqdata import *
    get_industries(name='zjw')
    get_industries(name='zjw', date='2016-01-01')
    '''

# 获取个股的所属行业数据
def get_industry(security, date=None) -> dict:
    return LDClient.instance().get_industry(**locals())
    '''
    参数
        security：标的代码。类型为字符串，形式如"000001.XSHE"；或为包含标的代码字符串的列表，形如["000001.XSHE", "000002.XSHE"]
        date：查询的日期。类型为字符串，形如"2018-06-01"或"2018-06-01 09:00:00"；或为datetime.datetime对象和datetime.date。注意传入对象的时分秒将被忽略。默认值为None，研究中默认值为当天，回测中默认值会随着回测日期变化而变化, 等于context.current_dt。
    返回结果
    一个dict， key是标的代码。
    示例
    >>> get_industry(security=['000001.XSHE','000002.XSHE'], date="2018-06-01")
    {'000001.XSHE': {'jq_l1': {'industry_code': 'HY007', 'industry_name': '金融指数'},
                    'jq_l2': {'industry_code': 'HY493', 'industry_name': '多元化银行指数'},
                    'sw_l1': {'industry_code': '801780', 'industry_name': '银行I'},
                    'sw_l2': {'industry_code': '801192', 'industry_name': '银行II'},
                    'sw_l3': {'industry_code': '851911', 'industry_name': '银行III'},
                    'zjw': {'industry_code': 'J66', 'industry_name': '货币金融服务'}
    参数

        security：标的代码，类型为字符串，形式如"000001.XSHE"；或为包含标的代码字符串的列表，形如["000001.XSHE", "000002.XSHE"]
        date：查询的日期。类型为字符串，形如"2018-06-01"或"2018-06-01 09:00:00"；或为datetime.datetime对象和datetime.date。注意传入对象的时分秒将被忽略。

    返回

    返回结果是一个dict，key是传入的股票代码

    示例

    #获取贵州茅台("600519.XSHG")的所属行业数据
    d = get_industry("600519.XSHG",date="2018-06-01")
    print(d)

    {'600519.XSHG': {'sw_l1': {'industry_code': '801120', 'industry_name': '食品饮料I'}, 'sw_l2': {'industry_code': '801123', 'industry_name': '饮料制造II'}, 'sw_l3': {'industry_code': '851231', 'industry_name': '白酒III'}, 'zjw': {'industry_code': 'C15', 'industry_name': '酒、饮料和精制茶制造业'}, 'jq_l2': {'industry_code': 'HY478', 'industry_name': '白酒与葡萄酒指数'}, 'jq_l1': {'industry_code': 'HY005', 'industry_name': '日常消费指数'}}}
    '''

# 获取所有标的信息
def get_all_securities(types=[], date=None) ->pd.DataFrame :
    return LDClient.instance().get_all_securities(**locals())
    '''
    获取平台支持的所有股票、基金、指数、期货、期权信息
    参数
        types: list: 用来过滤securities的类型, list元素可选: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof', 'fja', 'fjb', 'open_fund', 'bond_fund', 'stock_fund', 'QDII_fund'(QDII基金), 'money_market_fund', 'mixture_fund'。 types为空时返回所有股票, 不包括基金,指数和期货
        date: 日期, 一个字符串或者 datetime.datetime /datetime.date 对象, 用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息.建议使用时添加上指定date

    返回 [pandas.DataFrame], 比如:
    '''

# 获取单个标的信息

def get_security_info(code, date=None):
    return LDClient.instance().get_security_info(**locals())

    '''
        获取股票/基金/指数/期货的信息.
        参数
            code: 证券代码
            date：查询日期,默认为None，仅支持股票
        返回值
            一个对象, 有如下属性:
                display_name: 中文名称
                name: 缩写简称
                start_date: 上市日期, [datetime.date] 类型
                end_date: 退市日期（股票是最后一个交易日，不同于摘牌日期）， [datetime.date] 类型, 如果没有退市则为2200-01-01
                type: 股票、基金、金融期货、期货、债券基金、股票基金、QDII 基金、货币基金、混合基金、场外基金，'stock'/ 'fund' / 'index_futures' / 'futures' / 'etf'/'bond_fund' / 'stock_fund' / 'QDII_fund' / 'money_market_fund' / ‘mixture_fund' / 'open_fund'
                parent: 分级基金的母基金代码
        示例
        # 获取000001.XSHE的上市时间
        start_date = get_security_info('000001.XSHE').start_date
        print(start_date)
    '''


    '''
    参数
        security：标的代码。类型为字符串，形式如"000001.XSHE"；或为包含标的代码字符串的列表，形如["000001.XSHE", "000002.XSHE"]
        date：查询的日期。类型为字符串，形如"2018-06-01"或"2018-06-01 09:00:00"；或为datetime.datetime对象和datetime.date。注意传入对象的时分秒将被忽略。默认值为None，研究中默认值为当天，回测中默认值会随着回测日期变化而变化, 等于context.current_dt。
    返回结果
    一个dict， key是标的代码。
    示例
    >>> get_industry(security=['000001.XSHE','000002.XSHE'], date="2018-06-01")
    {'000001.XSHE': {'jq_l1': {'industry_code': 'HY007', 'industry_name': '金融指数'},
                    'jq_l2': {'industry_code': 'HY493', 'industry_name': '多元化银行指数'},
                    'sw_l1': {'industry_code': '801780', 'industry_name': '银行I'},
                    'sw_l2': {'industry_code': '801192', 'industry_name': '银行II'},
                    'sw_l3': {'industry_code': '851911', 'industry_name': '银行III'},
                    'zjw': {'industry_code': 'J66', 'industry_name': '货币金融服务'}
                    },
    '000002.XSHE': {'jq_l1': {'industry_code': 'HY011', 'industry_name': '房地产指数'},
                    'jq_l2': {'industry_code': 'HY509', 'industry_name': '房地产开发指数'},
                    'sw_l1': {'industry_code': '801180', 'industry_name': '房地产I'},
                    'sw_l2': {'industry_code': '801181', 'industry_name': '房地产开发II'},
                    'sw_l3': {'industry_code': '851811', 'industry_name': '房地产开发III'},
                    'zjw': {'industry_code': 'K70', 'industry_name': '房地产业'}
                    }
    }
    '''

def get_futures_info(securities=None, fields=('contract_multiplier','tick_size','trade_time')):
    return LDClient.instance().get_futures_info(**locals())
    
    '''
        infos = get_futures_info(["AG2012.XSGE",'A1609.XDCE' ])
        print(infos)
        >>>{'AG2012.XSGE': {'tick_size': 1.0, 
        'trade_time': [['2019-12-17', '2020-12-15', '21:00~02:30', '09:00~10:15', '10:30~11:30', '13:30~15:00']], 
        'contract_multiplier': 15.0}, 
        'A1609.XDCE': {'tick_size': 1.0, 
        'trade_time': [['2015-03-16', '2015-05-08', '21:00~02:30', '09:00~10:15', '10:30~11:30', '13:30~15:00'], 
        ['2015-05-09', '2016-09-14', '21:00~23:30', '09:00~10:15', '10:30~11:30', '13:30~15:00']],
        'contract_multiplier': 10.0}}
    '''

# get_all_trade_days 获取所有交易日
def get_all_trade_days():
    return LDClient.instance().get_all_trade_days(**locals())

    '''
    get_all_trade_days()

    获取所有交易日, 不需要传入参数, 返回一个包含所有交易日的 numpy.ndarray, 每个元素为一个datetime.date类型.

    注： 需导入 jqdata 模块，即在策略或研究起始位置加入

    '''
# get_trade_days 获取指定范围交易日

def get_trade_days(start_date=None, end_date=None, count=None):
    return LDClient.instance().get_trade_days(**locals())
    '''
    from jqdata import *
    get_trade_days(start_date=None, end_date=None, count=None)

    获取指定日期范围内的所有交易日, 返回一个包含datetime.date object的列表, 包含指定的 start_date 和 end_date, 默认返回至 datetime.date.today() 的所有交易日

    注意get_trade_days最多只能获取到截至现实时间的当前年份的最后一天的交易日数据

    注： 需导入 jqdata 模块，即在策略或研究起始位置加入
    import jqdata

    参数

        start_date: 开始日期, 与 count 二选一, 不可同时使用. str/datetime.date/datetime.datetime 对象
        end_date: 结束日期, str/datetime.date/datetime.datetime 对象, 默认为 datetime.date.today()
        count: 数量, 与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日，包含 end_date 当天。
    '''


