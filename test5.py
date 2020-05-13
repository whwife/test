import requests
from lxml import etree

header = {
"Referer" : "https://www.mzitu.com/xinggan/",   #防盗链，下载图片时需要使用在network中跟user agent一起的地方可以找到
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
# 1.请求妹子图拿到整体数据
response = requests.get('https://www.mzitu.com/xinggan/')
html = etree.HTML(response.text)

#2.抽取想要的属性
alt_list = html.xpath('//img[@class="lazy"]/@alt')
src_list = html.xpath('//img[@class="lazy"]/@data-original')
for alt,src in zip(alt_list,src_list):                #将标签和图片整合到一起
    # 3.下载图片
    response = requests.get(src,headers = header)               #src时图片地址
    file_name = "E:\\picture\\" + alt + ".jpg"   #    在这个文件夹中建立一个phone的目录，用于存放下载好的图片，\\表示一个\   alt是图片名称
    print("正在保存妹子图片文件："+file_name)
    # 4.保存图片
    with open(file_name,"wb")as f:     #wb是写二进制
        f.write(response.content)
