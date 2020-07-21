'''
Name: Komentar
Date: 18-07-2020
'''

from bs4 import BeautifulSoup as bs
import requests as req
import re

class Komentar:

    def __init__(self, cookie):
        self.cookie = cookie
        self.head = 'https://free.facebook.com'

    def spam(self, url, komen, jumlah):
        url = url.replace('www.facebook.com', 'free.facebook.com')
        for x in range(jumlah):
            page = req.get(url, cookies=self.cookie)
            data = self.getInput(page.text)
            data['comment_text'] = komen
            data['submit'] = 'Komentari'

            action = re.search(r'\<form\ method\=\"post\"\ action\=\"\/a\/comment\.php(.*?)\"\>', page.text).group(1).replace(';', '&')
            # Mengirim komentar
            req.post(self.head+'/a/comment.php'+action, cookies=self.cookie, data=data)
            print(f'\r    -> {str(x+1)} Komentar Terkirim', end='', flush=True)

    def getInput(self, page):
        data = {}
        pars = bs(page, 'html.parser')
        inp = pars.find_all('input', {'type':'hidden'})
        for x in inp:
            try:
                data[x['name']] = x['value']
            except KeyError:
                data[x['name']] = ''
        return data
