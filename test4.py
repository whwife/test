# 导入必要的包
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

# 打开谷歌浏览器
driver = webdriver.Chrome()
# 输入url，打开煎蛋网首页
driver.get('http://jandan.net')
# 初始化一个引用计数，用于后面的图片简单命名
index = 1

# 定义爬虫方法
def getImage(link_texts):
    # 将index置为全局变量
    global index
    # 通过点击的动作执行翻页
    for i in link_texts:
        # 模拟点击
        driver.find_element_by_link_text(i).click()
        # 解析网页
        html = BeautifulSoup(driver.page_source, 'html.parser')
        # 获取原图的url链接
        links = html.find_all('a', {'class': 'view_img_link'})
        # 遍历当页获得的所有原图链接
        for link in links:
            # 将原图存至当前目录下的jdimg 文件夹，以index命名，后缀名为图片原名的后三位，即jpg或者gif
            # with open('jdimg/{}.{}'.format(index, link.get('href')[len(link.get('href'))-3: len(link.get('href'))]), 'wb') as jpg:
            #     jpg.write(requests.get("http:" + link.get('href')).content)
            # print("正在爬取第%s张图片" % index)
            # index += 1
            with open( "E:\\picture/{}.{}".format(index,link.get('href')[len(link.get('href')) - 3: len(link.get('href'))]),
                      'wb') as f:
                    f.write(requests.get("http:" + link.get('href')).content)
            print("正在爬取第%s张图片" % index)
            index += 1

# 定义主函数
def main():
    # 将准备执行的浏览或翻页动作的关键字存入数组
    link_texts = [u'随手拍', u'下一页', u'下一页', u'下一页', u'下一页']
    #开始爬取
    getImage(link_texts)

main()