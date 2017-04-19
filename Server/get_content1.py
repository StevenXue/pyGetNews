#coding:utf-8  
#author:zhangyang  
#date:2015-5-17  
#�˳���������ȡ�����ձ��µ�������Դ����ҳ����Ҫ��ȡ����1946�굽2003��֮�������·�  
#�μ�ҳ���Ǹ����·ݵ����б���  
#ĩ��ҳ���Ǳ�������  
  
import urllib2,bs4,os,re  
from time import clock  
  
#����bs4����url�ķ������Բο���http://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html  
  
starturl="http://rmrbw.info/"  
testMonthURL="http://rmrbw.info/thread.php?fid=6"  
  
def getSoup(url):  
    pape=urllib2.urlopen(url)  
    soup=bs4.BeautifulSoup(''.join(pape),'lxml')  
    return soup  
  
#����ҳ���ж�ȡÿһ����ÿ���µ�URL���һ��URLLIST���أ�  
def getDataFromMainURL():  
    urllist=[]  
    mainSoup=getSoup(starturl)  
    alist=mainSoup.find_all('a','fnamecolor')  
    for item in alist:  
        urllist.append(starturl+item['href'])  
  
    return urllist  
  
  
#����ÿһ���µ���ҳ�棬�����õ��ܵ���ҳ�����͵�ǰ�ĵ�URL  
#����������ҳ�淵�ص�URLLIST����ܵ�URLLIST  
#���ݵõ�URLΪÿһ���´�����һ���ļ��С�  
def getDataFromMonth(monthURL):  
    filepath=os.getcwd()+os.path.sep+"data"+os.path.sep  
    urllist=[]  
    soup=getSoup(monthURL)  
    title=soup.find('a','fl')   #�ҵ����µı�ǩλ��  
    month=title.contents[0]  
    curpath=os.getcwd()  
    #print month.encode('utf8')  
    datapath=curpath+os.path.sep+"data"+os.path.sep+month.encode('utf8')  
    if os.path.exists(datapath)==False:  
        os.mkdir(datapath)                       #�����õ����ļ���  
  
    pages=soup.find('div','pages').contents[-1]  
    totalpage=pages.split(' ')[3].split('/')[1]   #�õ���ҳ����  
  
    for num in range(int(totalpage)):  
        curURL=monthURL+"&page="+str(num)  
        urllist+=getDocementList(curURL)  
    print "�����뵱ǰ�·ݵ�����urllist"  
    return datapath,urllist  
  
#�õ���ǰҳ����ĵ�URL���URLLIST����  
def getDocementList(curURL):  
    urllist=[]  
    curSoup=getSoup(curURL)  
    res=curSoup.find_all(id=re.compile("a_ajax_"))  
    for item in res:  
        urllist.append(starturl+item['href'])  
  
    print "�����뵱ǰҳ��������ĵ�url"  
    return urllist  
  
#�õ�docement�е����ݲ����浽�ļ���  
def getDocement(docURL):  
    docSoup=getSoup(docURL)  
    title=docSoup.find('h1','fl').get_text()  
    title=title.strip().split(' ')[0]  
    cont_div=docSoup.find('div','tpc_content')  
    cont=cont_div.get_text().strip()  
    pattern=re.compile(r'<br/?>')  
    #for item in cont_div:  
        #print type(item)  
        #if not re.match(str(item)):  
            #cont+=str(item)  
        #if str(item)!='<br/>' or str(item)!='<br>':  
            #cont+=str(item)  
  
    return title,cont  
  
  
  
#�·�ҳ���µĿ��Ƴ�������Ϊ�·ݵ�URL��������ȡ�����ݷֱ���뵽�ļ���  
def monthMain(monthURL):  
    start=clock()  
    datapath,urllist=getDataFromMonth(monthURL)  
    for url in urllist:  
        try:  
            doc_title,doc_cont=getDocement(url)  
            #print doc_title  
            doc_title=doc_title.encode('utf8')  
            filename=datapath+os.path.sep+doc_title+".txt"  
            f=open(filename,'w')  
        except Exception as e:  
            print e  
            continue  
        doc_cont=doc_cont.encode('utf8')  
        f.write(doc_cont)  
        f.close()  
    end=clock()  
    print "finish input data to "+datapath  
    print "running time is "+str(end-start)+"s"  
  
  
def main():  
    starttime=clock()  
    urllist=getDataFromMainURL()  
    for url in urllist:  
        try:  
            monthMain(url)  
        except Exception as e:  
            print e  
            continue  
    endtime=clock()  
    print "total running time is "+str(endtime-starttime)+"s"  
if __name__=="__main__":  
    main()  