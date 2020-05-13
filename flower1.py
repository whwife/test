#-----------------------------------------------------------------------------
# Name:        douban.py
# Purpose:     读取豆瓣上关于某个电影的评论，并用词云显示出来
#
# Author:      ISS-XiangjianChen
#
# Created:     16/04/2020
# Copyright:   (c) ISS 2018
#-------------------------------------------------------------------------------

import urllib.request
import jieba
from bs4 import BeautifulSoup as bs
import re
from pyecharts import WordCloud 

#获取评论放一个文本文件中
#名          ID
#阿甘正传   1292720
#无问西东   6874741
#红海行动   26861685
#捉妖记2    26575103
def GetTxt(start):
    eachCommentList = []
    requrl = 'https://movie.douban.com/subject/26787574/comments?start='+ \
              str(start) + '&limit=20&sort=new_score&status=P'
    resp = urllib.request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')
    for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)
    #写到文本文件中
    f = open('content.txt','a',encoding='utf-8')
    for comment in eachCommentList:
        f.write(comment)
    f.close()

#从文本文件中生成词云
def Generator():
    with open('content.txt', 'r', encoding='utf-8') as f:
        text_body = f.read()
    f.close()

    #使用jieba进行分词
    words_lst = jieba.cut(text_body.replace('\n', '').replace(' ', ''))
    #统计词频
    total = {}
    for i in words_lst:
        total[i] = total.get(i, 0) + 1

    #按词频进行排序，只选取包含两个或两个以上字的词
    data = dict(sorted({k: v for k, v in total.items() if len(k) >= 2}.items(),\
                        key=lambda x: x[1], reverse=True)[:200])

    name = data.keys()
    value = [i for i in data.values()]#获取列表对象

    #构造一个词云对象，把所有的词放进去
    word_cloud = WordCloud(width=1600, height=1024)
    #pentagon表示用五角星的形状显示词云
    word_cloud.add("", name, value, word_size_range=[20, 100], shape='triangle')
    #把词云显示到一个html网页中
    word_cloud.render('content.html')


def main():
    for i in range(1,201,20):
        GetTxt(i)
    Generator()

if __name__ == '__main__':
    main()