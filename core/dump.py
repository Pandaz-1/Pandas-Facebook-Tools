'''
Name: Dump
Date: 13-07-2020
'''

from bs4 import BeautifulSoup
from requests import Session
import re

class Dump:

    def __init__(self, cookie):
        self.cookie = cookie
        self.req = Session()
        self.head = 'https://free.facebook.com'

        self.id = []

    def user(self, fros, loop=True):
        me = self.req.get(self.head+fros, cookies=self.cookie).text
        page = self.get_next_page(me, 'Teman')
        try:
            if loop:
                while True:
                    if 'Anda Tidak Dapat Menggunakan Fitur Ini Sekarang' in page:
                        break
                    else:
                        self.get_id(page)
                        me = page
                        page = self.get_next_page(me, 'Lihat Teman Lain')
                        print(f'\r    -> {str(len(self.id))} ID Telah Dikumpulkan', end='', flush=True)
            else:
                self.get_id(page)
        except:
            pass
        return self.id

    def get_next_page(self, target, string):
        parse = BeautifulSoup(target, 'html.parser')
        a = parse.find_all('a', string=string)
        for x in a:
            if '/friends?' in str(x) or '/profile.php' in str(x):
                page = self.req.get(self.head+x['href'], cookies=self.cookie).text
                return page

    def get_id(self, page):
        a = re.findall(r'middle\"\>\<a\ class\=\"(.*?)\"\ href\=\"(.*?)\"\>', page)
        for x in a:
            if 'friends/hovercard/mbasic/' in x[1]:
                pass
            elif 'profile.php' in x[1]:
                try:
                    email = re.search(r'id\=(.*?)\&', x[1]).group(1)
                    self.id.append(email)
                except:
                    pass
            else:
                try:
                    email = re.search(r'\/(.*?)\?', x[1]).group(1)
                    self.id.append(email)
                except:
                    pass
