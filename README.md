# 特别说明：本库仅提供企业内部服务，不向外部提供商业性的数据服务和支持

dbpystream API 主要为已经购买了数据供应商API服务的企业内部提供向自己员工内部的数据服务的API接口，这种服务是一种API的镜像服务。

## dbpystream API的目的

对于不少企业来说，购买了很多不同类的数据，比如wind,同花顺，joinquant,财汇，聚源等等。很多是以账号的形式提供服务，也有部分是以落地数据库的形式。但这些形式，更多的只是提供给企业内部的局部人员使用，在数据共享和数据探索，以及服务上，还是处于一个相对窄的面上。对企业来讲，这些数据并没有得到全面的使用，也没有把数据信息资产化，并且流动起来，让业务产生更大的价值。

基于上面的痛点 ，dbpystream的目的是根据自身的业务需要，把企业内部的数据进行服务化，让企业内的员工能方便得到数据服务，而不再让数据服务只是一小部分人的特权，让数据可以在更广泛的层面得到充分的利用，并发挥数据驱动业务的价值。

从更长远的角度，数据的广泛利用，有利于在公司、行业层面发挥价值，同时也让大家更加重视数据的内在价值，也有利提升行业的生态环境。

## dbpystream API 的特点

1、函数基本一致。在接口规范上，尽量保持和原生的API接口相近，尽量让大家上手比较快,个别上函数签名和返回值上可能会有微调；
2、基于内部使用。 API的服务范围是基于内部的需要开发的实用接口部分，其要比原生API范围的小；
3、数据上“源汁源味"。数据上不对源数据做相应的清洗和加工。

## dbpystream API 与其它数据源API不同

1、定位不同。dbpystream是对内服务。

和供应商提供的API服务不同，dbpystream是对内的，更相对于是一个局域网。数据源API是对外赋能，dbpystream是对内赋能，而不是对外商业化。

2、上下游关系。dbpystream依赖于供应商的API服务。

供应商的API的服务质量是dbpystream的天花板，没有优秀的供应商服务（源头），就不可能有好的内部服务。

3、共生关系。dbpystream只做整合部分，不能替代供应商API，是对供应商API服务包装，为了让服务更好的落地，而供应商API做的是一套完整的生产和质量管理流程。

## dbpystream API展望

目前，data api 市场和服务还是较初级的阶段，感谢市场上为数不多的数据提供商，可以让大家有了接触api服务的可能。在此基础上，dbpystream api才有了二次的可能，在此特别致谢，joinquant, tushare、同花顺等数据服务厂商，也感谢为市场提供免费数据的sina财经等网站。

目前，dbpystream主要的数据服务商有：jqdatasdk, 未来计划支持更多。

dbpystream只对企业内部提供数据服务,也期待能与数据供应商一起为整个数据生态而努力！

## 安装方法

```python

    pip install dbpystream

```

## 实例说明

以下jqdatasdk为例，本库提供了jqdatasdk类似的支持，主要函数签名及参数基本上与jqdatasdk一致

其中，比如，你希望通过get_price获取历史1 min bar行情，首先，你需要在首次登陆时需要使用到auth函数。

auth:

```python
    def auth(username=None,password=None) -> None
```

说明：
    可以选择手动同时填入两个参数，也可以使用从环境变量中进行设置。默认是从环境变量中;如果从环境变量设置相关变量，建议以"dbpystream_username"，"dbpystream_password"来命名。
    当前面username和password参数必须显示指定和输入。这两个参数，需要由内部分发。

在完成登陆后，你就可以直接调用get_price函数了。

get_price:

```python
    def get_price(security,start_date,end_date,frequency,fq='pre',fields=None) -> pd.DataFrame:
```

关于get_price的用法：

```python
    其中主要参数：
    1、security 
        一支股票代码或者一个股票代码的list。股票代码或期货合约要包含交易后缀，比如.XSHE,XSHG等等。
    2、start_date
        与 count 二选一，不可同时使用. 字符串或者 datetime.datetime/datetime.date 对象, 开始时间.
    3、end_date
        格式同上, 结束时间, 默认是'2015-12-31', 包含此日期. 注意: 当取分钟数据时, 如果 end_date 只有日期, 则日内时间等同于   00:00:00, 所以返回的数据是不包括 end_date 这一天的.
    4、frequency
        'daily'(等同于'1d'), 'minute'(等同于'1m'),  默认值是daily
    5、fields：有3个选项:，
        (1) None :
            只支持['code','datetime','open', 'close', 'high', 'low', 'volume', 'money']
        (2)'all' : 即全选，
            是指[code","datetime","open","close","low","high","volume","money","factor","high_limit","low_limit","avg","pre_close","paused","open_interest"]
        (3)选取字段: 比如["datetime","open","close"]
            是指从"all"对应的字段全集中，选取所需要的参数组合。
    6、fq:，是指复权参数，其中,"pre"指前复权，"post"指后复权，None为不复权。
        共有'pre',"post",None三个选项；其中默认值为，"pre"。

    如,get_price("000005.XSHE", "2022-01-01", "2022-10-05", "minute", "post")
  
                datetime   open  close   high    low   volume      money
    1 2022-01-04 09:31:00  23.51  23.51  23.51  23.41  54328.0  1276801.0
    2 2022-01-04 09:32:00  23.51  23.41  23.51  23.41   6730.0   157603.0
    3 2022-01-04 09:33:00  23.41  23.41  23.41  23.41  13704.0   320829.0
    4 2022-01-04 09:34:00  23.41  23.41  23.41  23.41   5507.0   128928.0
```

## 整体调用参考代码

```python

    import pandas as pd 
    import dbpystream

    start_date = "2020-09-30" # 日期字符串格式
    end_date   = "2022-11-01" # 日期字符串格式
    frequency  = "minute" # daily
    fq         = "post" # pre:前复权[默认]，None
    auth() # 第一次调用，需要登陆一下
    codes = ["159707.XSHE"] #603619.XSHG,ZN2210.XSGE
    for security in codes:
        df  = get_price(security,start_date,end_date,frequency,fq) ## data为返回的是pd.dataframe格式的数据；
        print(f"code : {security} df shape : {df.shape} ")
        print(f"{df.head()}")

```

输出：

```python
code : 159707.XSHE df shape : (52320, 8)  
          code            datetime   open  close   high    low      volume       money
0  159707.XSHE 2021-11-12 09:31:00  1.010  1.008  1.010  1.007  22446600.0  22635524.0
1  159707.XSHE 2021-11-12 09:32:00  1.008  1.004  1.008  1.001   2566100.0   2574806.0
2  159707.XSHE 2021-11-12 09:33:00  1.005  1.007  1.008  1.005   5207000.0   5239605.0
3  159707.XSHE 2021-11-12 09:34:00  1.007  1.008  1.009  1.007   1583300.0   1596114.0
4  159707.XSHE 2021-11-12 09:35:00  1.005  1.006  1.007  1.005   4935000.0   4966423.0
```

这样，你就可以开始使用dbpystream了。

如果有任何问题，欢迎邮件至rustroom@163.com。
