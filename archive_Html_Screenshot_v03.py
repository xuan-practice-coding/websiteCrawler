# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 21:25:55 2021

@author: Xuan Chen (Lydia)
"""


import os, re, requests
import pandas as pd
from time import sleep
from advertools import crawl
from urllib.parse import urlparse
from bs4 import BeautifulSoup  
from PIL import Image
from fpdf import FPDF
# from obtain_all_links_v03 import Extrat_all_links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--hide-scrollbars')
chrome_path = "E://DEI//01_coding_project//website_crawler//chromedriver.exe"


class Models:
    
    # Initial the extractor for each url
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        
        
class Archive_to_database:
    
    # Initial the extractor for each url
    def __init__(self, models):
        self.models = models
        self.allIntLinks = set()
        self.target_path = ''
        self.html_arch = ''
        self.url_title = ''
    
    def getHtml(self, url):
        response=requests.get(url, headers=self.models.headers)
        # if response.status_code == 200:
        cont = response.text.encode('utf-8')
        self.html_arch = BeautifulSoup(cont, 'html.parser')
        return self.html_arch
    
    def chrome_screen_shot(self, url, png_name, path):
        driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
        driver.get(url)
        sleep(1)
        scroll_width = driver.execute_script('return document.body.scrollWidth')
        scroll_height = driver.execute_script('return document.body.scrollHeight')
        driver.implicitly_wait(5)
        driver.execute_script("window.scrollTo(0, 1500);")
        sleep(2)
        driver.set_window_size(scroll_width, scroll_height)
        save_path = os.path.join(path, png_name)
        driver.save_screenshot(save_path)     
        driver.quit()
    
    def screenshots_crop_to_pdf(self, jpg_path, file_name):  
        files = os.listdir(jpg_path)
        # files.sort()
        imgFiles = [] 
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                imgFiles.append(jpg_path + file)
        pdf = FPDF('P', 'in', 'Letter') 
        pdf.set_auto_page_break(0)
        for image in imgFiles:
            fp = open(image, 'rb')
            img = Image.open(fp)
            width, height = img.size
            width_in, height_in = float(width*0.0104166667), float(height*0.0104166667)
            num = int(height_in/10)+1
            pdf_size = {'w': 8.5, 'h': 11}
            if height_in <= 10:
                pdf.add_page()
                pdf.image(image, x=0.5*(8.5-width_in), y=0.5, w=width_in)
            else:
                i = 0
                while i < num:
                    if i < num - 1:
                        box = (0, 950*i, 800, 950*i+950)
                        h1 = 950
                    else:
                        box = (0, 950*i, 800, height)
                        h1 = height%950
                    img_c = img.crop(box)
                    pdf.add_page()
                    pdf.image(img_c, x=0.5*(8.5-width_in), y=0.5, w=width_in) #h=h1*0.0104166667) *(8.5-width_in)
                    i += 1
            fp.close()
        pdf.output(jpg_path + file_name, 'F')
        
    def mkdir(self, project_folder, url):
        sub_folder_path = []
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        main_folder = urlparse(url).netloc
        project_path = project_folder + main_folder +'//'
        folder = os.path.exists(project_path)
        if not folder: # check if the main project folder exsits
                os.makedirs(project_path)
        sub_path = urlparse(url).path.strip('/')
        if sub_path.count('/') != 0:
            sub_folder_path = project_path
            while sub_path.count('/') >= 1:   # create folders according to the url structure
                sub_folder_name = sub_path.partition('/')[0]
                sub_folder_path = sub_folder_path + sub_folder_name +'//'
                folder = os.path.exists(sub_folder_path)
                if not folder: # check if the folder exsits
                    os.makedirs(sub_folder_path)   
                sub_path = sub_path.partition('/')[2]
                # target_path = target_path
                self.target_path = sub_folder_path
                self.url_title = re.sub(rstr, "_", sub_path)
        else:
            self.target_path = project_path
            if len(sub_path) == 0:
                self.url_title = 'main_page'
            else:
                self.url_title = re.sub(rstr, "_", sub_path)
        return self.target_path, self.url_title
    
    def saveHtml(self, path, filename, html_content):
        # rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        # file_name = re.sub(rstr, "_", url.lstrip('http(s)?://').rstrip('/'))  # replace with '_'
        # file_name = id_tag + filename # limit the length of the file name
        with open(path + filename + ".html.txt", "w", encoding = "utf-8") as f:
            f.write(html_content)
    
    def getAllInternalLinks(self, inputurl, inputdomain):
        filename=inputdomain+'.jl'
        crawl(inputurl, filename, follow_links=True)
        website_info = pd.read_json(filename, lines=True)
        self.allIntLinks = set(website_info["url"].tolist())
        return self.allIntLinks
    
    def png_to_jpg(self, folderPath):  
        mainfolder = os.walk(folderPath)
        sub_folder_path = folderPath + 'screenshots_jpg//'
        folder = os.path.exists(sub_folder_path)
        if not folder:    
            os.makedirs(sub_folder_path)  
        # filelist = os.listdir(folderPath)
        for path, dir, filelist in mainfolder:
            for filename in filelist:
                if filename.endswith('png'):
                    save_name = sub_folder_path + re.sub('_', '.', str(filename).rstrip('.png')) + '.jpg'
                    im = Image.open(path +'/' + filename)
                    new_i = im.convert('RGB')
                    new_i.save(save_name, 'JPEG', optimize=True, quality=90)
        return sub_folder_path
 
if __name__ == '__main__':
    
    project_path = "E://DEI//01_coding_test_dir//"
    
    website_lst = [
        # 'https://lusbrands.com',
        # 'https://insurance-supermarket.ca/',
        # 'https://canada-life-insurance.org/',
        'https://realreason.ca/kory/',
        ]
    project_folder = project_path + urlparse(website_lst[0]).netloc +'//'
    
    models = Models()
    # ext = Archive_to_database(models)
    print("Start archiving......")
    
    # get all links from saved cvs from obtain_all_links_v3.py
    # allLinks, allIntLinks, allExtLinks = ext.getAllLinks(item)
    df_int = pd.read_csv(project_folder + 'allIntLinks.csv')
    allIntLinks = df_int["Address"].tolist()
    allIntLinks.sort()
    df_ext = pd.read_csv(project_folder +'allExtLinks.csv')
    allExtLinks = df_ext["Address"].tolist()
    allExtLinks.sort()
    # allLinks = allIntLinks + allExtLinks

    for item in website_lst:
        project_folder = project_path + urlparse(item).netloc +'//'
        # initialize the class
        arc = Archive_to_database(models)
        # ext = Extrat_all_links(models)
        
        print('start archiving html and screen shots for %s internal links......' % urlparse(item).netloc)
        index_number = 0
        for url in allIntLinks:
            internal_folder_path = project_folder + 'int_page//'
            subfolder_path, url_title = arc.mkdir(internal_folder_path, url)
            # archive html
            html_arch = arc.getHtml(url)
            filename = '%04d_' % index_number + url_title
            arc.saveHtml(subfolder_path, filename, str(html_arch))
            # archive screen shot
            screenshot_name = filename + '.png'
            arc.chrome_screen_shot(url, screenshot_name, subfolder_path)
            index_number += 1
        
        print('start archiving html and screen shots for %s external links......' % urlparse(item).netloc)
        index_number = 0
        for url in allExtLinks:
            external_folder_path = project_folder + 'ext_page//'
            subfolder_path, url_title = arc.mkdir(external_folder_path, url)
            # archive html
            html_arch = arc.getHtml(url)
            filename = '%04d_' % index_number + url_title
            arc.saveHtml(subfolder_path, filename, str(html_arch))
            # archive screen shot
            screenshot_name = filename + '.png'
            arc.chrome_screen_shot(url, screenshot_name, subfolder_path)
            index_number += 1
            
        # merge all internal screen shots to one pdf
        print('start converting png to jpg......')
        sub_folder_path = arc.png_to_jpg(internal_folder_path)
        print('start making pdf for %s......' % urlparse(item).netloc)
        arc.images_to_pdf('internal_page.pdf', sub_folder_path)
        
        # merge all external screen shots to one pdf
        print('start converting png to jpg......')
        sub_folder_path = arc.png_to_jpg(external_folder_path)
        print('start making pdf for %s......' % urlparse(item).netloc)
        arc.images_to_pdf('external_page.pdf', sub_folder_path)
