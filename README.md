### Python-crawls-douban-data-through-proxy-ip
本项目是python爬虫的基础，主要是运用代理ip顺利爬虫，以及如何查看一个隐藏的get接口
==上面的接口可能没用了，但办法是通用的，我当时爬取了豆瓣30个标签电影的数据（只存了电影id），在第一个文件里==

爬虫最怕是被封`ip`，我相信很多爬虫新手都会傻傻地拿自己的`ip`用户爬取数据（顺序1的文件），前几次可能成功，但过了这个时间后，你会发现请求抛出`403 `状态码，这是因为你的请求频率太高了，系统会认为你在爬虫，暂时把你的`ip`封了。

那如何解决这个问题呢？主要有下面三种办法

 1. 伪装请求报头（request header）
 2. 减轻访问频率，速度
 3. 使用代理IP
 
 一般办法1作用不大，办法2的话又导致耗时太大，所以办法3是又省时又奏效的好办法

##### 1、首先我们[国内高匿代理IP](https://www.xicidaili.com/nn/1) 获得代理IP数据

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803124737242.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMzY3Mw==,size_16,color_FFFFFF,t_70)
这么多`ip`够你用的了，但是也不能任性，还是尽量不要同时运行多个爬虫程序

运行文件2之后，你会得到一个下面这样的文件
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803125149203.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMzY3Mw==,size_16,color_FFFFFF,t_70)
##### 2、检验这些`ip`是否可用，经本人测试，一般都是`状态码200`，所以这步你忽略也没关系
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803125047607.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMzY3Mw==,size_16,color_FFFFFF,t_70)
##### 3、智能更换代理`ip`（但没有检验通过该代理，请求是否成功）
```
def change_proxy(proxies):
    proxy=random.choice(proxies)
    if proxy==None:
        proxy_support=urllib.request.ProxyHandler({})
    else:
        proxy_support = urllib.request.ProxyHandler({"http": proxy})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders=[("User-Agent",headers["User-Agent"])]
    urllib.request.install_opener(opener)
    print('智能切换代理：%s' % ('本机' if proxy == None else proxy))
```
##### 4、检验通过该代理，请求是否成功

```
respones = requests.get(url, headers=headers, proxies=random.choice(proxys))
while respones.status_code!=200:
	respones = requests.get(url, headers=headers, proxies=random.choice(proxys))
```
-----
##### 获取get接口
打开chrome的“检查”工具->切换到network界面->选择`XHR`，准备看网站的真实请求地址
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803130145399.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMzY3Mw==,size_16,color_FFFFFF,t_70)
通过chrome的“检查”观察发现真实的URL为

> https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0&genres=%E5%96%9C%E5%89%A7&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86

`sort`:按热度排序为T、按时间排序为R、按评分排序为S
`tags`:类型
`countries`:地区
`geners`:形式（电影、电视剧…）
`start`:“加载更多”
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803130613391.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMzY3Mw==,size_16,color_FFFFFF,t_70)
对于爬虫，这种`json`数据是很好的

==总之先看下真实请求接口有没有好东西，没有的话再爬取网站源码数据==
