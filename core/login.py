'''
Name: Parser Cookie
Date: 13-07-2020
'''

from requests import Session
from headerz import headerz
import re

def parserData(data):
    head = headerz().parser(data)
    kuki = headerz().cookie_builder(head['cookie'])
    cookie = {'cookies':kuki}

    me = Session().get('https://free.facebook.com/me', cookies=cookie)
    if 'Buat Akun Baru' in me.text:
        return 'IC'
    elif 'Harap Konfirmasikan Identitas Anda' in me.text:
        return 'CP'
    else:
        username = re.search(r'\<title\>(.*?)\<\/title\>', me.text).group(1)
        return [cookie, username]
