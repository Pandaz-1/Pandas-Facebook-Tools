'''
Name: Pertemanan
Date: 13-07-2020
'''

from concurrent.futures import ThreadPoolExecutor as thread
from bs4 import BeautifulSoup as bs
from . import dump
import requests as req
import re

class Pertemanan:

    def __init__(self, cookie):
        self.cookie = cookie
        self.head = 'https://free.facebook.com'

    # Unfriend
    def unfriend(self):
        count = 0
        while True:
            konfir = []
            id = dump.Dump(self.cookie).user('/me', loop=False)
            if len(id) != 0:
                for x in id:
                    lainnya = self.getLink(self.head+'/'+x, 'Lainnya')
                    batalkan = self.getLink(self.head+lainnya[0], 'Batalkan pertemanan')
                    konfir.append(batalkan[0])
                with thread(max_workers=10) as th:
                    for s in konfir:
                        th.submit(self.konfirmasi_penghapusan, (self.head+s))
                        count += 1
                        print(f'\r    -> {str(count)} Teman Telah Dihapus', end='', flush=True)
            else:
                print()
                print('\n    -! Teman Tidak Didapatkan')

    def konfirmasi_penghapusan(self, url):
        data = {'confirm':'Konfirmasi'}
        page = req.get(url, cookies=self.cookie)
        parse = bs(page.text, 'html.parser')
        input_type_hidden = parse.find_all('input', {'type':'hidden'})

        for i in input_type_hidden:
            try:
                data[i['name']] = i['value']
            except KeyError:
                data[i['name']] = ''
        action = parse.find('form', {'method':'post'})['action']
        req.post(self.head+action, cookies=self.cookie, data=data)

    # Konfirmasi Permintaan Pertemanan
    def konfirmasi_permintaan_pertemanan(self):
        count = 0
        while True:
            link = self.getLink('https://free.facebook.com/friends/center/requests', 'Konfirmasi')
            if len(link) != 0:
                with thread(max_workers=3) as thr:
                    for x in link:
                        thr.submit(self.start, (x))
                        count += 1
                        print(f'\r    -> {str(count)} Terkonfirmasi', end='', flush=True)
            else:
                print('    -! Permintaan Tidak Didapatkan')
                break

    # Hapus Permintaan Pertemanan
    def hapus_permintaan_pertemanan(self):
        count = 0
        while True:
            link = self.getLink('https://free.facebook.com/friends/center/requests', 'Hapus Permintaan')
            if len(link) != 0:
                with thread(max_workers=3) as thr:
                    for x in link:
                        thr.submit(self.start, (x))
                        count += 1
                        print(f'\r    -> {str(count)} Terhapus', end='', flush=True)
            else:
                print('    -! Permintaan Tidak Didapatkan')
                break

    def start(self, action):
        req.get(self.head+action, cookies=self.cookie)

    def getLink(self, url, string):
        action = []
        page = req.get(url, cookies=self.cookie)
        parse = bs(page.text, 'html.parser')

        link = parse.find_all('a', string=string)

        for x in link:
            href = re.search(r'href\=\"(.*?)\"', str(x)).group(1).replace(';', '&')
            action.append(href)

        return action


