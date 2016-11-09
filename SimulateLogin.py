#!/usr/bin/env python
# encoding=utf-8
# 中文验证码：
# _xsrf:6b9aa7f57129e5fb728be16b3f02ebf8
# password:
# captcha:{"img_size":[200,44],"input_points":[[16.5,23.6094],[162.5,16.60938]]}
# captcha_type:cn
# remember_me:true
# email:
import time
import requests
import os
import getpass
from bs4 import BeautifulSoup


LOGIN_URL = 'http://www.zhihu.com/#signin'
LOGIN_SUBMIT_URL = 'https://www.zhihu.com/login/email'
CAPTCHA_PATH = 'https://www.zhihu.com/captcha.gif?r={time}&type=login'
CAPTCHA_PATH = 'E:\\项目\\模拟登陆\\'


def kill_captcha(data, path=CAPTCHA_PATH, name='capcha.gif'):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + name, 'wb') as f:
        f.write(data)
    print(data)
    return input('验证码：')


def login(email, password, captcha):

    session = requests.session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                                    '(KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    _xsrf = BeautifulSoup(session.get(LOGIN_URL).content, 'html.parser').find('input', attrs={'name': '_xsrf'})['value']
    pic_capcha = session.get(CAPTCHA_PATH.format(time=int(time.time() * 1000))).content
    form = {
        '_xsrf': _xsrf,
        'password': password,
        'captcha': captcha(pic_capcha),
        'remember_me': 'true',
        'email': email
    }
    print(form)
    resp = session.post(LOGIN_SUBMIT_URL, form).content
    print('resp:')
    print(resp)
    assert b'\\u767b\\u5f55\\u6210\\u529f' in resp
    return session

if __name__ == '__main__':
    email = input('Email:')
    password = getpass.getpass()
    my_session = login(email, password, kill_captcha)
    print(BeautifulSoup(my_session.get('https://www.zhihu.com').content, 'html.parser')
          .find('span', class_='name').getText())
