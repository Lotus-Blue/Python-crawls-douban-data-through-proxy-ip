#检验代理ip是否可用
#time:2019-8-1 15:23

import os
import time
import requests
from bs4 import BeautifulSoup

def test_proxy():
    N = 1
    os.chdir(r'C:/Users/Administrator/Desktop')
    url = 'https://www.baidu.com'
    fp = open('host.txt', 'r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip = p.strip('\n').split('\t')
        proxy = 'http:\\' + ip[0] + ':' + ip[1]
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    for pro in proxys:
        try:
            s = requests.get(url, proxies=pro)
            print('第{}个ip：{} 状态{}'.format(N,pro,s.status_code))
        except Exception as e:
            print(e)
        N+=1

if __name__ == '__main__':
    test_proxy()