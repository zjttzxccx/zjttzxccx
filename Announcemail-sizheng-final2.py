#Version: python3
#-*- coding: utf-8 -*-
import urllib
import http.cookiejar
import requests
from bs4 import BeautifulSoup
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import datetime
import socket
import time

#邮件发送模块
def sent_email(mail_body):
    sender = '0010467@zju.edu.cn'
    receiver = ['xujiyu@zju.edu.cn','ccx@zju.edu.cn']
    smtpServer = 'smtp.zju.edu.cn'
    username = '0010467'
    password = '47530471shine'
    if datetime.date.today().isoweekday()==1:
    	mail_title=(datetime.date.today()-datetime.timedelta(days=3)).__format__('%Y-%m-%d')+'至'+(datetime.date.today()-datetime.timedelta(days=1)).__format__('%Y-%m-%d')+'（周五至周日）最新通知'
    else:
    	mail_title = (datetime.date.today()-datetime.timedelta(days=1)).__format__('%Y-%m-%d')+'最新通知'
    mail_body = mail_body

    message = MIMEText(mail_body, 'plain', 'utf-8')
    message["Accept-Language"] = "zh-CN"
    message["Accept-Charset"] = "ISO-8859-1,utf-8"
    message['From'] = sender
    message['To'] =",".join(receiver)
    message['Subject'] = Header(mail_title, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpServer)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, message.as_string())
        print('邮件发送成功')
        smtp.quit()
    except smtplib.SMTPException:
        print("邮件发送失败！！！")

#爬虫模块
def get_content_xgb():
	socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
	url ='http://www.xgb.zju.edu.cn/default.html'
	head={}
	head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	r = requests.get(url=url,headers=head)
	r.encoding='gb2312'
	soup = BeautifulSoup(r.text,'lxml')
	r.close()
	time.sleep(0.1)	# 自定义
	links = soup.find('div',class_="con")
	alinks=links.find_all('li')
	#links = soup.find_all('a',target="_blank")
	#main_url = 'http://bksy.zju.edu.cn/office/'
	content_list = []
	today_time=datetime.date.today()
	for alink in alinks:
		art_url=alink.a.get('href')
		content=alink.a.get('title')
		art_time=alink.find('span',class_="time").text.strip('\n')
		if today_time.isoweekday()==1:
			for i in range(1,4):
				current_time=(today_time-datetime.timedelta(days=i)).__format__('%Y-%m-%d')
				if art_time==current_time:
					content_list.append('学工部通知： '+content+' 链接地址:'+art_url+' 时间：'+art_time)
		else:
			current_time=(today_time-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
		#current_time=(datetime.date.today()-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
			if art_time==current_time:
				content_list.append('学工部通知： '+content+' 链接地址:'+art_url)
	return content_list

def get_content_tw():
	socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
	url ='http://www.youth.zju.edu.cn/redir.php?catalog_id=597'
	head={}
	head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	r = requests.get(url=url,headers=head)
	r.encoding='gb2312'
	soup = BeautifulSoup(r.text,'lxml')
	r.close()
	time.sleep(1)	# 自定义
	links=soup.find('table',width="98%",border="0",align="center",cellspacing="0",style="margin:0px 0px;")
	trlinks=links.find_all('tr')
	main_url='http://www.youth.zju.edu.cn/'
	today_time=datetime.date.today()
	#print(trlinks)
	content_list=[]
	for trlink in trlinks:
		art_url=trlink.a.get('href')
		content=trlink.a.get('title')
		if(trlink.find('td',width="90",align="center")!=None):
			art_time=trlink.find('td',width="90",align="center").text
		if today_time.isoweekday()==1:
			for i in range(1,4):
				current_time='['+(today_time-datetime.timedelta(days=i)).__format__('%Y-%m-%d')+']'
				if art_time==current_time:
					content_list.append('校团委通知： '+content+' 链接地址:'+main_url+art_url+' 时间：'+art_time)
		else:
			current_time='['+(datetime.date.today()-datetime.timedelta(days=1)).__format__('%Y-%m-%d')+']'
		#current_time=(datetime.date.today()-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
			if art_time==current_time:
				content_list.append('校团委通知： '+content+' 链接地址:'+main_url+art_url)
	return content_list

def get_content_jyzx():
	socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
	url ='http://www.career.zju.edu.cn/jyxt/jygz/new/getContent.zf?minCount=0&maxCount=10&lmjdid=739BEBB72A0B2B25E0538713470A6C41&sjlmid=undefined&lmtype=2&lx=2&_=1572597509407'
	head={}
	head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	r = requests.get(url=url,headers=head)
	r.encoding='utf-8'
	soup = BeautifulSoup(r.text,'lxml')
	r.close()
	time.sleep(0.1)	# 自定义
	links = soup.find('ul',class_="com-list")
	#print(links)
	alinks=links.find_all('li')
	#links = soup.find_all('a',target="_blank")
	main_url = 'http://www.career.zju.edu.cn/jyxt/'
	content_list = []
	today_time=datetime.date.today()
	for alink in alinks:
		if alink.a.get('href')=="javascript:void(0)":
			art_url=main_url+alink.a.get('data-src')+'xwid='+alink.a.get('data-xwid')+'&lmtype='+alink.a.get('data-lmtype')
		else:
			art_url=alink.a.get('href')
		content=alink.find('span',class_="news-ctn").text
		#print(content)
		art_time=alink.find('span',class_="news-time").text.strip('\n')
		#print(art_time)
		if today_time.isoweekday()==1:
			for i in range(1,4):
				current_time=(today_time-datetime.timedelta(days=i)).__format__('%Y-%m-%d')
				if art_time==current_time:
					content_list.append('就业中心通知： '+content+' 链接地址:'+art_url+' 时间：'+art_time)
		else:
			current_time=(today_time-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
		#current_time=(datetime.date.today()-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
			if art_time==current_time:
				content_list.append('就业中心通知： '+content+' 链接地址:'+art_url)
	return content_list

if __name__ == '__main__':
	'''url ='http://www.xgb.zju.edu.cn/default.html'
	head={}
	head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	r = requests.get(url=url,headers=head)
	r.encoding='gb2312'
	soup = BeautifulSoup(r.text,'lxml')
	links = soup.find('div',class_="con")
	alinks=links.find_all('li')
	content_list=[]
	for alink in alinks:
		art_url=alink.a.get('href')
		content=alink.a.get('title')
		art_time=alink.find('span',class_="time").text.strip('\n')
		current_time=datetime.date.today().__format__('%Y-%m-%d')
		if art_time==current_time:
			content_list.append(content+'/'+art_time)
	print(content_list)'''

		#art_url=tdlink.find('href')
		#print(art_url)
	content_list1=get_content_xgb()
	content_list2=get_content_tw()
	content_list3=get_content_jyzx()
	content_list=content_list1+content_list2+content_list3
	print(content_list)
	mail_content=''
	if len(content_list)==0:
		sent_email('今天没有邮件')
	else:
		#sent_email(content_list)
		for content in content_list:
			mail_content=mail_content+content+'\r\n\n'
		sent_email(mail_body=mail_content)
	content_list.clear()