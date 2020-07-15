#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pymysql
import json
import re
def run():
    try:
        job_url = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="contentpile__content__wrapper__item clearfix"]/a')))
        for i in job_url:
            with open('urls_data_0715.json', 'a+',encoding='utf-8') as f:
                    i = i.get_attribute('href')
                    f.write(i+'\n')  
            # 翻页功能，点击下一页，等待页面加载完
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="pagination__check__page"]//button[2]')))
        
        # 下一页的按钮
        next_tag = web.find_element_by_xpath('//div[@class="pagination__check__page"]//button[2]')
        # 按钮变灰，没有下一页，会出现‘pager_next_disabled’属性
        if 'soupager__btn--disable' in next_tag.get_attribute('class'):
            print("已爬取最后一页"+url)
            flag = 0
        else:
                    #如果有下一页，就点击下一页 
            web.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 把要点击的按钮放到可视范围内，不然会报错
            next_tag.click()
            time.sleep(2)
            flag = 1
    except Exception as e:
        print(url)
        print(e)
        flag = 0
    return flag
if __name__ == '__main__':         
    jobnames = ['web前端','数据分析师','大数据','java开发','数据分析师']
    a = 'https://sou.zhaopin.com/?jl='
    url_list = [ a+str(j)+'&kw='+i+'&kt=3' for i in jobnames for j in range(702,719)]
    # 下面代码为设置端口、忽略证书错误以及指定文件夹
    chromeOptions = Options()
    #chromeOptions.add_argument('--user-data-dir=D:\chrome下载文件\AutomationProfile')
    chromeOptions.add_argument('--no-sandbox')  
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    #chromeOptions.add_argument('--headless')
    #chromeOptions.add_argument('--disable-gpu')
    for url in url_list: 
        web = Chrome(options=chromeOptions, executable_path='./chromedriver')
        web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
              "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                    })
                  """
                })
        wait = WebDriverWait(web,3)#设置等待时间 
        web.get(url)
        time.sleep(1)
        flag = 1
        count = 0 
        while flag==1:
                count += 1 
                print(url+'已爬取第%d页'%count)
                flag = run()
        if flag==0:
                web.close()

