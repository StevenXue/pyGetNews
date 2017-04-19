#coding:utf-8
#�˳���������ȡ�����ձ��µ�������Դ����ҳ����Ҫ��ȡ����1946�굽2003��֮�������·�
#�μ�ҳ���Ǹ����·ݵ����б���
#ĩ��ҳ���Ǳ�������
#ʹ�ö��߳������ȡЧ��

'''�����д�����IO�����߳̿��������ȡ��Ч�ʡ����ڲ�ͬ���д洢��ͬurl�Ͷ���������зֹ��ĳ��ԣ�����ʵ������������shareMonthQueue��shareReportQueue������shareMonthQueue�洢�����·ݳ�ʼurl�Ͱ���������ҳ�棨һ���·��кܶ�page������1946��5�°���30��page����shareReportQueue�洢�������ŵ�url��������������ר�õ�����monthSpider��reportSpider'''

import urllib2,bs4,os,re
from time import clock
import threading,Queue

#����bs4����url�ķ������Բο���http://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html

starturl="http://rmrbw.info/"
shareMonthQueue=Queue.Queue()  #�洢�·�url�Ĺ�������
shareReportQueue=Queue.Queue() #c�洢����url�Ĺ�������
_WORK_MONTH_THREAD_NUM=3       #���ڴ����·�url����������
_WORK_REPORT_THREAD_NUM_=10    #���ڴ�������url����������
totalNum=0  #ȫ�ּ�����
mutex=threading.Lock() #������
tlist=[]<span style="white-space:pre">	</span>#�߳��б�
t1=clock()
t2=clock()
t3=clock()
t4=clock()

class monthSplider(threading.Thread):
	def __init__(self,name,dicPath = os.getcwd()+os.path.sep+"data"+os.path.sep):
		threading.Thread.__init__(self)
		self.name=name
		self.dicPath=dicPath
		self.TIMEOUT=10

	def run(self):
		start=clock()
		end=clock()
		while True:
			if shareMonthQueue.empty()==False:
				start=clock()
				monthurl=shareMonthQueue.get()
				try:
					page=urllib2.urlopen(monthurl).read()
					soup=bs4.BeautifulSoup(''.join(page),'lxml')
				except Exception as e:
					print "loading url error at line 43"
					print e
					continue
				title=soup.find('a','fl')   #�ҵ����µı�ǩλ��
				month=title.contents[0]
				curpath=os.getcwd()
				#print month.encode('utf8')
				datapath=self.dicPath+month.encode('gbk')
				if os.path.exists(datapath)==False:
					os.mkdir(datapath)                       #�����õ����ļ���

				pages=soup.find('div','pages').contents[-1]
				totalpage=pages.split(' ')[3].split('/')[1]   #�õ���ҳ����
				templist=monthurl.split('=')
				curpage=templist[-1]
				curpage=int(curpage.strip())              #�õ���ǰҳ��ֵ
		
				#�ж����curpageС��totalpage�����curpage+1�õ���һ��ҳ�����shareMonthQueue��
				if curpage<totalpage:
					templist[-1]=str(curpage+1)
					nexturl='='.join(templist)
					shareMonthQueue.put(nexturl)
				#��ȡ��ǰҳ���������ŵ�url,����url����shareReportQueue��
				res=soup.find_all(id=re.compile("a_ajax_"))
				for item in res:
					shareReportQueue.put(starturl+item['href'])
			else:
				#��shareMonthQueueΪ�յ�����µȴ�TIMEOUT����˳�
				end=clock()
				if (end-start)>self.TIMEOUT:
					break
					
class reportSpider(threading.Thread):
	def __init__(self,name,dicPath = os.getcwd()+os.path.sep+"data"+os.path.sep):
		threading.Thread.__init__(self)
		self.name=name
		self.dicPath=dicPath
		self.TIMEOUT=10
		
	def run(self):
		start=clock()
		end=clock()
		while True:
			if shareReportQueue.empty()==False:
				start=clock()
				url=shareReportQueue.get()
				try:
					page=urllib2.urlopen(url).read()
					soup=bs4.BeautifulSoup(''.join(page),'lxml')
				except Exception as e:
					print "loading url error at line 93"
					print e
					continue
				month=soup.find('a',href=re.compile('thread.php')).get_text().strip() #������ǰ��ҳ��������
				month=month.encode('gbk')
				title=soup.find('h1','fl').get_text() #������ǰ��ҳ�����ű���

				title=title.strip().split(' ')[0]
				#print title.encode('utf8')
				cont_div=soup.find('div','tpc_content')
				cont=cont_div.get_text().strip()   #������ǰ��ҳ����������
				title=title.encode('gbk')
				cont=cont.encode('gbk')
				try:
					filename=self.dicPath+month+os.path.sep+title+'.txt'
					f=open(filename,'w')
					f.write(cont)
				except Exception as e:
					print str(e)+self.name
					continue
				global totalNum
				global mutex
				if mutex.acquire(1):
					totalNum+=1
					mutex.release()
				#print self.name+"������һ��ҳ��"
				if totalNum%100==0:
					global t3,t4
					t4=clock()
					print "�Ѵ�����"+str(totalNum)+"������,��ʱ"+str(t4-t3)+'s'
			else:
				end=clock()
				if (end-start)>self.TIMEOUT:
					break

def main():
	global t1,t2,t3,t4
	t1=clock()
	pape=urllib2.urlopen(starturl)
	mainsoup=bs4.BeautifulSoup(''.join(pape),'lxml')
	alist=mainsoup.find_all('a',class_='fnamecolor',limit=10)

	for item in alist:
		monthurl=item['href']+'&page=1'
		shareMonthQueue.put(starturl+monthurl)
	t2=clock()
	print "��ҳ����ȡ��ɣ���ʱ"+str(t2-t1)+'s'

	for i in xrange(_WORK_REPORT_THREAD_NUM_):
		if i<_WORK_MONTH_THREAD_NUM:
			ms=monthSplider('ms'+str(i))
			tlist.append(ms)
		rs=reportSpider('rs'+str(i))
		tlist.append(rs)
	t3=clock()
	print "����׼������,��ʱ"+str(t3-t2)+'s'
	for t in tlist:
		t.start()
	for t in tlist:
		t.join()

if __name__=="__main__":
	main()