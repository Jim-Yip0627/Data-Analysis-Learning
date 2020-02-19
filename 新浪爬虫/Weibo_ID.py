#!/usr/bin/env python
# coding: utf-8

# In[62]:


import urllib.request
from urllib import parse
import json
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery as pq
import  pandas as pd
import xlwt
import time

#代理IP
proxy_addr="120.83.123.165"
        
def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({'http':proxy_addr})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data


def getUserId(userName, pageNum, proxy_addr):
    # 用户名需要URL编码后
    print("---" + userName + "---")
    html_doc = "https://s.weibo.com/user/&nickname=" + parse.quote(userName) + "&page=" + pageNum
    html = use_proxy(html_doc,proxy_addr)
    soup = BeautifulSoup(html, 'html.parser')
    if soup:
        print("---Successfully Found Html---")
        for a in soup.find_all("a",attrs={"action-type":"login"}):
            if a:
                uid = a.get('uid')
                return uid
            else:
                print("Fail to Found ID")
                return None

                    
if __name__ == "__main__":
    df = pd.read_excel('D:/nameList.xls')
    name = df['name'].values.tolist()
    k = 0
    for i in name:
        name = re.sub('\s', ' ',i)
        userName = name
        uid = getUserId(userName,"1",proxy_addr)
        print(uid)
        df.loc[k,"uid"] = uid
        k+=1
        time.sleep(2)
    df.to_excel('D:/name_uid.xlsx')
    print("---------Finished---------")
        
    


# In[ ]:




