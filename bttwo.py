from bs4 import BeautifulSoup
import os
# from pymongo import MongoClient
import datetime
import requests
from Download import download


class bttwo():

    def all_url(self, url):
        start_html = download.get(url)
        max_page_url = BeautifulSoup(start_html.text, 'lxml').find(
            'a', class_='extend')['href']
        max_page_num = max_page_url[-2:]
        href = max_page_url[:-2]  # 'http://www.bttwo.com/new-movie/page/'

        for page_num in range(1, int(max_page_num) + 1):
            page_url = href + str(page_num)
            page_html = download.get(page_url)
            all_movie_a = BeautifulSoup(page_html.text, 'lxml').find(
                'div', class_='bt_img').find('ul').find_all('a')
            s = set()
            for movie_a in all_movie_a:
                movie_url_2 = movie_a['href']
                s.add(movie_url_2)  # 去重
            for movie_url in s:
                try:
                    movie_html = download.get(movie_url)
                    download_field = BeautifulSoup(movie_html.text, 'lxml').find(
                        'div', class_='ypbt_down_list')
                    title = download_field.find('a')['title']
                    all_bt_a = download_field.find_all('a')
                except Exception as e:
                    print(e)
                    print(u'获取', movie_url, u'出错,已跳过')
                    continue
                title = title.replace(':', '：')
                title = title.replace('?','？')
                print(u'开始保存', title)
                path = 'C:\\Users\\60114\\Desktop\\bttwo'
                # os.mkdir(os.path.join(path,title))
                if not self.mkdir(path, title):
                    print(u'已经跳过', title)
                    continue
                # os.chdir(os.path.join(path,title))
                for bt_a in all_bt_a:
                    try:
                        dataid = bt_a['dataid']
                        ver = bt_a['ver']
                    except Exception as e:
                        print(e)
                        print(u'在', movie_url, u'下载bt时出现错误，已跳过')
                        continue
                    name = bt_a.get_text().strip().split('/')[1]
                    bigsezi = bt_a.find('sapn', class_='bigsezi').get_text()
                    size1 = bigsezi[:1]
                    size2 = bigsezi[2:4]
                    try:
                        self.save(name, dataid, size1, size2, ver)
                    except Exception as e:
                        print(e)
                        print(u'保存', name, u'出错,已跳过')
                        continue

    def mkdir(self, path, title):
        isExists = os.path.exists(os.path.join(path, title))
        if not isExists:
            os.mkdir(os.path.join(path, title))
            os.chdir(os.path.join(path, title))
            return True
        else:
            return False

    def save(self, name, dataid, size1, size2, ver):
        print(u'开始保存', name)
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
        with open(name, 'ab') as f:
            f.write(bt.content)


Bttwo = bttwo()
Bttwo.all_url('http://www.bttwo.com/new-movie')
