import requests
from bs4 import BeautifulSoup as bs
import re
import requests
from os import mkdir
from tqdm import tqdm
from random import choice

class WikiArtHandler:
    def __init__(self):
        f = open('artinfo.json', 'r')
        self.allinf = json.loads(f.read())
    
    def get_genres(self):
        for i in self.allinf[2]:
            print(i)

    def get_artists(self):
        for i in self.allinf[0]:
            print(i)

    def get_artists_per_genre(self, genre):
        for i in self.allinf[4].keys():
            if i == genre:
                for j in self.allinf[4][i]:
                    print(j)

    def get_pic(self, artist, name):
        name = name.replace(" ", "-")
        name = name.replace("(", "")
        name = name.replace(")", "")
        name = name.replace(",", "")
        name = name.replace(".", "")
        name = name.replace("!", "")
        name = name.replace("?", "")
        artist = artist.replace(" ", "-")
        ap = 'https://uploads1.wikiart.org/images/{}/{}.jpg!Large.jpg'.format(artist.lower(), name.lower())
        return ap

    def get_works(self, artist):
        for i in range(len(self.allinf[0])):
            if self.allinf[0][i] == artist:
                ans = []
                ap = self.allinf[1][i] + "/all-works/text-list"
                print(self.allinf[0][i], " ", self.allinf[1][i])
                image_resolution = ['!PinterestSmall.jpg', '!PinterestLarge.jpg', '!Portrait.jpg', '!Blog.jpg', '!Large.jpg', ''][4]
                all_pics = bs(requests.get(ap).text, "html.parser")
                for i, link in enumerate(tqdm(list(filter(lambda x: (len(x.attrs) == 1) and ('href' in x.attrs), all_pics.findAll('a')))[:200])):
                    img_link = bs(requests.get('https://www.wikiart.org{}'.format(link.attrs['href'])).text, "html.parser").findAll('img', {'itemprop': 'image'})[0].attrs['src'].split('!')[0] + image_resolution
                    ans.append(requests.get(img_link).content)
                    return choice(ans)
