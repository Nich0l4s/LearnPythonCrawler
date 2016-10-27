# _*_coding: utf-8 _*_
import requests
from bs4 import BeautifulSoup

import codecs
import csv

__author__ = 'Nicholas'

def getHTML(url):
    r = requests.get(url)
    return r.content

def parseHTML(html):
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.body
    company_middle = body.find('div', attrs={'class': 'middle'})
    company_list_ct = company_middle.find('div', attrs={'class': 'list-ct'})
    company_list = []
    for ul in company_list_ct.find_all('ul', attrs={'class': 'company-list'}):
        for li in ul.find_all('li'):
            company_url = li.a['href']
            company_info = li.a.get_text()
            company_list.append([company_info, company_url])
    return company_list
def writeCSV(file_name, data_list):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for data in data_list:
            writer.writerow(data)
if __name__ == '__main__':
    URL = 'http://www.cninfo.com.cn/cninfo-new/information/companylist'
    html = getHTML(URL)
    data_list = parseHTML(html)
    print(data_list)
    writeCSV('test.csv', data_list)




# soup = BeautifulSoup(html,'html.parser')
# div_people_list = soup.find('div', attrs={'class': 'people_list'})
#
# a_s = div_people_list.find_all('a', attrs={'target':'_blank'})
# for a in a_s:
#     url = a['href']
#     name = a.get_text()
#     print(name,url)