#-*-coding=UTF-8-*-

import pymongo  
 
HOST = "127.0.0.1"  
PORT = 27017  
client = pymongo.MongoClient(HOST,PORT)  
# 选择一个数据库
NewsDB = client.NewsDB
# 选择一个collection
collection = NewsDB.NewsList

print(collection)  

# 插入
dic = {  
    "from_url" : "http://tech.163.com/",  
    "news_body" : [  
        "科技讯 6月9日凌晨消息2015",  
        "全球开发者大会（WWDC 2015）在旧",  
        "召开，网易科技进行了全程图文直播。最新",  
        "9操作系统在",  
        "上性能得到极大提升，可以实现分屏显示，也可以支持画中画功能。",  
        "新版iOS 9 增加了QuickType 键盘，让输入和编辑都更简单快捷。在搭配外置键盘使用 iPad 时，用户可以用快捷键来进行操作，例如在不同 app 之间进行切换。",  
        "而且，iOS 9 重新设计了 app 间的切换。iPad的分屏功能可以让用户在不离开当前 app 的同时就能打开第二个 app。这意味着两个app在同一屏幕上，同时开启、并行运作。两个屏幕的比例可以是5：5，也可以是7：3。",  
        "另外，iPad还支持“画中画”功能，可以将正在播放的视频缩放到一角，然后利用屏幕其它空间处理其他的工作。",  
        "据透露分屏功能只支持iPad Air2；画中画功能将只支持iPad Air, iPad Air2, iPad mini2, iPad mini3。",  
        "\r\n"  
    ],  
    "news_from" : "网易科技报道",  
    "news_thread" : "ARKR2G22000915BD",  
    "news_time" : "2015-06-09 02:24:55",  
    "news_title" : "iOS 9在iPad上可实现分屏功能",  
    "news_url" : "http://tech.163.com/15/0609/02/ARKR2G22000915BD.html"  
}  

#测试用
# collection.insert(dic)

