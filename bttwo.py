#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pymongo import MongoClient
from Download import download
from termcolor import colored
import os
import datetime
import requests


class bttwo():

    def __init__(self):
        client = MongoClient()
        db = client['bttwo']
        self.bttwo_bt = db['bt']
        self.title = ''
        self.name = ''
        self.content = ''  # binary data
        
    def all_url(self, url):
        start_html = download.get(url)
        start_html.encoding='utf-8'
        max_page_url = BeautifulSoup(start_html.text, 'lxml').find(
            'a', class_='extend')['href']
        max_page_num = max_page_url[-2:]
        href = max_page_url[:-2]  # 'http://www.bttwo.com/new-movie/page/'

        for page_num in range(1, int(max_page_num) + 1):
            page_url = href + str(page_num)
            page_html = download.get(page_url)
            page_html.encoding='utf-8'
            all_movie_a = BeautifulSoup(page_html.text, 'lxml').find(
                'div', class_='bt_img').find('ul').find_all('a')
            s = set()
            for movie_a in all_movie_a:
                movie_url_2 = movie_a['href']
                s.add(movie_url_2)  # remove duplicates
            for movie_url in s:
                try:
                    movie_html = download.get(movie_url)
                    movie_html.encoding='utf-8'
                    download_field = BeautifulSoup(movie_html.text, 'lxml').find(
                        'div', class_='ypbt_down_list')
                    title = download_field.find('a')['title']
                    self.title = title
                    all_bt_a = download_field.find_all('a')
                except Exception as e:
                    print(e)
                    print("Error: couldn't get", movie_url)
                    continue
                title = title.replace(':', '：') #compatible windows
                title = title.replace('?','？')
                path = '/users/apple/Desktop/bttwo/crawler'
                self.chdir(path,title)
                for bt_a in all_bt_a:
                    try:
                        dataid = bt_a['dataid']
                        ver = bt_a['ver']
                    except Exception as e:
                        print(e)
                        print("Couldn't get torrent file in ",movie_url)
                        continue
                    name = bt_a.get_text().strip().split('/')[1]
                    self.name = name
                    if self.bttwo_bt.find_one({'name':name}):
                        print('%s has been download!' % name)
                        continue
                    bigsezi = bt_a.find('sapn', class_='bigsezi').get_text()
                    size1 = bigsezi[:1]
                    size2 = bigsezi[2:4]
                    try:
                        self.save(name, dataid, size1, size2, ver)
                    except Exception as e:
                        print(e)
                        print("Error: couldn't save", name)
                        continue

    def chdir(self, path, title):
        isExists = os.path.exists(os.path.join(path, title))
        if not isExists:
            os.mkdir(os.path.join(path, title))
            print('Have created folder', title)
            os.chdir(os.path.join(path, title))
        else:
            os.chdir(os.path.join(path, title))

    def save(self, name, dataid, size1, size2, ver):
        print('Starting to save', name)
        # bt_url = 'http://www.bttwo.com/download/'+dataid+'/?version='+size1+'-'+size2+'gb'
        data = {
            'action': 'downloads_link',
            'doid': dataid,
            'ver': ver
        }
        post = requests.post(
            'http://www.bttwo.com/wp-admin/admin-ajax.php', data=data)
        bt_url = post.text
        bt = download.get(bt_url)
        self.content = bt.content
        with open(name, 'wb+') as f:
            f.write(bt.content)
        post = {
            'title': self.title,
            'name': self.name,
            'content': self.content,
            'date': datetime.datetime.now()
        }
        self.bttwo_bt.insert_one(post)
        print('Database has been updated')


Bttwo = bttwo()
Bttwo.all_url('http://www.bttwo.com/new-movie')
