'''
Name: Modul Pesan
Date: 14-07-2020
'''
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs
from requests import Session
import re

class Pesan:

    def __init__(self, cookie):
        self.cookie = cookie
        self.req = Session()
        self.head = 'https://free.facebook.com'

    # Spam Chat
    def spam(self, id, pesan, count):
        terkirim = 0
        page = self.req.get(self.head+'/messages/read/?tid='+id, cookies=self.cookie)
        for x in range(int(count)):
            data = {
                'body':pesan,
                'send':'Kirim'
                }
            tag_input = bs(page.text, 'html.parser').find_all('input', {'type':'hidden'})
            for y in tag_input:
                try:
                    data[y['name']] = y['value']
                except KeyError:
                    data[y['name']] = ''
            action = re.search(r'\<form\ method\=\"post\"\ action\=\"(.*?)\"\ class\=\"(.*?)\"\ id\=\"composer_form\"\>', page.text).group(1)
            self.req.post(self.head+action, cookies=self.cookie, data=data)
            terkirim += 1
            print(f'\r    -> {str(terkirim)} Pesan Terkirim', end='', flush=True)
        print('\n    -> Selesai')

    # Penghapus Log Pesan
    def hapus_log_pesan(self):
        count = 0
        while True:
            page_pesan = self.req.get(self.head+'/messages/', cookies=self.cookie)
            link_pesan = re.findall(r'href\="\/messages\/read\/\?(.*?)"\>', page_pesan.text)
            if len(link_pesan) != 0:
                with ThreadPoolExecutor(max_workers=10) as th:
                    for x in link_pesan:
                        th.submit(self.hapus, (self.head+'/messages/read/?'+link_pesan[0].replace(';', '&')))
                        count += 1
                        print(f'\r    -> {str(count)} Pesan Terhapus', end='', flush=True)
            else:
                print('\n    -! Pesan Tidak Didapatkan')
                break

    def hapus(self, url):
        data = {'delete':'Hapus'}
        page = self.req.get(url, cookies=self.cookie)

        page_hapus = bs(page.text, 'html.parser').find_all('input', {'type':'hidden'})
        for x in page_hapus:
            try:
                data[x['name']] = x['value']
            except KeyError:
                data[x['name']] = ''
        action = re.search(r'action\=\"\/messages\/action\_redirect\?(.*?)\"', page.text).group(1).replace(';', '&')

        page_konformasi = self.req.post(self.head+'/messages/action_redirect?'+action ,cookies=self.cookie, data=data)
        link_konfirmasi = bs(page_konformasi.text, 'html.parser').find('a', string='Hapus')['href']

        # Konformasi penghapusan
        self.req.get(self.head+link_konfirmasi, cookies=self.cookie)
