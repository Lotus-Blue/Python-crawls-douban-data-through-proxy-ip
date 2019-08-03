#一次性爬取豆瓣某标签的电影
#time:2019-4-1 16:07

import urllib.request
import urllib
import json
import time
import os
import random

headers = {}
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers["Accept-Encoding"] = "gzip, deflate, sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2"
# headers["Cache-Control"] = "max-age=0"
headers["Connection"] = "keep-alive"
# headers["Cookie"] = 'bid="LJSWKkSUfZE"; ll="108296"; __utmt=1; regpop=1; _pk_id.100001.4cf6=32aff4d8271b3f15.1442223906.2.1442237186.1442224653.; _pk_ses.100001.4cf6=*; __utmt_douban=1; __utma=223695111.736177897.1442223906.1442223906.1442236473.2; __utmb=223695111.0.10.1442236473; __utmc=223695111; __utmz=223695111.1442223906.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=30149280.674845100.1442223906.1442236473.1442236830.3; __utmb=30149280.4.9.1442237186215; __utmc=30149280; __utmz=30149280.1442236830.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap=1'
headers["Host"] = "movie.douban.com"
headers["Referer"] = "http://movie.douban.com/"
headers["Upgrade-Insecure-Requests"] = 1
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"


#生成代理池子，num为代理池容量
def proxypool(num):
    n = 1
    os.chdir(r'C:/Users/Administrator/Desktop')
    fp = open('host.txt', 'r')
    proxys = list()
    ips = fp.readlines()
    while n<num:
        for p in ips:
            ip = p.strip('\n').split('\t')
            proxy = 'http:\\' + ip[0] + ':' + ip[1]
            proxies = {'proxy': proxy}
            proxys.append(proxies)
            n+=1
    return proxys


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

def fetch_movies():
	ISOTIMEFORMAT='%Y-%m-%d %X'

	outputFile = '灾难-按标记.txt'
	fw = open(outputFile, 'w')
	fw.write('id;title;url;cover;rate\n')

	# 开始爬取
	print("********** START **********")
	print(time.strftime( ISOTIMEFORMAT, time.localtime() ))
	start = 0
	while True:
		print("********** %d **********"%start)
		proxies=proxypool(100)
		change_proxy(proxies)
		url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E7%81%BE%E9%9A%BE&start={}&genres=&countries=".format(start)
		# urllib.request.ProxyHandler({"http": 'http:\\1.197.16.178:9999'})
		request = urllib.request.Request(url=url)
		response = urllib.request.urlopen(request)
		movies = json.loads(response.read())['data']
		if len(movies) == 0:
			break
		# if start > 500:
		# 	break
		print(movies[0])
		for item in movies:
			rate = item['rate']
			title = item['title']
			url = item['url']
			cover = item['cover']
			movieId = item['id']
			record = str(movieId) + ';' + title + ';' + url + ';' + cover + ';' + str(rate) + '\n'
			fw.write(movieId+" ")
			# print (tag + '\t' + title)
		time.sleep(2)  
		start = start + 20
	fw.close()

if __name__ == '__main__':
	fetch_movies()