#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101121500
import requests   
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import json

def get_ip():
    # 这里填写芝麻代理api地址，num参数必须为1，每次只请求一个IP地址                                                                                
    url = 'http://d.jghttp.golangapi.com/getip?num=1&type=1&pro=440000&city=440100&yys=0&port=1&pack=26785&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions='#ip接口
    response = requests.get(url)
    response.close()
    ip = response.text
    print(ip)
    return ip

def run():
    
#获取数据
    job_url = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="job-name"]/a')))
    job_title = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="job-name"]/a')))
    job_company_name = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="company-text"]/h3/a')))
    job_company_url = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="company-text"]/h3/a')))
    job_location = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="job-area"]')))
    job_salary = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="red"]')))
    #job_release_data = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="format-time"]')))
    for a,b,c,d,e,f in zip(job_title,job_url,job_company_name,job_company_url,job_location,job_salary):
        f = f.text
        try:
            max_salary = re.findall(r"\d+",f,)[1]+'000'
        except:
            max_salary = f
        dict = {
            "job_sourse":"2",
            "job_title":a.get_attribute('title'),
            "job_url":b.get_attribute('href'),
            "job_company_name":c.get_attribute('title'),
            "job_company_url":d.get_attribute('href'),
            "job_location":e.text,
            "job_salary":f,
            "job_max_salary":max_salary,
            "job_min_salary":f[:f.index('-')]+'000',
            "job_release_data":'',
            "job_collect_data":"2020-7-10"
                                 }
        with open('boss_data.json', 'a+',encoding='utf-8') as f:
                   dict = json.dumps(dict,ensure_ascii=False)
                   f.write(dict+'\n')    
    try:                 
# 点击下一页，等待页面加载完
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="page"]//a[@ka="page-next"]')))
# 下一页的按钮
        next_tag = web.find_element_by_xpath('//div[@class="page"]//a[@ka="page-next"]')
# 按钮变灰，没有下一页，会出现‘pager_next_disabled’属性
        if 'next disabled' in next_tag.get_attribute('class'):
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
    jobnames = ['web前端','数据分析师','大数据','java开发','数据分析师']
    citys = ['c101121500','c101120100','c101120200','c101120300','c101121400','c101121200','c101120500','c101120600','c101121300',
        'c101120900','c101120400']
    a = 'https://www.zhipin.com/'
    url_list = [ a+j+'/?query='+i for i in jobnames for j in citys]
    chromeOptions = Options()
    ip_one = get_ip()
    for url in url_list[45:]:        
        chromeOptions.add_argument("--proxy-server=http://"+ip_one)
        web = Chrome(options = chromeOptions)
        wait = WebDriverWait(web,8)#设置等待时间 
        web.get(url)
        time.sleep(1)
        flag = 1
        count = 0 
        while flag==1:
            count += 1
            print('已爬取第%d页'%count)
            try:    
                flag = run()
            except Exception as e:
                print(e)
                print(url)
                time.sleep(10)                 
        if flag==0:
            web.close()

    


# In[ ]:




