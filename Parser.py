import requests
from bs4 import BeautifulSoup as bs
import re
import requests
from os import mkdir
from tqdm import tqdm

class WikiArtHandler:
    def __init__(self):
        page = requests.get('https://www.wikiart.org/ru/artists-by-genre')
        soup = bs(page.text, 'html.parser')
        self.genre_name_list = soup.find_all(class_ = "dictionaries-list")[2]
        self.genre_name_list = self.genre_name_list.find_all("a")
        self.genre_painter = {}
        self.names_ans = []
        for i in self.genre_name_list:
            self.genre_painter[i.text.split(" ")[0]] = []
            ap = i.get("href")
            ap = "https://www.wikiart.org" + ap + "/text-list"
            print(ap)
            page_genre = requests.get(ap)
            soup_genre = bs(page_genre.text, 'html.parser')
            names = soup_genre.find_all(class_= "masonry-text-view masonry-text-view-all")[0]
            names = names.find_all("a")
            for j in names:
                self.names_ans.append(j)
                self.genre_painter[i.text.split(" ")[0]].append(j.text)
        self.names_ans = list(set(self.names_ans))
    
    def get_genres(self):
        for i in self.genre_name_list:
            print(i.text)

    def get_artists(self):
        for i in self.names_ans:
            print(i.text)

        def get_artists_per_genre(self, genre):
            for i in self.genre_painter.keys():
                if i == genre:
                    for j in self.genre_painter[i]:
                        print(j)

    def get_works(self, artist):
        for i in self.names_ans:
            if i.text == artist:
                ans_link = []
                ap = i.get("href")
                ap = "https://www.wikiart.org" + ap + "/all-works/text-list"
                    # !!! ARGUMENTS !!!
                    image_resolution = ['!PinterestSmall.jpg', '!PinterestLarge.jpg', '!Portrait.jpg', '!Blog.jpg', '!Large.jpg', ''][4]  # В последних скобочках ставить число от 0 до 5. Чем больше число, тем больше разрешение
                    folder = artist  # Имя папки, куда будут сохранены изображения
                    # !!! ARGUMENTS !!!
                    
                    all_pics = bs(requests.get(ap).text, "html.parser")
                    try:
                        mkdir(folder)
                    except FileExistsError:
                        pass
            
                for i, link in enumerate(tqdm(list(filter(lambda x: (len(x.attrs) == 1) and ('href' in x.attrs), all_pics.findAll('a')))[:200])):
                    img_link = bs(requests.get('https://www.wikiart.org{}'.format(link.attrs['href'])).text, "html.parser").findAll('img', {'itemprop': 'image'})[0].attrs['src'].split('!')[0] + image_resolution
                    with open('{}/{}.jpg'.format(folder, i + 1), 'wb') as f:
                        f.write(requests.get(img_link).content)
