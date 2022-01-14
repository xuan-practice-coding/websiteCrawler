# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 13:45:40 2021
Last modified on Thur Jul 22 17:10:30 2021
@author: Xuan Chen (Lydia)
"""


import os, re, requests
import pandas as pd
from urllib.parse import urlparse
from bs4 import BeautifulSoup  
from advertools import crawl # advertools library for SEO, use to get all internal links


class Models:
    
    # Initial the extractor for each url
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        

class Extrat_all_links:
    
    # # Initial the extractor for each url
    def __init__(self, models):
        self.models = models
        # collect all the links on the website  
        self.allExtLinks = set()
        self.allIntLinks = set()
        self.allLinks = set()
    
    # obtain a list of all internal links in a webpage  
    def getInternalLinks(self, inputUrl, domainName):   
        internalLinks = []
        filename = domainName+'.jl'
        crawl(inputUrl, filename, follow_links = True, 
              # css_selectors={'sidebar_links': '.toctree-l1 .internal::text',
              #            'sidebar_links_url': '.toctree-l1 .internal::attr(href)'},
              # xpath_selectors={'sidebar_links': '//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]/text()',
              #              'sidebar_links_url': '//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]/@href'}
              # custom_settings={
              #     'USER_AGENT': 'custom-user-agent'}
              )
        website_info = pd.read_json(filename, lines = True)
        if 'errors' in website_info.columns: 
            internalLinks = website_info.loc[website_info['errors'].isnull()]['url'].tolist()
        else:
            internalLinks = website_info['url'].tolist()
        return internalLinks
      
    # obtain a list of all external links in a webpage
    def getExternalLinks(self, bsObj, excludeUrl):  
        externalLinks = []
        # find links start with "http" or "www", and not contain the target domain URL
        regex_ex = r"(http|www)((?!(%s)).)*$" % excludeUrl
        for link in bsObj.findAll("a", href = re.compile(regex_ex)):  
            if link.attrs['href'] is not None: 
                if re.match('.*\.(pdf|jpg|png|mp4|mp3)$', link.attrs['href']): 
                    pass
                else:
                    if re.match(regex_ex, link.attrs['href']) != None:
                        if link.attrs['href'] not in externalLinks:  
                            externalLinks.append(link.attrs['href'])
                    # else:
                    #     pass
        return externalLinks
    
    def getAllLinks(self, siteUrl):
        domain = urlparse(siteUrl).netloc.lstrip('www.')

        internalLinks_lst = self.getInternalLinks(siteUrl, domain)
        self.allIntLinks = set(internalLinks_lst)
        
        for url in internalLinks_lst:  
            response = requests.get(url, headers = self.models.headers)
            html = response.content
            bsObj = BeautifulSoup(html, "html.parser")

            externalLinks_lst = self.getExternalLinks(bsObj, domain)
            #collect the external links
            for link in externalLinks_lst:
                # req = requests.get(url, headers = self.models.headers)
                # if req.status_code == 200:
                    if link not in self.allExtLinks:
                        self.allExtLinks.add(link)
                        # print("Found an external URL: "+link)
                # else:
                #     pass
        self.allLinks = set.union(self.allIntLinks, self.allExtLinks)
        return self.allLinks, self.allIntLinks, self.allExtLinks


if __name__ == "__main__":
    
    project_path = "E://DEI//01_coding_test_dir//"
    
    website_lst = [
        # 'https://lusbrands.com',
        # 'https://insurance-supermarket.ca/',
        # 'https://canada-life-insurance.org/',
        'https://realreason.ca/kory/',
        ]
    
    models = Models()
    print("extracting......")

    for item in website_lst:
        
        ext = Extrat_all_links(models)
        
        project_folder = project_path + urlparse(item).netloc +'//'
        folder = os.path.exists(project_folder)
        if not folder:
            os.makedirs(project_folder)

        allLinks, allIntLinks, allExtLinks = ext.getAllLinks(item)
        
        allLinks_csv = pd.DataFrame(list(allLinks), columns = ['Address'])
        allIntLinks_csv = pd.DataFrame(list(allIntLinks), columns = ['Address'])
        allExtLinks_csv = pd.DataFrame(list(allExtLinks), columns = ['Address'])
        allLinks_csv.to_csv(project_folder +'allLinks.csv', mode="a", line_terminator="\n", encoding = 'utf-8')
        allIntLinks_csv.to_csv(project_folder +'allIntLinks.csv', mode="a", line_terminator="\n", encoding = 'utf-8')
        allExtLinks_csv.to_csv(project_folder +'allExtLinks.csv', mode="a", line_terminator="\n", encoding = 'utf-8')
