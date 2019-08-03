#爬取某网站获取国内高匿ip数据
#time:2019-8-1 15:12

import os
import time
import requests
from bs4 import BeautifulSoup

def fetch_proxy(num):#表示获取num页 
    #修改当前工作文件夹
    os.chdir(r'C:/Users/Administrator/Desktop')
    api = 'http://www.xicidaili.com/nn/{}'
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    fp = open('host7.txt', 'a+', encoding=('utf-8'))
    
    ISOTIMEFORMAT='%Y-%m-%d %X'
    print("********** START **********")
    print(time.strftime( ISOTIMEFORMAT, time.localtime() ))
    start_time=time.time()

    #一页页爬取这个网站的代理ip
    for i in range(1,num+1):
        api = api.format(i)
        respones = requests.get(url=api, headers=header)
        soup = BeautifulSoup(respones.text, 'lxml')
        container = soup.find_all(name='tr',attrs={'class':'odd'})
        for tag in container:
            try:
                con_soup = BeautifulSoup(str(tag),'lxml')
                td_list = con_soup.find_all('td')
                ip = str(td_list[1])[4:-5]  #td_list[1],例如<td>163.204.246.120</td>，我们只截取ip部分
                port = str(td_list[2])[4:-5]
                IPport = ip + '\t' + port + '\n'
                fp.write(IPport)
            except Exception as e:
                print('No IP！')
        time.sleep(1)
    fp.close()
    end_time=time.time()
    print("本次耗时'%.2fs"%(end_time-start_time))

if __name__ == '__main__':
    fetch_proxy(5)