# dbpystream 说明 
特别说明：本库仅提供企业内部服务，不向外部提供商业性的数据服务和支持

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

## python sdk 实例说明

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

## python sdk 整体调用参考代码

```python

    import pandas as pd 
    import dbpystream.api as db

    start_date = "2020-09-30" # 日期字符串格式
    end_date   = "2022-11-01" # 日期字符串格式
    frequency  = "minute" # daily
    fq         = "post" # pre:前复权[默认]，None
    db.auth() # 第一次调用，需要登陆一下，这里默认从环境变量中已经设置好；或者db.auth("********","******")的显示设置账户和密码的方式。
    codes = ["159707.XSHE"] #603619.XSHG,ZN2210.XSGE
    for security in codes:
        df  = db.get_price(security,start_date,end_date,frequency,fq) ## data为返回的是pd.dataframe格式的数据；
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

## web api使用提醒
本数据服务提供现成sdk模式服务，同时支持restful api调用。但需要注意：

- 可以在headers中提供"compression"字段，可选为"gzip"和"zstd".默认为"gzip"。如果需要更好的性能，可选"zstd"，但是需要进行相应的zstd模式下的解压。
- 可以在headers中提供"lang"字段，可填写"python","rust","julia"等任何语言信息。如果填写"python"或不提供此字段，此默认前端为python语言调用，此时，前端需要进行pickle反序列化处理。


## python web api模式
```python
# 具体代码略，以下为主要关键流程代码,不是全部代码【特别说明】
import requests
import pyzstd
import pandas as pd

df = pd.DataFrame()
response = requests.post(url,data = data,headers = headers) 
result = response.content #得到服务端传过来的zstd压缩后的字节流文件 
_msg = pyzstd.decompress(result) #默认是zstd方式解压
decompress_data = pickle.loads(_msg) # 需要通过pickle来反序列化，得到dict
df   = pd.DataFrame(decompress_data) # 生产datafram

```

## julia web api 模式
```julia
# 注意headers中lang和compression字段的设置
using HTTP;
using JSON;
using CodecZstd; 

token = get_token();
println("获得token : {}",token);
println("请等待获取数据......");
codes = get_all_securities(token,"stock","2021-02-01")
@time data = get_price(token)
println("数据如下：",data);

function get_token()
    login_url ="http://47.122.40.16/login";
    username ="***********" #据实填写，下同
    password ="**********"
    params= Dict("username" => username,"password" =>password)
    res = HTTP.post( login_url, body=JSON.json(params))
    text = String(res.body)
    return text 
end
function get_price(token)
    get_price_url  ="http://47.122.40.16/history_price";
    headers = Dict("Content-Type"=>"application/json","Authorization"=>token,"lang" =>"julia","compression"=>"zstd") ## 可以选择两种压缩方式
    params  = Dict("security" => "600036.XSHG",
    "start_date"=> "2021-01-01",
    "end_date"=>"2022-01-07",
    "frequency"=>"minute",
    "fq"=>"pre",
    "fields"=>"None"); ##根据自己的设置来填写参数
    res = HTTP.request("POST",get_price_url, body=JSON.json(params),headers = headers)
    if "compression" in keys(headers) && headers["compression"] == "zstd"
        return String(transcode(ZstdDecompressor, res.body))
    else
        return res.body
    end
end

function get_all_securities(token::String,code::String,date::String)
    url  = "http://47.122.40.16/all_securities";
    headers = Dict("Content-Type"=>"application/json","Authorization"=>token,"lang" =>"julia","compression"=>"zstd")
    params  = Dict("types" => code,"date" =>date);
    res = HTTP.post(url, body=JSON.json(params),headers =headers)
    if "compression" in keys(headers) && headers["compression"] == "zstd"
        return String(transcode(ZstdDecompressor, res.body))
    else
        return res.body
    end
end


```
## rust web api 模式

cargo.toml文件如下：
```rust

[package]
name = "demo"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
tokio = { version = "1.0.0",  features = ["full", "tracing"] }
serde = "1.0.55"
serde_derive = "1.0"
serde_json = "1.0"
reqwest = { version = "0.11", features = ["json", "multipart"] }
zstd = "0.13.0"
```
main.rs文件如下：

```rust
// 注意headers中lang和compression字段的设置。
// 这里采用了tokio异步框架方式，也可以选择纯reqwest库的方式。
use reqwest::{self, Client};
use std::io;
use std::time::{Duration, SystemTime};

const LOGIN_URL :&'static str =  "http://47.122.40.16/login";
const GET_PRICE_URL :&'static str =  "http://47.122.40.16/history_price";

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let sys_time = SystemTime::now();
    let mut myclient  = MyClient::default();
    myclient.get_token().await;
    println!("token :{:?}",myclient.token);
    let data = myclient.get_price().await;
    let costtime = sys_time.elapsed().unwrap();
    println!("data :{:?}",data);
    println!("cost time :{:?} ",costtime);
    Ok(())
}

#[derive(Debug)]
struct MyClient{
    client: Client,
    account: Account,
    mac : String,
    requestid :String,
    token :Option<String>,
    lang: String, //指前端开发语言,python,julia
    compression : String,
}
#[derive(Debug)]
struct Account{
    username : String,
    password : String,
}
impl Account{
    pub fn default()->Self{
        Account{
            username:"************".into(),
            password:"************".into(),
        }
    }
}

impl MyClient{
    pub fn default()-> Self{
        MyClient{
            client: Client::new(),
            account: Account::default(),
            mac : "".into(),//这个无所谓，原来是想让server记住客户端mac信息
            requestid: "1".into(),//这个也无所谓
            token: None,
            lang :"rust".into(),
            compression : "zstd".into(),
        }
    } 

    async fn get_token(&mut self){
        let response = self.client
        .post(LOGIN_URL)
        .header("Content-Type","application/json")
        .json(&serde_json::json!({
            "username": &self.account.username,
            "password": &self.account.password,
        }))
        .send()
        .await
        .expect("send login->");
        //println!("response :{:?}",response);
        self.token = Some(response.text().await.unwrap());
    }
    async fn get_price(&mut self) ->String {
        let sys_time = SystemTime::now();
        if let Some(token) = &self.token{
            let response = self.client
            .post(GET_PRICE_URL)
            .header("Content-Type","application/json")
            .header("Authorization",token)
            .header("lang",&self.lang)
            .header("compression",&self.compression)
            .json(&serde_json::json!({
                "security":"600036.XSHG",
                "start_date": "2021-01-01",
                "end_date": "2021-01-05",
                "frequency": "daily", //daily,minute
                "fq":"pre",
                "fields":"None"
            }))
            .send()
            .await
            .expect("send db get_price ->");
            let  raw_bytes = response.bytes().await.unwrap().to_vec(); 
            let decoded: Vec<u8> = zstd::decode_all(raw_bytes.as_slice()).unwrap();
            let text = std::str::from_utf8(&decoded).unwrap();
            let costtime = sys_time.elapsed().unwrap();
            println!("cost time :{:?}",costtime);
            return String::from(text)
        }else{
            return "get_price Error".into()
        }
    }    
}
```
## 性能
```python
#主要函数性能如下:
def test_get_price():
    start_date = "2022-01-10" # 日期字符串格式
    end_date   = "2023-01-30" # 日期字符串格式
    frequency  = "minute" # daily
    fq         = "pre"#"pre"#"post" # pre:前复权[默认]，None
    codes = "600036.XSHG"
    flds  = ["datetime","close"]
    t0 = t.time()
    df  = db.get_price(codes,start_date,end_date,frequency,fq) ## 返回pd.dataframe格式；
    print(f"code : {codes} df shape : {df.shape} ")
    print(f"-------------{fq}--------------------")
    print(f"{df.head()}")
    print(f"{df.tail()}")
    print(f"--------------{fq}-------------------")
    print(f"cost time :{t.time()-t0} seconds!")
    
if __name__== "__main__" :
	db.auth(）
    test_get_price()
```
输出：

```python
登陆成功！
query -> url :  http://47.122.40.16/history_price 
query -> data : {"security": "600036.XSHG", "start_date": "2022-01-10", "end_date": "2023-01-30", "frequency": "minute", "fq": "pre", "fields": null} method_name: get_price
code : 600036.XSHG df shape : (60720, 7)
-------------pre--------------------
             datetime   open  close   high    low     volume        money
0 2022-01-10 09:31:00  47.41  47.35  47.41  47.22  3133461.0  148370930.0
1 2022-01-10 09:32:00  47.41  47.59  47.60  47.41  2024244.0   96189778.0
2 2022-01-10 09:33:00  47.59  47.80  47.80  47.59  1498226.0   71496604.0
3 2022-01-10 09:34:00  47.80  47.82  47.90  47.80  2136000.0  102250438.0
4 2022-01-10 09:35:00  47.82  47.89  47.89  47.82  1458678.0   69824801.0
                 datetime   open  close   high    low     volume        money
60715 2023-01-30 14:56:00  41.98  42.00  42.02  41.98   542800.0   22797906.0
60716 2023-01-30 14:57:00  42.02  41.99  42.03  41.98   234600.0    9856293.0
60717 2023-01-30 14:58:00  41.99  41.99  41.99  41.99        0.0          0.0
60718 2023-01-30 14:59:00  41.99  41.99  41.99  41.99        0.0          0.0
60719 2023-01-30 15:00:00  41.99  42.03  42.03  41.99  3058600.0  128552958.0
--------------pre-------------------
cost time :0.8377432823181152 seconds!
```

如果有任何问题，欢迎邮件至rustroom@163.com。
