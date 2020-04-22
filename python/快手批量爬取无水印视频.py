'''
@Author: your name
@Date: 2020-04-22 21:08:45
@LastEditTime: 2020-04-22 21:20:19
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \text1\快手爬取无水印视频.py
'''
# -*-coding:utf-8 -*-
import requests
import time
import os
import json
import threading
import re
 
cookies = ""
 
def downVideo(video,d_url,v_name):
    if not os.path.exists(video):
        r = requests.get(d_url)
        r.raise_for_status()
        with open(video, "wb") as f:
            f.write(r.content)
        print("    视频 " + v_name + " 下载成功 √")
#    else:
#        print("    视频 " + v_name + " 已存在 √")
 
def downPic(j,pic,d_url,p_name):
    if not os.path.exists(pic):
        r = requests.get(d_url)
        r.raise_for_status()
        with open(pic, "wb") as f:
            f.write(r.content)
        print("    " + str(j + 1) + "/ 图片 " + p_name + " 下载成功 √")
#    else:
#        print("    " + str(j + 1) + "/ 图片 " + p_name + " 已存在 √")
 
def getCookies():
#    url = 'https://c.m.chenzhongtech.com/rest/lapi/getcoo?_='+str(int(round(time.time() * 1000)))
    url = 'https://live.kuaishou.com/u/3x57y7nzsq38ryu/3xv6h3usek8agau'
    headers_web = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'live.kuaishou.com',
#    'Origin': 'https://v.kuaishou.com',
#    'Referer': 'https://v.kuaishou.com/fw/photo/3xqbgg5rrpui69c',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
#    'Cookie':'did=web_8f50746f9f90467ea33f258ca67d6822'
    }
    rs = requests.get(url=url, headers=headers_web, allow_redirects=False)
#    resJson = json.loads(rs.content.decode(encoding='utf-8'))
    global cookies
#    cookies = resJson['cookies'][0].split(';')[0]
    cookies = 'did='+rs.cookies._cookies['.kuaishou.com']['/']['did'].value
 
def getVideo(data):
    url = 'https://v.kuaishou.com/rest/kd/feed/profile'
    headers_web = {
    'accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'v.kuaishou.com',
    'Origin': 'https://v.kuaishou.com',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    #Cookie 根据自己的电脑修改
    #'Cookie': 'did=web_6ab2aa48ebfa49c18e497b1efb80429f'
    }
    headers_web["Cookie"] = cookies
    rs = requests.post(url=url, headers=headers_web, json=data)
    v_json = json.loads(rs.content.decode(encoding='utf-8'))
    if (str(v_json["result"])=="2"):
        print("服务器返回操作太快，可能触发反爬机制")
        return
    feeds = v_json["feeds"]
    for i in range(len(feeds)):
        feed = feeds[i]
        caption = str(feed["caption"]).replace("\n","").replace("\u200b","").replace("\"","").replace("\\","")[0:100]
        f_time = time.strftime('%Y-%m-%d %H%M%S', time.localtime(feed['timestamp'] / 1000))
        name = re.sub(r'[\\/:*?"<>|\r\n]+', "", feed['userName'])
        dir = "data/" + name + "(" + feed['userEid'] + ")/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        if(str(feed['singlePicture']) == "False"):
            d_url = feed['mainMvUrls'][0]['url']
            v_name = f_time + "_" + caption + ".mp4"
            video = dir + v_name
            t_downVideo = threading.Thread(target=downVideo, args=(video,d_url,v_name,))
            t_downVideo.start()
        else:
            try:
                imgList = feed['ext_params']['atlas']['list']
                cdn = feed['ext_params']['atlas']['cdn'][0]
            except:
                imgList = []
                imgList.append(str(feed['coverUrls'][0]['url']).replace("https://",""))
                cdn = ""
            for j in range(len(imgList)):
                p_name = f_time + "_" + caption + "_" + str(j + 1) + ".jpg"
                pic = dir + p_name
                d_url = "https://" + cdn + imgList[j].replace("webp","jpg")
                t_downPic = threading.Thread(target=downPic, args=(j,pic,d_url,p_name,))
                t_downPic.start()
    pcursor = v_json["pcursor"]
    if(str(pcursor) != "no_more"):
        data = {"eid":v_json['feeds'][0]['userEid'],"count":30,"pcursor":pcursor}
        getVideo(data)
 
 
 
if not os.path.exists("/data"):
    os.makedirs("/data")
getCookies()
eidList = ["3x57y7nzsq38ryu", "3xv6h3usek8agau"]
for eid in eidList:
    data = {"eid":eid,"count":30,"pcursor":"0"}
    getVideo(data)
print("收工")