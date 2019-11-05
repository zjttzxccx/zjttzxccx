# 浙江大学校内网站通知爬取及邮件提醒
效果图
------
![](https://github.com/zjttzxccx/zjttzxccx/raw/master/Image/sample.png)

技术实现
-------
调用request和BS4来抓取网页HTML源码，同时和最新时间比较之后，提取最新通知的标题及时间

技术栈
-------
    * request
    * BS4
    * smtplib

下载及运行
------
下载之后直接运行py文件，要求至少具有Python环境
