
#!/usr/bin/python3
#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

import img
import cv2
import numpy as np
import pic_save
import re
import time
import random
import traceback
import requests


def auto_drag(browser,distance):
    element = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div[3]")

    # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
    #distance -= element.size.get('width') / 2
    distance=distance *0.7714
    has_gone_dist = 0
    remaining_dist = distance
    #distance += randint(-10, 10)

    # 按下鼠标左键
    ActionChains(browser).click_and_hold(element).perform()
    time.sleep(0.1+random.randint(-10,20)/100)
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        rand_ratio=random.randint(100, 150) / 100

        if ratio < 0.15:
            # 开始阶段移动较慢
            span = random.randint(3,8)
        elif ratio < 0.35:
            # 结束阶段移动较慢
            span = random.randint(10,15)
        elif ratio < 0.55:
            # 结束阶段移动较慢
            span = random.randint(12, 18)
        elif ratio > 0.8:
            # 结束阶段移动较慢
            span = random.randint(10, 15)
            rand_ratio=1
        else:
            # 中间部分移动快
            span = random.randint(15, 25)
        ActionChains(browser).move_by_offset(span*rand_ratio, random.randint(-6, 6)).perform()
        remaining_dist -= span*rand_ratio
        has_gone_dist += span*rand_ratio
        time.sleep(random.randint(1,20)/100)

    ActionChains(browser).move_by_offset(remaining_dist, random.randint(-3, 3)).perform()
    time.sleep(random.randint(100, 200) / 100)

    ActionChains(browser).release(on_element=element).perform()

def verify(chrome):
    izsz = 1
    url = chrome.current_url
    # print(url)
    if 'https://passport.jd.com/new/login.aspx?' in str(url):
        izsz = 1
        # print("is","=1")
    else:
        izsz = 0
        return izsz

    try:
        # 获取图片
        big_img_url_org=[]
        big_img_url=[]
        filename=[]
        big_img_url_org = chrome.find_element_by_class_name("JDJRV-bigimg").find_element_by_tag_name("img").get_attribute("src")
        # print(big_img_url)
        big_img_url = re.findall(r"data:image/png;base64,(.+)", big_img_url_org)
        # print(big_img_url)
        # print(big_img_url.screenshot_as_base64)
        filename = pic_save.get_picture(big_img_url[0])
        print(filename)
        if filename:
            big_img = cv2.imread(filename)
            dis, _ = img.calculate_distance(big_img)
            auto_drag(chrome, dis)


            if WebDriverWait(chrome,2,0.2).until(EC.title_contains(u"JD.COM")):
                izsz = 0
            else:
                izsz=  1

            #cv2.waitKey()
    except Exception as e :

        #print('str(Exception):\t',Exception ,"_",e)
        if  "Unable to locate element"  in str(e):
            izsz = 0
        else:
            izsz =1
    return izsz


def login( chrome):
    # 下面填入京东的用户名以及密码
    jd_up = {"ue": "***********", "pd": "***********"}
    chrome.get(url="https://passport.jd.com/new/login.aspx?")

    chrome.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div/div[3]/a").click()
    # chrome.find_element_by_xpath("//*[@id='content']/div/div[1]/div/div[2]/a").click()
    User = chrome.find_element_by_id("loginname")
    User.clear()
    User.send_keys(jd_up["ue"])
    Passwd = chrome.find_element_by_id("nloginpwd")
    Passwd.clear()
    Passwd.send_keys(jd_up["pd"])
    chrome.find_element_by_id("loginsubmit").click()
    #这里是不是可以sleep一下然后手动填上验证码，下面就对验证后的页面进行处理就可以，找元素定位什么的


    while verify(chrome)==1:
        time.sleep(random.randint(100, 200) / 100)
        print("重试...")

    print("登录成功...")
    # 从driver中获取cookie列表（是一个列表，列表的每个元素都是一个字典）
    mycookie = chrome.get_cookies()
    #这个和我直接用浏览器把那所有cookie赋值到requests中有什么区别
    return mycookie

#获得了cookie之后，使用requests操作
def spyder_do(cookies,sess):
    for cookie in cookies:
        sess.cookies.set(cookie['name'],cookie['value'])
    resp=sess.get("https://home.jd.com/")
    resp.encoding = 'utf-8'
    print('status_code = {0}'.format(resp.status_code))
    # 将网页内容存入文件
    #with open('html.txt','w+') as  fout:
        #fout.write(resp.text)
    stock=sess.get("https://item.jd.com/****************.html")


if __name__ == '__main__':


    chrome = webdriver.Chrome()
    chrome.implicitly_wait(2)

    cookies=login(chrome)
    s = requests.Session()
    spyder_do(cookies,s)

    exit(0)
    while True:
        try:
           
            try:
                chrome.get(url="https://item.jd.com/***********.html")#模拟购买的商品ID
            except TimeoutException:
                print('！！！！！！time out after 20 seconds when loading page！！！！！！')
                # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
                #chrome.execute_script("window.stop()")

            chrome.find_element_by_id("InitCartUrl").click()
            print(6)

            chrome.get(url="https://cart.jd.com/cart.action")
            print(7)

            print(8)
            WebDriverWait(chrome, 10, 0.5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'submit-btn'))).click()
            #chrome.find_element_by_class_name("submit-btn").click()
            print(9)

            WebDriverWait(chrome, 10, 0.5).until(
                EC.presence_of_element_located((By.ID, 'order-submit'))).click()
            #chrome.find_element_by_id("order-submit").click()
            print(10)

            print("Success...")

            #chrome.quit()
            break
        except Exception as e:
            print("Try Again... ", e)






##-----------------------------------------------------------------
def normal_drag(dis):
    # 滑块验证   /html/body/div[4]/div/div/div/div[2]/div[3]
    slider = chrome.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div[3]")

    # slider=chrome.find_element_by_class_name(r"JDJRV-slide-inner JDJRV-slide-btn")# 找到“蓝色滑块”
    action = ActionChains(chrome)  # 实例化一个action对象
    action.click_and_hold(slider).perform()  # perform()用来执行ActionChains中存储的行为
    action.reset_actions()
    action.move_by_offset(dis*0.7714, 0).perform()  # 移动滑块
    action.release().perform()