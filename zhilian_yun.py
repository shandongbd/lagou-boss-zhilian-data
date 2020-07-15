#!/usr/bin/env python
# coding: utf-8
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pymysql
import json
import re
import threading
from selenium.webdriver import ActionChains
def get_track():      # distance为传入的总距离
    # 移动轨迹
    distance = 258
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=258*4/5
    # 计算间隔
    t=0.2
    # 初速度
    v=0

    while current<distance:
        if current<mid:
            # 加速度为2
            a=3
        else:
            # 加速度为-2
            a=-2
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
    return track
def get_data(urls):
    chromeOptions = Options()
    # 下面代码为避免网站对selenium的屏蔽  =======无头模式已开启
    chromeOptions.add_argument('--disable-dev-shm-usage')
    chromeOptions.add_argument('--no-sandbox') 
    chromeOptions.add_argument('--headless')
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    count = 0
    db = pymysql.connect("119.3.184.238","guest","guest","jobs")# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    for i in urls:
        i = i.replace('\n','')
        count += 1
        print("====正在处理第%d条数据===="%count)
        print(i)
        try:
            web = Chrome(options=chromeOptions)
            web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
               "source": """
                 Object.defineProperty(navigator, 'webdriver', {
                   get: () => undefined
                   })
                    """
                })
            wait = WebDriverWait(web,3)#设置等待时间 
            web.get(i)
            time.sleep(0.5)
            try:
               action = ActionChains(web)
               source=web.find_element_by_xpath("//*[@id='nc_1_n1z']")#需要滑动的元素
               action.click_and_hold(source).perform()
               tracks = get_track()
               for x in tracks:
                 action.move_by_offset(xoffset=x,yoffset=0).perform()
               time.sleep(0.5)
               action.release().perform() 
               time.sleep(0.1)
            except:
               pass
        #获取数据
            job_title = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//h3[@class="summary-plane__title"]')))
            job_company_name = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="company"]/a')))
            job_company_url = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="company"]/a')))
            job_location = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//ul[@class="summary-plane__info"]/li/a')))
            job_salary = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="summary-plane__salary"]')))
            job_release_data = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="summary-plane__time"]')))
       # for a,b,c,d,e,f,g in zip(job_title,job_url,job_company_name,job_company_url,job_location,job_salary,job_release_data):
            f = job_salary[0].text 
            max_salary = 0 
            min_salary = 0
            if '万' in f[:f.index('-')]:  #最小单位为万
                f = f.replace('万','0千')
                max_salary = re.findall(r"\d+",f,)[1]+'000'
                min_salary = re.findall(r"\d+",f,)[0]+'000'  
                if '.' in f[:f.index('-')]: #处理最小工资为小数
                    f = f.replace('.','',1)
                    f = f.replace('0千','千',1)
                    min_salary = re.findall(r"\d+",f,)[0]+'000'  
                if  '.' in f[f.index('-'):]:  #处理最大工资为小数
                    f = f.replace('.','',1)  
                    f = f.replace('0千','千',1)
                    max_salary = re.findall(r"\d+",f,)[0]+'000' 
            elif '万' in f[f.index('-'):]:  #如果最大工资单位为万
                    f = f.replace('万','0千')
                    max_salary = re.findall(r"\d+",f,)[1]+'000'
                    min_salary = re.findall(r"\d+",f,)[0]+'000' 
                    if '.' in f[:f.index('-')]:
                        f = f.replace('.','',1)  #处理工资为小数
                        min_salary = re.findall(r"\d+",f,)[0]+'00'
                    if '.' in f[f.index('-'):]:
                        f = f.replace('.','',1) 
                        f = f.replace('0千','千',1)
                        max_salary = re.findall(r"\d+",f,)[1]+'000'                    
            else:   #工资单位都为一千
                    max_salary = re.findall(r"\d+",f,)[1]+'000' 
                    min_salary = re.findall(r"\d+",f,)[0]+'000'
                    if '.' in f[:f.index('-')]:
                            a = f.replace('.','',1)
                            min_salary = re.findall(r"\d+",a,)[0]+'00'
                    if '.' in f[f.index('-'):]:
                            a = f[f.index('-'):].replace('.','',1)
                            max_salary = re.findall(r"\d+",a,)[0]+'00'   
            g = job_release_data[0].text
            try:
                text = re.findall(r"\d+月\d+日",g,)[0]
                g_1 = re.findall(r"\d+月",g,)[0]
                g_2 = re.findall(r"\d+日",g,)[0]
                g = '2020'+'-'+g_1+'-'+g_2
            except Exception as e:
                print(e)
                g = '2020-7-14'
            dict = {
                "job_sourse":"4",
                "job_title":job_title[0].text,
                "job_url":i,
                "job_company_name":job_company_name[0].text,
                "job_company_url":job_company_url[0].get_attribute('href'),
                "job_location":job_location[0].text,
                "job_salary":f,
                "job_max_salary":max_salary,
                "job_min_salary":min_salary,
                "job_release_data":g,
                "job_collect_data":"2020-7-15"
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
            with open('/root/Python/zhilian_data_0714.json', 'a+',encoding='utf-8') as f:  #本地也保留一份 
                dict = json.dumps(dict,ensure_ascii=False)
                f.write(dict+'\n')
                f.close()
            web.close()
        except :
            print(i+'哎呀，这个页面获取失败了！')
            web.close()
    db.close()

if __name__ == '__main__':         
    f = open("/root/Python/urls_data_0714.json","r")
    url_list = f.readlines()
    i = int(len(url_list))/6
    url_list1 = url_list[:1119]
    url_list2 = url_list[1119:2*1119]
    url_list3 = url_list[2*1119:3*1119]
    url_list4 = url_list[3*1119:4*1119]
    url_list5 = url_list[4*1119:5*1119]
    url_list6 = url_list[5*1119:6*1119]


# 开启线程
    # 开启合适的线程个数 接受分配好的任务
    th1 = threading.Thread(target=get_data, args=(url_list1,))
    th2 = threading.Thread(target=get_data, args=(url_list2,))
    th3 = threading.Thread(target=get_data, args=(url_list3,))
    th4 = threading.Thread(target=get_data, args=(url_list4,))
    th5 = threading.Thread(target=get_data, args=(url_list5,))
    th6 = threading.Thread(target=get_data, args=(url_list6,))

    # 开启线程
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()

    # 线程等待 保证每个线程可以在主线程结束前结束
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    th5.join()
    th6.join()
