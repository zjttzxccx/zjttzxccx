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
    receiver = 'ccx@zju.edu.cn'
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
    message['To'] = receiver
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
def get_content_bksy():
	socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
	url ='http://bksy.zju.edu.cn/office/redir.php?catalog_id=711393'
	head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
	      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	      "Accept-Language":"zh-CN,zh;q=0.9","Connection":"keep-alive","Cookie":"gr_user_id=8e4f4feb-e567-4678-a242-3004d72ca415;grwng_uid=e7d2fa60-043f-4d03-81ac-f1dcc79e1aa4; __utmz=128484826.1564969932.173.2.utmcsr=ccea.zju.edu.cn|utmccn=(referral)|utmcmd=referral|utmcct=/2018/0703/c18416a819394/page.htm; __utma=128484826.1808301175.1536644494.1567577896.1567643034.180; fp_ver=4.7.11; BSFIT_EXPIRATION=1572069874581; BSFIT_DEVICEID=FSWjPTZBZHTSeMiObEVTHRgF1AuN8C8IfjRQxptzCuwq5oJskeYIjUlJPK0KlqkzYsqRtxzOrOOuQIhSWjNuiR8J89DL4oVAtXxfR5K1KAmqhDMJAxzQChRdjGvB6CQxuC70G8ktq0o5By4_34RxlmkGlevdTvSu; Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453=1570671058,1572340027; iPlanetDirectoryPro=Tyo25uImJyPrcIHvR5Xobg29NCrqdKoEoFZJJrmEAVnctsseh63QuzqQ%252Bgpzz6sJtbpo1Hm1wrz%252FdZNIIU3Vp6aAOTcAcvC%252FZhk16KGk%252FKswhdnD0ZW%252BWQIxKqFSPQeHtwbjWT5aQejswloL%252BqDhpmPyqMNk6%252FR7HW%252F%252FOveAUK1h3%252FKX3x08qCOLls0ROTif; sudy_ck=B9B0D6E8E9ED9E99542ED3AF07750A1E4FDB628E60480CDDA7D24A95AF6EF741E11273D00DE1B3A591988EA185CF8C700E15F9E70EEA0A3B7F61202969CACFDAA6F41B61A1DF1F9D0D0CDF7B3B97DF85; wsess=i0qjltbcpc0hbbvkr7op7vcj67; _pk_ref.2.2d7f=%5B%22%22%2C%22%22%2C1572588701%2C%22http%3A%2F%2Fwww.ccea.zju.edu.cn%2F2018%2F0703%2Fc18416a819394%2Fpage.htm%22%5D; _pk_ses.2.2d7f=*; _pk_id.2.2d7f=99f83a0ae589db69.1570692084.34.1572589338.1572588701."}
	r = requests.get(url=url,headers=head)
	r.encoding='gb2312'
	soup = BeautifulSoup(r.text,'lxml')
	r.close()
	time.sleep(1)	# 自定义
	links = soup.find('ul',class_="cg-news-list",id="arthd")
	alinks=links.find_all('li')
	#links = soup.find_all('a',target="_blank")
	main_url = 'http://bksy.zju.edu.cn/office/'
	content_list = []
	today_time=datetime.date.today()
	for alink in alinks:
		art_url=main_url+alink.a.get('href')
		content=alink.a.get('title')
		art_time=alink.find('span',class_="art-date").text
		if today_time.isoweekday()==1:
			for i in range(1,4):
				current_time=(today_time-datetime.timedelta(days=i)).__format__('%Y-%m-%d')
				if art_time==current_time:
					content_list.append('本科生院通知： '+content+' 链接地址:'+art_url+' 时间：'+art_time)
		else:
			current_time=(today_time-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
			if art_time==current_time:
				content_list.append('本科生院通知： '+content+' 链接地址:'+art_url)
	return content_list

def get_content_grs():
	socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
	url ='http://grs.zju.edu.cn/'
	head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
	      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	      "Accept-Language":"zh-CN,zh;q=0.9","Connection":"keep-alive"}
	r = requests.get(url=url,headers=head)
	r.encoding='utf-8'
	soup = BeautifulSoup(r.text,'lxml')
	r.close()
	time.sleep(1)	# 自定义
	links = soup.find('ul',class_="cg-news-list",id="arthd")
	#print(soup)
	alinks=links.find_all('li')
	#aurl=links.find_all('a',target="_blank")
	#links = soup.find_all('a',target="_blank")
	main_url = 'http://grs.zju.edu.cn/'
	content_list = []
	today_time=datetime.date.today()
	for alink in alinks:
		aurl=alink.find('a',target="_blank")
		#print(aurl)
		art_url=main_url+aurl.get('href')
		#print(art_url)
		content=aurl.get('title')
		#print(content)
		art_time=alink.find('span',class_="art-date").text
		#print(art_time)
		if today_time.isoweekday()==1:
			for i in range(1,4):
				current_time=(today_time-datetime.timedelta(days=i)).__format__('%Y-%m-%d')
				if art_time==current_time:
					content_list.append('研究生院通知： '+content+' 链接地址:'+art_url+' 时间：'+art_time)
		else:
			current_time=(today_time-datetime.timedelta(days=1)).__format__('%Y-%m-%d')
			if art_time==current_time:
				content_list.append('研究生院通知： '+content+' 链接地址:'+art_url)
	return content_list

if __name__ == '__main__':
	content_list_1=get_content_bksy()
	content_list_2=get_content_grs()
	content_list=content_list_1+content_list_2
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