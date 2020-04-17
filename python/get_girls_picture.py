
'''
    解决办法：
    既然知道了原因，那么就可以针对原因提出解决方法。

    我的办法是过滤掉<class 'NoneType'>这种类型，因为这个空类型是错误的根本。

    在stockInfo = soup.find('div', attrs={'class' : 'stock-bets'})代码下面增加一个if 判断， 用isinstance()函数将空类型过滤掉。

    即：

    if isinstance(stockInfo,bs4.element.Tag):
    然后缩进后续相关的代码，注意在使用isinstance()时，参数2：bs4.element.Tag是参数1：stockInfo要匹配的类型。在使用参数2时要在开头引入bs4模块，即import bs4
    ————————————————
    版权声明：本文为CSDN博主「爱搬砖的小迷糊」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/qq_36525166/java/article/details/81258168
'''
import requests
import bs4
from bs4 import BeautifulSoup
import os
import urllib
import random


class mzitu():
    def all_url(self, url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print(u'开始保存：', title)
            path = str(title).replace("?", '_')
            if not self.mkdir(path):  ##跳过已存在的文件夹
                print(u'已经跳过：', title)
                continue
            href = a['href']
            self.html(href)

    def html(self, href):
        html = self.request(href)
        if isinstance(html,bs4.element.Tag):
            max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                self.img(page_url)

    def img(self, page_url):
        img_html = self.request(page_url)
        if isinstance(img_html,bs4.element.Tag):
            img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
            self.save(img_url, page_url)

    def save(self, img_url, page_url):
        name = img_url[-9:-4]
        try:
            img = self.requestpic(img_url, page_url)
            f = open(name + '.jpg', 'ab')
            f.write(img.content)
            f.close()
        except FileNotFoundError:  ##捕获异常，继续往下走
            print(u'图片不存在已跳过：', img_url)
            return False

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\d\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("D:\d\mzitu", path))
            os.chdir(os.path.join("D:\d\mzitu", path))  ##切换到目录
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def requestpic(self, url, Referer):  ##这个函数获取网页的response 然后返回
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        ua = random.choice(user_agent_list)
        headers = {'User-Agent': ua, "Referer": Referer}  ##较之前版本获取图片关键参数在这里
        content = requests.get(url, headers=headers)
        return content

    def request(self, url):  ##这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content


Mzitu = mzitu()  ##实例化
Mzitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
print(u'恭喜您下载完成啦！')