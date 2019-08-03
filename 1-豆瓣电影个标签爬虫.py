#一次性爬取豆瓣所有电影的概要信息
#time:2019-8-1 15:47

import urllib.request
import urllib
import json
import time

ISOTIMEFORMAT='%Y-%m-%d %X'

outputFile = 'DouBanTagMovieData.txt'
fw = open(outputFile, 'w')
fw.write('id\t title\t url\t cover\t rate\n')

headers = {}
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers["Accept-Encoding"] = "gzip, deflate, sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2"
headers["Connection"] = "keep-alive"
headers["Host"] = "movie.douban.com"
headers["Referer"] = "http://movie.douban.com/"
headers["Upgrade-Insecure-Requests"] = 1
headers["User-Agent"] = "Mozilla/6.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"

# 获取标签
request = urllib.request.Request(url="http://movie.douban.com/j/search_tags?type=movie")
response = urllib.request.urlopen(request)
tags = json.loads(response.read())['tags']

# 开始爬取
print("********** START **********")
print(time.strftime( ISOTIMEFORMAT, time.localtime() ))

for tag in tags:
	print ("Crawl movies with tag: " + tag)
	print (time.strftime( ISOTIMEFORMAT, time.localtime() ))

	start = 0
	while True:
		url = "http://movie.douban.com/j/search_subjects?type=movie&tag=%s&page_limit=20&page_start=%d" %(tag.encode('utf8'),start)
		request = urllib.request.Request(url=url)
		response = urllib.request.urlopen(request)
		movies = json.loads(response.read())['subjects']#读取json数据
		if len(movies) == 0:
			break
		for item in movies:
			rate = item['rate']
			title = item['title']
			url = item['url']
			cover = item['cover']
			movieId = item['id']
			record = str(movieId) + ';' + title + ';' + url + ';' + cover + ';' + str(rate) + '\n'
			fw.write(record.encode('utf8'))
			print (tag + '\t' + title)
		start = start + 20
if __name__ == '__main__':
	fw.close()