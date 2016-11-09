#!/usr/bin/env python
# encoding=utf-8

import os
import requests
import json
import getpass
import SimulateLogin
from bs4 import BeautifulSoup

CAPTCHA_PATH = 'E:\\项目\\模拟登陆\\豆瓣\\验证码\\'
CAPTCHA_URL_URL = 'https://www.douban.com/j/misc/captcha'
DOUBAN_LOGIN_URL = 'https://www.douban.com/accounts/login'
DOUBAN_HOME = 'https://www.douban.com/'


def login(email, password, captcha):
    session = requests.session()
    # session.headers[]
    json_str = session.get(CAPTCHA_URL_URL).text
    json_obj = json.loads(json_str)
    captcha_url = 'https:' + json_obj['url']
    captcha_id = json_obj['token']
    name = captcha_id.replace(':', '_') + '.gif'

    if os.path.exists(CAPTCHA_PATH + name) and os.path.isfile(CAPTCHA_PATH + name):
        print('文件已存在')
        captcha_content = input('验证码：')
    else:
        captcha_content = captcha(session.get(captcha_url).content,
                                  path=CAPTCHA_PATH, name=name)
    form = {
        'source': 'index_nav',
        'form_email': email,
        'form_password': password,
        'captcha-solution': captcha_content,
        'captcha-id': captcha_id
    }
    resp = session.post(DOUBAN_LOGIN_URL, data=form)
    assert resp.url == 'https://www.douban.com/'
    assert b'\xe7\x9a\x84\xe5\xb8\x90\xe5\x8f\xb7' in resp.content
if __name__ == '__main__':
    email = input('Email:')
    password = getpass.getpass()
    login(email, password, SimulateLogin.kill_captcha)
