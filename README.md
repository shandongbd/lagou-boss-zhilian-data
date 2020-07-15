# 拉钩+智联+boss直聘
拉钩+智联+boss直聘的爬虫代码


## lagou.py [点击前往](https://github.com/shandongbd/lagou-boss-zhilian-data/blob/master/lagou.py)
部署在云服务器上，每天8点定时爬取拉勾网，每天需要修改收集日期


## boss.py [点击前往](https://github.com/shandongbd/lagou-boss-zhilian-data/blob/master/boss.py)
爬取boss直聘数据，由于反爬虫机制，需要购买设置代理ip。


## zhilian_urls.py [点击前往](https://github.com/shandongbd/lagou-boss-zhilian-data/blob/master/zhilian_urls.py)
提取每个所有职位的url，在本地运行，每天提取一次。使用时需要登录才能获取全部页面，所以新建一个用户文件夹，用cmd打开浏览器，登录一次会保留登录信息，大概2天失效。


## zhilian_yun.py [点击前往](https://github.com/shandongbd/lagou-boss-zhilian-data/blob/master/zhilian_yun.py)
部署在云服务器上，每天8点定时爬虫。在爬虫开始前一晚，应该将当天的职位urls的json发送到服务器上，并且修改收集日期。
