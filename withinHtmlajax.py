# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 18:33:36 2021

@author: Xuan Chen (Lydia)
"""


# from urllib import request
# from urllib.request import urlopen  
# from bs4 import BeautifulSoup  
# import wget
# from PIL import Image
# from fpdf import FPDF
import pandas as pd
import os, sys, re, json, csv, time, math
from time import sleep
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--hide-scrollbars')
chrome_path = "E://DEI//Crawler_Code//chromedriver.exe"

rstr = r"[\/\\\:\*\?\"\<\>\|]"

main_path = 'E://DEI//Crawler_Code//test_dir//lusbrands.com//'
review_path = 'E://DEI//Crawler_Code//test_dir//lusbrands.com//reviews//'

df_int = pd.read_csv(main_path + 'allIntLinks.csv')
df_int = df_int[df_int['Status Code'] == 200]
df_int["suffix"] = df_int.Address.apply(lambda x: x.split('/')[-1])
allIntLinks = df_int[["Address", "suffix"]]
allIntLinks = allIntLinks.sort_values('Address')
allIntLinks.reset_index(drop=True, inplace=True)

url_lst = allIntLinks['Address'][110:148].append(allIntLinks['Address'][175:205])
url_lst = url_lst.tolist()

def mkdir(test_path, url):
    sub_folder = re.sub(rstr, '_', urlparse(url).path.strip('/'))
    html_path = review_path + sub_folder +'//'
    folder = os.path.exists(html_path)
    if not folder: # check if the main project folder exsits
        os.makedirs(html_path)
    return html_path

# def web_screen_shot(url, png_name, path):
#     driver = webdriver.Chrome(executable_path = chrome_path, 
#                               chrome_options = chrome_options)
#     driver.implicitly_wait(3)
#     driver.get(url)
#     sleep(1)
#     scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
#     lastHeight = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         # driver.execute_script("window.scrollTo(0,3350)")
#         time.sleep(0.2)
#         try:
#             driver.find_element(By.CSS_SELECTOR, "path:nth-child(3)").click()
#         except:
#             pass
#         time.sleep(0.2)
#         newHeight = driver.execute_script("return document.body.scrollHeight")
#         if newHeight == lastHeight:
#              break
#         lastHeight = newHeight
#     driver.set_window_size(scroll_width, lastHeight)
#     read_more = []
#     try:
#         read_more = driver.find_elements_by_xpath("//span[contains(.,\'...Read More\')]")
#         for element in read_more:
#             element.click()
#             time.sleep(1)
#     except:
#         pass
#     save_path2 = os.path.join(path, png_name)
#     driver.save_screenshot(save_path2)    
#     driver.quit()

for url in url_lst:
    driver = webdriver.Chrome(executable_path = chrome_path, chrome_options = chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)
    scroll_width = driver.execute_script('return document.body.scrollWidth')
    lastHeight = driver.execute_script("return document.body.scrollHeight")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "path:nth-child(3)").click()
        time.sleep(1)
    except:
        pass
    
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
          break
    lastHeight = newHeight
    driver.set_window_size(scroll_width, lastHeight)
    
    try:
        element = driver.find_element_by_class_name("reviews-amount")
    except:
        continue
    
    i = int(element.text.split(' ')[0])
    path1 = mkdir(review_path, url)
    
    while j <= math.ceil(i/5):
        url_sub = url + '?yoReviewsPage=' + str(j)
        png_name = str(j)+'.png'
        scrollWidth = []
        scrollHeight = []
        scrollWidth_new = []
        scrollHeight_new = []
        read_more1 = []
        read_more2 = []
        read_more3 = []
        read_more4 = []
        read_more = []
        driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
        driver.set_window_size(800, 1080)
        driver.get(url_sub)
        driver.implicitly_wait(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        try:
            driver.find_element(By.CSS_SELECTOR, "path:nth-child(3)").click()
            time.sleep(1)
        except:
            pass

        try:
            read_more1 = driver.find_elements_by_xpath("//span[contains(.,\'...Read More\')]")
            read_more4 = driver.find_elements_by_xpath("//span[contains(.,\'...Read.More\')]")
            read_more2 = driver.find_elements_by_css_selector('span.yotpo-read-more')
            read_more3 = driver.find_elements_by_class_name('yotpo-read-more')
            read_more = read_more1 + read_more2 + read_more3 + read_more4
            for element in read_more:
                element.click()
                time.sleep(1)
        except:
            pass
        
        scrollWidth_new = driver.execute_script('return document.body.scrollWidth') #parentNode
        scrollHeight_new = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(scrollWidth_new, scrollHeight_new)
        save_path2 = os.path.join(path1, png_name)
        driver.save_screenshot(save_path2)
        
        j += 1
        driver.quit()
