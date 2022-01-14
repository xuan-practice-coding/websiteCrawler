# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 13:45:40 2021
Last modified on Thur Jul 22 17:10:30 2021
@author: Xuan Chen (Lydia)
"""

# from urllib import request  
from urllib.request import urlopen, HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup  
# import re
import requests
import pandas as pd

# from pytube import YouTube
# import youtube_dl 

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
        
# obtain a list of all internal video links in a webpage  
def get_video_link(inputUrl): 
    allVideoLinks = []
    response = requests.get(inputUrl, headers = headers)
    html = response.content
    bsObj = BeautifulSoup(html, "html.parser")
    
    for link in bsObj.findAll("iframe"): 
        video_links1 = {}
        video_links2 = {}
        
        if link.get('src') != None:
            video_links1['video_url'] = link.get('src')
            video_links1['from_page'] = inputUrl
            allVideoLinks.append(video_links1)
        
        if link.get('data-src') != None:
            video_links2['video_url'] = link.get('data-src')
            video_links2['from_page'] = inputUrl
            allVideoLinks.append(video_links2)
            
    return allVideoLinks
        # videoUrl_src = link.get('src')
        # videoUrl_data_src = link.get('data-src')
        # if videoUrl_src is not None:
            # if videoUrl_src not in allVideoLinks:
            #     allVideoLinks.append(videoUrl_src)
            # video_links1['video_url'] = videoUrl_src
            # video_links1['from_page'] = inputUrl
            # if video_links1 not in allVideoLinks:
            # allVideoLinks.append(video_links1)
        if videoUrl_data_src is not None:
            # allVideoLinks.append(videoUrl_data_src)
            video_links2['video_url'] = videoUrl_data_src
            video_links2['from_page'] = inputUrl
            # if video_links2 not in allVideoLinks:
            # allVideoLinks.append(video_links2)
            # print(video_links2)
            # print(allVideoLinks)
    # return allVideoLinks


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

# get all links from screamfrog output
df_int = pd.read_csv(target_path+'internal_html.csv')
allIntLinks = df_int["Address"].tolist()

allVideos = []
for url in allIntLinks:
    int_video_link = []
    int_video_link = get_video_link(url)
    for item in int_video_link:
        # if info_dic not in allVideos:
        allVideos.append(item)

# save_lst=list(allVideoLinks)
# save_lst.sort()
# save_csv = pd.DataFrame(save_lst, columns = ['media_url'])
# save_csv.to_csv(target_path +'allVideoLinks_0819_withurl.csv', mode="a", line_terminator="\n", encoding = 'utf-8')

# allVideoLinks = []
# for item in int_video_link:
#     if len(item) == 2:
#         allVideoLinks.append(item)

import csv

log_file = 'E://DEI//Crawler_Code//test_dir//lusbrands.com//allVideoLinks_0819_withpage.csv'
csv_fields = ['from_page', 'video_url']

with open(log_file, "w", newline = '', encoding = "utf-8") as fd:
    csv_writer = csv.DictWriter(fd, fieldnames = csv_fields)
    csv_writer.writeheader()

    for video_links in allVideos:
        try:
            csv_row = {}
            csv_row['from_page'] = video_links['from_page']
            csv_row['video_url'] = video_links['video_url']
        except Exception as e:
            print("Exception encountered")
            print(str(e))
            pass
        csv_writer.writerow(csv_row)

# for videolink in allVideoLinks:
#     gaa.save_video_from_link(videolink, target_path)
