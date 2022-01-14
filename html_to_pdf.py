# coding=utf-8

import os, re, requests, logging
from time import sleep
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
# from PyPDF2 import PdfFileMerger

import pdfkit # not able to customize page size, only certain patterns
config = pdfkit.configuration(wkhtmltopdf='D://Program Files//wkhtmltopdf//bin//wkhtmltopdf.exe')

import pdfcrowd, sys # need to registed
from PIL import Image
from fpdf import FPDF
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_path = "E://DEI//01_coding_project//website_crawler//chromedriver.exe"

html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
        {content}
        </body>
        </html>
    """


def parse_url_to_html(url, name):
    """
    Parse URL, return HTML content
    :param url: Parsed url
    :param name: file name of saved html
    :return: html
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Main Body
        body = soup.find_all(class_="x-wiki-content")[0]
        # Title
        title = soup.find('h4').get_text()

        # The title is added to the front of the text and displayed in the center
        center_tag = soup.new_tag("center")
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        html = str(body)
        # change the relative path of the img src tag to absolute path
        pattern = "(<img .*?src=\")(.*?)(\")"

        def func(m):
            if not m.group(3).startswith("http"):
                rtn = m.group(1) + "http://www.liaoxuefeng.com" + m.group(2) + m.group(3)
                return rtn
            else:
                return m.group(1)+m.group(2)+m.group(3)
        html = re.compile(pattern).sub(func, html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        with open(name, 'wb') as f:
            f.write(html)
        return name

    except Exception as e:

        logging.error("Parsing error", exc_info=True)

def get_url_list():
    """
    obtain all the URL and save to list
    :return:
    """
    response = requests.get("www.dei.ca")
    soup = BeautifulSoup(response.content, "html.parser")

    #menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
    menu_tag = soup.find_all(class_="x-wiki-index-item")[1]
    urls = []
    for li in menu_tag.find_all("li"):
        url = "http://www.liaoxuefeng.com" + li.a.get('href')
        urls.append(url)
    return urls

def web_to_pdf(url, file_name):
    """
    save all the html files to pdf
    :param htmls:  html file list
    :param file_name: pdf file name
    :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        # 'custom-header': [
        #     ('Accept-Encoding', 'gzip')
        # ],
        # 'cookie': [
        #     ('cookie-name1', 'cookie-value1'),
        #     ('cookie-name2', 'cookie-value2'),
        # ],
        'outline-depth': 10,
        'load-error-handling': 'ignore',
        'javascript-delay':'10000',
        # 'no-stop-slow-scripts':"true"
    }
    pdfkit.from_url(url, file_name, options=options, configuration=config)

def html_to_pdf(html, file_name):
    """
    save all the html files to pdf
    :param htmls:  html file list
    :param file_name: pdf file name
    :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        # 'custom-header': [
        #     ('Accept-Encoding', 'gzip')
        # ],
        # 'cookie': [
        #     ('cookie-name1', 'cookie-value1'),
        #     ('cookie-name2', 'cookie-value2'),
        # ],
        'outline-depth': 10,
        'load-error-handling': 'ignore',
        'javascript-delay':'10000',
    }
    css = ''
    pdfkit.from_file(html, file_name, options=options, configuration=config, css=css)

def webpage_to_single_page_pdf(url, path, file_name):
    print_time = datetime.now().strftime("%b " + "%d, "+"%Y "+"%X")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)
    sleep(2)
    scroll_width = driver.execute_script('return document.body.scrollWidth') #parentNode
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 1400);")
    sleep(3)
        
    paper_height = int(scroll_height * 0.0104166667) + 3.32 + 2*1*0.393701
    paper_width = scroll_width * 0.0104166667 + 2*1*0.393701
    driver.set_window_size(scroll_width, scroll_height)
    pdf = driver.execute_cdp_cmd("Page.printToPDF", 
                                 {'printBackground': True,
                                  'displayHeaderFooter': True,
                                  'paperHeight': paper_height,
                                  'paperWidth': paper_width,
                                  'headerTemplate':"<span style='font-size:12px'><span style='display:inline-block;width:38px;'></span><span>%s</span><span style='display:inline-block; width: 20px;'></span><span class=title></span></span>" % print_time,
                                  'footerTemplate':"<span style='font-size:12px'><span style='display:inline-block;width:38px;'></span><span class=url></span></span>",
                                  'marginBottom': 0.51,
                                  })
    with open(path + file_name, "wb") as f:
        f.write(base64.b64decode(pdf['data']))
    driver.quit()

def html_to_single_page_pdf(html, path, file_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
    driver.implicitly_wait(3)
    file_path = 'file://' + path + html
    driver.get(file_path)
    sleep(1)
    scroll_width = driver.execute_script('return document.body.scrollWidth') #parentNode
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 1400);")
    sleep(3)
        
    paper_height = int(scroll_height * 0.0104166667)+3.5 + 2*1*0.393701
    paper_width = scroll_width * 0.0104166667 + 2*1*0.393701
    pdf = driver.execute_cdp_cmd("Page.printToPDF", 
                                 {'printBackground': True,
                                  'displayHeaderFooter': True,
                                  'paperHeight': paper_height,
                                  'paperWidth': paper_width,
                                  'headerTemplate':'<span style="font-size:12px"><span class=date></span><span class=title></span></span>',
                                  'footerHtml': 'Url',
                                  'footerLeft': 'Left',
                                  'footerFontSize': 14,
                                  })
    with open(path + file_name, "wb") as f:
        f.write(base64.b64decode(pdf['data']))
    driver.quit()

def screenshot_to_single_page_pdf(html, path, file_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
    driver.implicitly_wait(3)
    file_path = 'file://' + path + html
    driver.get(file_path)
    sleep(1)
    scroll_width = driver.execute_script('return document.body.scrollWidth') #parentNode
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 1400);")
    sleep(3)
        
    paper_height = int(scroll_height * 0.0104166667)+3.5 + 2*1*0.393701
    paper_width = scroll_width * 0.0104166667 + 2*1*0.393701
    driver.set_window_size(scroll_width, scroll_height)
    pdf_data = driver.get_screenshot_as_base64()
    pdf = driver.execute_cdp_cmd("Page.printToPDF", 
                                 {'printBackground': True,
                                  'displayHeaderFooter': True,
                                  'paperHeight': paper_height,
                                  'paperWidth': paper_width
                                  })
    with open(path + file_name, "wb") as f:
        # f.write(base64.b64decode(pdf_data))
        f.write(base64.b64decode(pdf['data']))
    driver.quit()
    
def web_to_pdf_2(url, file_name):
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToPdfClient('alex_xx', '138f6a26fd891565108c78cbf28f467d')
        
        # page setting
        client.setPageHeight("-1")
        client.setHeaderHeight('15mm')
        client.setFooterHeight('10mm')
        # client.setHeaderHtml('<a class=\'pdfcrowd-source-url\' data-pdfcrowd-placement=\'href-and-content\'></a>')
        client.setFooterHtml('<a class=\'pdfcrowd-source-url\' data-pdfcrowd-placement=\'href-and-content\'></a>')
        # client.setFooterHtml('<center><span class=\'pdfcrowd-page-number\'></span></center>')
        # client.setMarginTop('0')
        # client.setMarginBottom('0')
        
        # run the conversion and write the result to a file
        client.convertUrlToFile(url, file_name)
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
        # rethrow or handle the exception
        raise

def html_to_pdf_2(html, file_name):
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToPdfClient('alex_xx', '138f6a26fd891565108c78cbf28f467d')

        # page setting
        client.setPageHeight("-1")
        client.setHeaderHeight('15mm')
        client.setFooterHeight('10mm')
        # client.setHeaderHtml('<a class=\'pdfcrowd-source-url\' data-pdfcrowd-placement=\'href-and-content\'></a>')
        client.setFooterHtml('<a class=\'pdfcrowd-source-url\' data-pdfcrowd-placement=\'href-and-content\'></a>')
        # client.setFooterHtml('<center><span class=\'pdfcrowd-page-number\'></span></center>')
        # client.setMarginTop('0')
        # client.setMarginBottom('0')
        
        # run the conversion and write the result to a file
        client.convertFileToFile(url, file_name)
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
        # rethrow or handle the exception
        raise


if __name__ == '__main__':
    
    review_path = "E://DEI//01_coding_test_dir//realreason.ca//" 
    url = 'https://realreason.ca/kory/'
    url2 = 'https://www.ola.org/en/members'
    path = review_path + 'html//'
    path2 = 'E:\\DEI\\01_coding_test_dir\\realreason.ca\\html\\'
    url_lst = [url,url2]
    
    for item in url_lst[1:]:
        file_name = path + urlparse(item).netloc + '.pdf'
        web_to_pdf(item, file_name)
        
    htmls =  os.listdir(path)
    for file in htmls:
        if file.endswith('.html'):
            html_path = path2 + file
            file_name = re.sub(' ', '_', file.rstrip('html')) + 'pdf'
            html_to_pdf([html_path], file_name)


    # start = time.time()
    # file_name = "test_tutorial"
    # urls = get_url_list()

    # for index, url in enumerate(urls):
    #   parse_url_to_html(url, str(index) + ".html")
    # htmls =[]
    # pdfs =[]
    # for i in range(0,124):
    #     htmls.append(str(i)+'.html')
    #     pdfs.append(file_name+str(i)+'.pdf')

    #     save_pdf(str(i)+'.html', file_name+str(i)+'.pdf')

    #     print('finish convert '+str(i)+' htmls')

    # merger = PdfFileMerger()
    # for pdf in pdfs:
    #    merger.append(open(pdf,'rb'))
    #    print('Merge '+str(i)+' pdfs'+pdf)

    # output = open("test_all.pdf", "wb")
    # merger.write(output)

    # print("output pdf done")

    # for html in htmls:
    #     os.remove(html)
    #     print("delete temp html files"+html)

    # for pdf in pdfs:
    #     os.remove(pdf)
    #     print("delete temp pdf files"+pdf)

    # total_time = time.time() - start
    # print(u"Total time：%f s" % total_time)
