# -*- encoding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import random
import io
import sys
import time

# 使用session来保存登陆信息
s = requests.session()


# 获取动态ip，防止ip被封
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


# 随机从动态ip链表中选择一条ip
def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


# 获取评论内容和下一页链接
def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    comment_list = soup.select('.comment > p')
    next_page = soup.select('.next')[0].get('href')
    return comment_list, next_page


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    absolute = 'https://movie.douban.com/subject/26322642/comments'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
    loginUrl = 'https://www.douban.com/accounts/login?source=movie'
    formData = {
        "redir": "https://movie.douban.com/subject/26322642/comments?start=201&limit=20&sort=new_score&status=P&percent_type=",
        "form_email": "www.1239198605@qq.com",
        "form_password": "yyf15997588668",
        "login": u'登录'
    }
    # 获取动态ip
    url = 'http://www.xicidaili.com/nn/'
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)

    current_page = absolute
    next_page = ""
    comment_list = []
    temp_list = []
    num = 0
    ans = 0
    while (1):
        ans += 1
        print("爬取第" + str(ans) + "页")
        time.sleep(5)
        html = s.get(current_page, headers=headers, proxies=proxies).content
        temp_list, next_page = get_data(html)

        if ans == 7:
            break
        current_page = absolute + next_page
        comment_list = comment_list + temp_list
        # time.sleep(1 + float(random.randint(1, 100)) / 20)
        num = num + 1
        # 每20次更新一次ip
        if num % 20 == 0:
            proxies = get_random_ip(ip_list)
        print(current_page)
        # 将爬取的评论写入txt文件中
        with open("E:\comments.txt", 'a')as f:
            ark = 0
            for node in comment_list:
                comment = node.get_text().strip().replace("\n", "")
                f.write(comment + "\n")
                ark += 1
                print("写了" + str(ark) + "个")
            f.close()