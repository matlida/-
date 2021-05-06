"""
@File    : 《斗破苍穹》小说内容爬取.py
@Time    : 2019/10/31 10:30
@Author  : 封茗囧菌
@Software: PyCharm

      转载请注明原作者
	  创作不易，仅供分享
 
"""
import requests
from bs4 import BeautifulSoup
import re
import time

# 加入请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

}

def get_info(url):
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    # 解析网页数据
    soup = BeautifulSoup(res.text, 'html.parser')
    # 获取到标题
    title = soup.select("body > div.main > div.entry-tit > h1")[0]
    print(title.get_text())
    # 利用正则表达式匹配到内容
    contents = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)

    f = open(r'C:\Python jupyter\爬虫\doupo.txt' , "a+")
    for content in contents:
        f.write(content + "\n")
    f.close()


# 程序主入口
if __name__ == '__main__':
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(i) for i in range(1630, 2000)]
    for url in urls:
        get_info(url)
        print("本章url:" + url)
        # 设置每次循环一次的休眠时间
        time.sleep(1)

