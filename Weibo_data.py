#!/usr/bin/env python
# coding: utf-8

# In[9]:


# -*- coding: utf-8 -*-

import urllib.request
import json
import re
import xlwt
import pandas as pd
import time


#设置代理IP
proxy_addr="120.83.123.165"

#定义匹配日期函数
def regexper_date(date):
    pattern = re.compile('2019-(0[1-9]|1[0-2])-(2[0-7]|1[0-9]|0[1-9])|201([0-8])-(0[1-9]|1[0-2])-(3[0-1]|2[0-9]|1[0-9]|0[1-9])')
    matchObj = not(re.match(pattern, date))
    return matchObj

#定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
    return containerid

#获取微博大V账号的用户基本信息;
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    name=content.get('userInfo').get('screen_name')
    print("微博昵称："+name+"\n")
    return name


#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id,file,name,count):
    i=1
    key=True
    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if(len(cards)>0)and(key==True):
                for j in range(len(cards)):
                    card_type=cards[j].get('card_type')
                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        attitudes_count=mblog.get('attitudes_count')
                        comments_count=mblog.get('comments_count')
                        created_at=mblog.get('created_at')
                        reposts_count=mblog.get('reposts_count')
                        scheme=cards[j].get('scheme')
                        text=mblog.get('text')
                        if(regexper_date(created_at)):
                            count+=1
                            print("-----正在爬取第"+str(i)+"页，第"+str(count)+"条微博------")
                            file.write(count,0,str(name))
                            file.write(count,1,str(created_at))
                            file.write(count,2,str(text))
                            file.write(count,3,str(attitudes_count))
                            file.write(count,4,str(comments_count))
                            file.write(count,5,str(reposts_count))
                            file.write(count,6,str(scheme))
                        else:
                            key=False
                            print('--------------爬取完毕--------------')
                            break
                i+=1
            else:
                return count
                break
        except Exception as e:
            print(e)
            pass

if __name__=="__main__":
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('SinaData')
    style = xlwt.XFStyle()
    worksheet.write(0, 0, '微博名') 
    worksheet.write(0, 1, '发布时间') 
    worksheet.write(0, 2, '微博内容') 
    worksheet.write(0, 3, '点赞数') 
    worksheet.write(0, 4, '评论数') 
    worksheet.write(0, 5, '转发数')
    worksheet.write(0, 6, '微博地址')
    print("--------------创建SinaData成功--------------")
    df_uid = pd.read_excel('D:/name_uid.xlsx')
    uid = df_uid['uid'].values.tolist()
    print("--------------读取name_uid成功--------------")
    
    count = 0
    for z in uid: 
        #将浮点型转为int，再将int转换为string
        userID = str(int(z))
        try:
            name = get_userInfo(userID)
            count = get_weibo(userID, worksheet, name, count)
        except Exception as e:
            print(e)
            continue
        time.sleep(2)
    
    print('--------------抓取完毕--------------')
    print('------共抓取微博' + str(count) + "条------")
    workbook.save('D:\SinaData.xls')
    print('--------------保存成功--------------')
    


# In[ ]:




