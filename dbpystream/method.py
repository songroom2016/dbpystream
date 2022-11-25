

def get_methods() -> dict:
    _METHODS = {}
    _get_price = {}
    _get_price["url"] ="/history_price"
    _get_price["params"] = ['code','start_date','end_date','freqence','security_type','fq_type','method_name']
    _get_price["comment"] ="获取证券/证券组合的历史 1min bar数据"
    _get_price["source"] ="jq"
    _get_price["return_type"] ="DataFrame"

    _auth = {}
    _auth["url"] ="/login"
    _auth["params"] =["username","password"]
    _auth["comment"] = "账户登陆"
    _auth["source"] ="dbpystream"
    _auth["return_type"] =""

    _get_security_info ={}
    _get_security_info["url"] ="/security_info"
    _get_security_info["params"] =[]
    _get_security_info["comment"] ="获取单支股票的信息"
    _get_security_info["source"] ="jq"
    _get_security_info["return_type"] ="DataFrame"


    _get_futures_info ={}
    _get_futures_info["params"] =[]
    _get_futures_info["url"] ="/futures_info"
    _get_futures_info["comment"] ="获取单个期货的信息"
    _get_futures_info["source"] ="jq"
    _get_futures_info["return_type"] ="DataFrame"

    _get_index_weights= {}
    _get_index_weights["params"] =[]
    _get_index_weights["url"] ="/index_weights"
    _get_index_weights["comment"] ="获取指数权重的信息"
    _get_index_weights["source"] ="jq"
    _get_index_weights["return_type"] ="DataFrame"


    _get_all_securities={}
    _get_all_securities["url"] ="/all_securities"
    _get_all_securities["params"] =[]
    _get_all_securities["comment"] ="获取平台支持的所有证券清单数据 [stock,fund,futures]"
    _get_all_securities["source"] ="jq"
    _get_all_securities["return_type"] ="DataFrame"

    _get_index_stocks={}
    _get_index_stocks["url"] ="/index_stocks"
    _get_index_stocks["params"]=[]
    _get_index_stocks["comment"] ="获取指数成份股"
    _get_index_stocks["source"] ="jq"
    _get_index_stocks["return_type"] ="DataFrame"

    _get_trade_days={}
    _get_trade_days["url"] = "/trade_days"
    _get_trade_days["params"] =[]
    _get_trade_days["comment"] ="获取指数成份股"
    _get_trade_days["source"] ="jq"
    _get_trade_days["return_type"] ="list"

    _get_all_trade_days ={}
    _get_all_trade_days["url"] ="/all_trade_days"
    _get_all_trade_days["params"]=[]
    _get_all_trade_days["comment"] ="获得所有交易日"
    _get_all_trade_days["source"] ="jq"
    _get_all_trade_days["return_type"] ="list"

    _get_industry={}
    _get_industry["url"] ="/stock_industry"
    _get_industry["params"] ="/industry"
    _get_industry["comment"] ="查询单支股票所属行业"
    _get_industry["source"] ="jq"
    _get_industry["return_type"] ="DataFrame"
    
    _get_industry_stocks={}
    _get_industry_stocks["url"] ="/industry_stocks"
    _get_industry_stocks["params"] ="/industry_stocks"
    _get_industry_stocks["comment"] ="查询某行业的成份股"
    _get_industry_stocks["source"] ="jq"
    _get_industry_stocks["return_type"] ="DataFrame"


    _get_locked_shares = {}
    _get_locked_shares["url"] ="/locked_shares"
    _get_locked_shares["params"] =[]
    _get_locked_shares["comment"] ="获取指定日期区间内的限售解禁数据"
    _get_locked_shares["source"] ="jq"
    _get_locked_shares["return_type"]="DataFrame"


    _METHODS["auth"] = _auth
    _METHODS["get_price"] =_get_price
    _METHODS["get_security_info"] =_get_security_info
    _METHODS["get_futures_info"] = _get_futures_info
    _METHODS["get_index_weights"] =_get_index_weights
    _METHODS["get_all_securities"] = _get_all_securities
    _METHODS["get_index_stocks"] =_get_index_stocks
    _METHODS["get_trade_days"] = _get_trade_days
    _METHODS["get_all_trade_days"] =_get_all_trade_days
    _METHODS["get_industry_stocks"] = _get_industry_stocks
    _METHODS["get_industry"] = _get_industry
    _METHODS["get_locked_shares"] =_get_locked_shares
    
    return _METHODS

def get_exchanges() ->dict:
    _EXCHANGES = {}
    _sh_stock={}
    _sh_stock["code"] =".XSHG"

    _sz_stock={}
    _sz_stock["code"] =".XSHE"

    _cffex_futures = {}
    _cffex_futures["code"] =".CCFX"

    _dce_futures ={}
    _dce_futures["code"] ="XDCE"

    _sh_futures ={}
    _sh_futures["code"] =".XSGE"

    _zce_futures ={}
    _zce_futures["code"] =".XZCE"

    _sh_energy={}
    _sh_energy["code"] =".XINE"

    _gz_futures ={}
    _gz_futures["code"] ="" #待定

    _EXCHANGES["sh_stock"] = _sh_stock
    _EXCHANGES["sz_stock"] =_sz_stock
    _EXCHANGES["sh_futures"] = _sh_futures
    _EXCHANGES["sh_energy"] = _sh_energy
    _EXCHANGES["zce_futures"] =_zce_futures

    _EXCHANGES["dce_futures"] =_dce_futures
    _EXCHANGES["cffex_futures"] = _cffex_futures
    return _EXCHANGES


#交易市场 	代码后缀 	示例代码 	证券简称
#上海证券交易所 	.XSHG 	600519.XSHG 	贵州茅台
#深圳证券交易所 	.XSHE 	000001.XSHE 	平安银行
#中金所 	.CCFX 	IC9999.CCFX 	中证500主力合约
#大商所 	.XDCE 	A9999.XDCE 	豆一主力合约
#上期所 	.XSGE 	AU9999.XSGE 	黄金主力合约
#郑商所 	.XZCE 	CY8888.XZCE 	棉纱期货指数
#上海国际能源期货交易所 	.XINE 	SC9999.XINE 	原油主力合约
#场外基金 	.OF 	398051.OF 	中海环保新能源混合
# 北京交易所  ---待定
# 广州交易所  ---待定

