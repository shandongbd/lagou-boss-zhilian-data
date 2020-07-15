#!/usr/bin/env python
# coding: utf-8

# In[66]:


#!/usr/bin/env python
# coding: utf-8

from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import re
import json
import pymysql
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  #无头
	

def run():
    
#获取数据
    job_url = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="position_link"]')))
    job_title = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="position_link"]/h3')))
    job_company_name = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="com_logo"]/a/img')))
    job_company_url = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="company_name"]/a')))
    job_location = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="position_link"]/span/em')))
    job_salary = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="p_bot"]//div[@class="li_b_l"]/span')))
    job_release_data = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="format-time"]')))
    for a,b,c,d,e,f,g in zip(job_title,job_url,job_company_name,job_company_url,job_location,job_salary,job_release_data):
        f = f.text.lower()#将工资信息 单位k 统一为小写
        try:
            max_salary = re.findall(r"\d+k",f,)[1].split('k')[0]+'000'
        except:
            max_salary = f
        if   re.findall(r"\d*-\d*-\d*",g.text,) :g = g.text
        else: g = '2020-7-12'
        dict = {
            "job_sourse":"1",
            "job_title":a.text,
            "job_url":b.get_attribute('href'),
            "job_company_name":c.get_attribute('alt'),
            "job_company_url":d.get_attribute('href'),
            "job_location":e.text,
            "job_salary":f,
            "job_max_salary":max_salary,
            "job_min_salary":f[:f.index('k')]+'000',
            "job_release_data":g,
            "job_collect_data":"2020-7-13"
                                 }
        cursor = db.cursor()#保存到mysql
        table = 'jobs'
        keys = ','.join(dict.keys())
        values = ','.join(['%s'] * len(dict))
        sql = 'insert into {table}({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
        try:
             if cursor.execute(sql, tuple(dict.values())):
                 print('insert successful')
                 db.commit()
        except Exception as e:
                 print("insert failed!", e)
                 db.rollback()
    try:                 
# 点击下一页，等待页面加载完
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="pager_container"]//span[@action="next"]')))
# 下一页的按钮
        next_tag = web.find_element_by_xpath('//div[@class="pager_container"]//span[@action="next"]')
# 按钮变灰，没有下一页，会出现‘pager_next_disabled’属性
        if 'pager_next_disabled' in next_tag.get_attribute('class'):
            print("已爬取最后一页"+url)
            flag = 0
        else:
                #如果有下一页，就点击下一页 
            web.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 把要点击的按钮放到可视范围内，不然会报错
            next_tag.click()
            time.sleep(2)
            flag = 1
        return  flag         
    except : web.close()
  
if __name__ == '__main__': 
    jobnames = ['web前端','大数据开发','大数据','java开发','etl开发']
    a = 'https://www.lagou.com/jobs/list_'
    url_list = [ a+i+'?city=济南' for i in jobnames]
    url_list_2 = [ a+i+'?city=青岛' for i in jobnames]
    url_list.extend(url_list_2)
    db = pymysql.connect("119.3.184.238","guest","guest","jobs")# 打开数据库连接
    for url in url_list:
        web = Chrome(options=chrome_options)
        wait = WebDriverWait(web,8)#设置等待时间 
        web.get(url)
        time.sleep(1)
        try:
            web.find_element_by_xpath('/html/body/div[8]/div/div[2]').click()
        except:   pass  
        flag = 1
        count = 0 
        while flag==1:
            count += 1
            print('已爬取第%d页'%count)
            flag = run()
        if flag==0:
            web.close()
    db.close()       
    







