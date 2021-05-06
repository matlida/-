# -*- coding: utf-8 -*-
"""
Created on Sun May 24 17:30:10 2020

@author: Gdc
"""

import requests
import json
import pandas as pd
from fake_useragent import UserAgent
from lxml import etree

url = 'https://www.lagou.com/jobs/positionAjax.json?'
param = {'city':'上海',
         'needAddtionalResult': 'false'
    }

headers = {
        'Referer': 'https://www.lagou.com/jobs/list_%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86?labelWords=&fromSearch=true&suginput=',
        'User-Agent':UserAgent(verify_ssl=False).random,
    }

Li_list = []
n = 0
for i in range(1,31):
    formData = {'first': 'false',
                'pn': i,
                'kd': '算法工程师',
        }

    s = requests.Session()    
    s.get('https://www.lagou.com/jobs/list_%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86?labelWords=&fromSearch=true&suginput=', headers=headers, timeout=3)
    
    res = s.post(url, headers=headers,params=param, data=formData, timeout=3)
    data = json.loads(res.text)
    results = data['content']['positionResult']['result']
    
    for result in results:
        n = n+1
        li = {}
        li['岗位ID'] = result['positionId']
        li['岗位名称'] = result['positionName']
        li['薪酬范围'] = result['salary']
        li['技能要求'] = result['skillLables']
        li['学历要求'] = result['education']        
        li['年限要求'] = result['workYear']
        li['岗位详情页'] = f'https://www.lagou.com/jobs/{result["positionId"]}.html'
        li['公司名称'] = result['companyFullName']
        li['公司地址'] = result['stationname']
        li['所属行业'] = result['industryField']
        li['公司规模'] = result['companySize'] 
        detail = s.post(li['岗位详情页'], headers=headers,params=param, data=formData, timeout=3)  
        dataxp = dataxp = detail.text
        html = etree.HTML(dataxp)   
        p_d = html.xpath('//*[@id="job_detail"]/dd[2]/div//text()')  
        li['岗位要求'] = [x.strip() for x in p_d if x.strip() != '']   
        Li_list.append(li)
        print(f'\r已记录{n}条岗位信息',end='')

df = pd.DataFrame(Li_list)
df.to_excel(r'C:\Python jupyter\爬虫\lagou.xlsx')



print(df)