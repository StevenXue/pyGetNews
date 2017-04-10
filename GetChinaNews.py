#coding=UTF-8
import re,urllib,socket,os,datetime,sys,time

from NewsParser import *

"""
默认站点列表，各站点的标签及其说明如下：
中国新闻网(ZXW)
网易新闻(163)
人民网(RMW)
新浪(SINA)
凤凰资讯(IFENG)
"""

#下载配置
defaultSiteList = ["ZXW","163","RMW","SINA","IFENG"] #新闻源站点设置
argD = os.getcwd()+os.path.sep+'dataNews'#default目录
newsListFilePath = os.getcwd()+os.path.sep


#默认开始结束时间
defaultStartTime = "2017-03-12"
defaultEndTime = "2017-03-13"
#默认Url连接超时时间
defaultSockTimeLimit = 20

#定义提取的div的属性值，每个网站不一样
dirForDiv = {'ZXW':['class','left_zw'],'163':['id','endText'],'RMW':['id','p_content'],'SINA':['id','artibody'],'IFENG':['id','main_content']}
#定义从滚动新闻页面提取出新闻Url的正则表达式
dirRegex = {'ZXW':r'<div class=\"dd_bt\"><a href=[^<>]*>[^<>]*</a></div><div class=\"dd_time\">[\d]{1,2}-[\d]{1,2} [\d]{2}:[\d]{2}</div>','RMW':r'<a href[^<>]*>[^<>]*</a>\[[\d]{2}[^<>]*[\d]{2}:[\d]{2}\]<br>','163':r't\"[^}]*','SINA':r',title[^}]*','IFENG':r'<h4>[\d]{2}/[\d]{2} [\d]{2}:[\d]{2}</h4><a href=[^<>]*>[^<]*'}
"""
各个网站的滚动新闻页面：
ZXW:"http://www.chinanews.com/scroll-news/" + Year + "/" + Month + Day + "/news.shtml"
163:"http://people.com.cn/GB/24hour/index" + Year + "_" + Month + "_" + Day +".html"
RMW:"http://snapshot.news.163.com/wgethtml/http+!!news.163.com!special!0001220O!news_json.js/"+Year+"-"+Month+"/"+Day+"/0.js"
SINA:"http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&date="+Year+"-"+Month+"-"+Day+"&k=&offset_page=0&offset_num=0&num=30000&asc=&page=1"
IFENG:"http://news.ifeng.com/rt-channel/rtlist_"+Year+Month+Day+"/"+str(pageNum)+".shtml"
"""


#"2013-11-01","2013-12-01",dirName='D:/testnews',timeLimit=20
#s:str_start_time,e:str_end_time,d:dirName,t:timeLimit
argST = defaultStartTime
argED = defaultEndTime

argT = defaultSockTimeLimit
args = sys.argv
if not os.path.exists(argD):
	os.mkdir(argD)

if len(args) == 1:
	#download:下今天的
	argST = time.strftime('%Y-%m-%d')
	argED = time.strftime('%Y-%m-%d',time.localtime(time.time()+86400))
else:
	if len(args) == 2:
		if args[1] != "-a" and args[1] != "-help":
			print "commond error,please see -help"
			sys.exit(0)
		if args[1] == "-a":	
			#download -a: 下载最近一个月的
			argED = time.strftime('%Y-%m-%d',time.localtime(time.time()+86400))
			datetmp = argED.split('-')
			timetmp = time.mktime(datetime.datetime(int(datetmp[0]),int(datetmp[1]),int(datetmp[2])).timetuple())
			argST = time.strftime('%Y-%m-%d',time.localtime(timetmp-86400*30))#往前走30天
		else:
			#download -help:显示帮助#命令帮助信息显示
			print "help info of this commond:\nno arg: get news of today\n-a: get recent 30 days' news\n-d 2017-03-12: get news from the day\n-d 2017-03-12 2017-03-13: get news from the begin day to end day\n-dx 2017-03-12 t: get t days' news from the day\n"
			sys.exit(0)
	elif len(args) == 3:
		if args[1] != "-d":
			print "commond error,please see -help"
			sys.exit(0)
		else:
			if not re.match(r"[\d]{4}-[\d]{2}-[\d]{2}$",args[2]):
				print args[2] + " is not a right date format."
				sys.exit(0)
			#download -d 2017-03-12:下载指定日期的
			argST = args[2]
			datetmp = args[2].split('-')
			timetmp = time.mktime(datetime.datetime(int(datetmp[0]),int(datetmp[1]),int(datetmp[2])).timetuple())
			argED = time.strftime('%Y-%m-%d',time.localtime(timetmp+86400))
	elif len(args) == 4:
		if args[1] != "-d" and args[1] != "-dx":
			print "commond error,please see -help"
			sys.exit(0)
		else:
			if not re.match(r"[\d]{4}-[\d]{2}-[\d]{2}$",args[2]):
				print args[2] + " is not a right date format."
				sys.exit(0)
			if args[1] == "-d":
				if not re.match(r"[\d]{4}-[\d]{2}-[\d]{2}$",args[3]):
					print args[3] + " is not a right date format."
					sys.exit(0)
				#download -d 2017-03-12 2017-03-12：下区间内的
				argST = args[2]
				datetmp = args[3].split('-')
				timetmp = time.mktime(datetime.datetime(int(datetmp[0]),int(datetmp[1]),int(datetmp[2])).timetuple())
				argED = time.strftime('%Y-%m-%d',time.localtime(timetmp+86400))
			else:
				if not re.match(r"[\d]*$",args[3]):
					print args[3] + " is not a right number format."
					sys.exit(0)
				#download  -dx 2017-04-01 t：下指定日期以后t天的
				argST = args[2]
				datetmp = args[2].split('-')
				timetmp = time.mktime(datetime.datetime(int(datetmp[0]),int(datetmp[1]),int(datetmp[2])).timetuple())
				argED = time.strftime('%Y-%m-%d',time.localtime(timetmp+86400*int(args[3])))
				
G = GetNews(str_start_time=argST,str_end_time=argED,dirName=argD,siteList=defaultSiteList,timeLimit=argT)
G.getChinaNews()		
