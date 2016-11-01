#!usr/bin/env python
# encoding=utf-8
import requests
import json
import csv
import os
from bs4 import BeautifulSoup


DOWNLOAD_URL = 'http://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'
INFO_URL = 'http://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'
LOGO_URL = 'http://www.lgstatic.com/thumbnail_120x120/'
LOGO_PATH = 'E:\项目\拉勾网爬虫\Logo\\'


def post_form(url, data=None):
    headers = {
        'Host': 'www.lagou.com',
        'Origin': 'http://www.lagou.com',
        'Referer': 'http://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36' +
                      '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    json_str = requests.post(url, headers=headers, data=data).text
    json_obj = json.loads(json_str)
    return json_obj


def get_total_page(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    total = int(soup.find('span', attrs={'class': 'span totalNum'}).get_text())
    return total


def main():
    total = get_total_page(DOWNLOAD_URL)
    if not os.path.exists(LOGO_PATH):
        os.mkdir(LOGO_PATH)
    with open('LaGouPython.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['职位', '薪水', '工作地点', '公司名称', '工作时间', '教育程度'])
        for index in range(1, total + 1):
            data = {
                'first': 'false',
                'pn': str(index),
                'kd': 'Python'
            }
            json_obj = post_form(INFO_URL, data=data)
            for info in json_obj['content']['positionResult']['result']:
                data = [info['positionName'], info['salary'], info['city'] +
                        ('' if info['businessZones'] is None else '·' + info['businessZones'][0]),
                        info['companyFullName'], info['workYear'], info['education']]
                writer.writerow(data)
                name = LOGO_PATH + info['companyLogo'].split('/')[-1]
                mark = name.find('?')
                if mark != -1:
                    name = name[:mark]
                if os.path.exists(name):
                    pass
                else:
                    logo = requests.get(LOGO_URL + info['companyLogo']).content
                    with open(name, 'wb') as lf:
                        lf.write(logo)


if __name__ == '__main__':
    main()
