'''
Name: Pandas
Date: 13-07-2020

Silahkan lihat codingannya,silahkan kalian lihat asalkan jangan di recode:)
'''

class Pandas:

    def __init__(self):
        os.system('clear')
        self.banner()
        try:
            files = open('cookie.log', 'r').read()
            data = parserData(files)
            if data == 'IC':
                print('    -! Invalid Cookie')
                os.system('rm cookie.log');exit()
            elif data == 'CP':
                print('    -! Akun Checkpoint')
                os.system('rm cookie.log');exit()
            else:
                pass
        except FileNotFoundError:
            print('    -! Simpan cookie di file dengan nama: cookie.log')
            exit()

        self.head = 'https://free.facebook.com'
        self.data = data

    def banner(self):
        print('''
    █▀█ ▄▀█ █▄ █ █▀▄ ▄▀█ █▀
    █▀▀ █▀█ █ ▀█ █▄▀ █▀█ ▄█ 
    -----------------------
        Facebook Tools
''')

    def menu(self):
        os.system('clear')
        self.banner()
        print('    User: '+self.data[1]+'\n')
        print('    1. Pertemanan')
        print('    2. Pesan')
        print('    3. Komentar')
        print('    4. Lainnya')
        print('    5. Info')
        print('    0. Keluar')
        pil = input('    \n    -> ')
        if pil == '1':
            self.menu_pertemanan()
        elif pil == '2':
            self.menu_pesan()
        elif pil == '3':
            self.menu_komentar()
        elif pil == '4':
            self.menu_lainnya()
        elif pil == '5':
            self.info()
        elif pil == '0':
            print('\n    -* Terima Kasih Telah Menggunkan Tools Ini:)')

    def info(self):
        os.system('clear')
        self.banner()
        print('''
    -* Author: Pandas ID
    -* Fanspage: Pandas ID
    -* Blog: https://pandasid.blogspot.com
    -* WhatsApp: 082250223147

    -* Versi: 1.0
                ''')
        input('    -* Kembali')
        self.menu()
    def menu_pertemanan(self):
        os.system('clear')
        self.banner()
        print('    1. Konfirmasi Permintaan Pertemanan')
        print('    2. Hapus Permintaan Pertemanan')
        print('    3. Hapus Teman')
        print('    0. Kembali')
        pil = input('\n    -> ')
        if pil == '1':
            Pertemanan(self.data[0]).konfirmasi_permintaan_pertemanan()
        elif pil == '2':
            Pertemanan(self.data[0]).hapus_permintaan_pertemanan()
        elif pil == '3':
            Pertemanan(self.data[0]).unfriend()
        elif pil == '0':
            self.menu()
        else:
            self.menu_pertemanan()

    def menu_pesan(self):
        os.system('clear')
        self.banner()
        print('    1. Hapus Log Pesan')
        print('    2. Spam Pesan')
        print('    0. Kembali')
        pil = input('    -> ')
        if pil == '1':
            Pesan(self.data[0]).hapus_log_pesan()
        elif pil == '2':
            print()
            id = input('    -> ID Target: ')
            pesan = input('    -> Pesan: ')
            jumlah = input('    -> Jumlah: ')
            Pesan(self.data[0]).spam(id, pesan, jumlah)
        elif pil == '0':
            self.menu()
        else:
            self.menu_pesan()

    def menu_komentar(self):
        os.system('clear')
        self.banner()
        print('    1. Spam Komentar')
        print('    0. Kembali')
        pil = input('\n    ->')
        if pil == '1':
            print()
            try:
                url = input('    -> Url Postingan: ')
                komen = input('    -> Komentar: ')
                jumlah = int(input('    -> Jumlah: '))
                Komentar(self.data[0]).spam(url, komen, jumlah)
            except ValueError:
                exit('    -! Masukan Angka')
        elif pil == '0':
            self.menu()
        else:
            self.menu_komentar()

    def menu_lainnya(self):
        os.system('clear')
        self.banner()
        print('    1. Dump ID')
        print('    0. Kembali')
        pil = input('\n    -> ')
        if pil == '1':
            print()
            print('    1. Dump ID Dari Teman')
            print('    2. Dump ID Teman Dari Teman')
            pil = input('\n    -> ')
            if pil == '1':
                results_id = Dump(self.data[0]).user('/me')
                print()
                print('\n    -> Simpan ID')
                nama_file = input('    -> Nama File: ')
                self.simpanID(results_id, nama_file)
            elif pil == '2':
                print()
                id = input('    -> ID: ')
                profil = requests.get(self.head+'/'+id, cookies=self.data[0]).text
                username = re.search(r'\<title\>(.*?)\<\/title\>', profil).group(1)
                if username == 'Halaman Tidak Ditemukan':
                    exit('    -! Teman Tidak Ditemukan')
                else:
                    print('    -> Meng-dump ID dari: '+username)
                    results_id = Dump(self.data[0]).user('/'+id)
                    print()
                    print('\n    -> Simpan ID')
                    nama_file = input('    -> Nama File: ')
                    self.simpanID(results_id, nama_file)

        elif pil == '0':
            self.menu()
        else:
            self.menu_lainnya()

    def simpanID(self, list_id, nama_file):
        try:
            files = open('data/id/'+nama_file, 'w')
            for x in list_id:
                files.write(x+'\n')
            print('    -> File Tersimpan Di: data/id/'+nama_file)
        except FileNotFoundError:
            os.system('mkdir data')
            os.system('mkdir data/id')
            self.simpanID(list_id, nama_file)

if __name__ == '__main__':
    import requests
    import os, re
    from core.pertemanan import Pertemanan
    from core.login import parserData
    from core.dump import Dump
    from core.pesan import Pesan
    from core.komentar import Komentar
    try:
        Pandas().menu()
    except requests.ConnectionError:
        print('    -! Koneksi Error')
        exit()
    except IOError:
        print('    -! Keluar')
    except KeyboardInterrupt:
        print('    -! Keluar')

