import random
from collections import defaultdict
import operator
from parser import WikiArtHandler

class RecommenderData(object):
    def __init__(self, user_id, artist):
        self.user_id = user_id
        self.liked_drawings = []

        self.artist = artist
        self.wikiart_handler = WikiArtHandler()

    def get_next(self):
        artist = self.artist[min(random.randint(0, len(self.artist)), len(self.artist) - 1)]
        return self.wikiart_handler.get_works(artist)

    def add_artist(self, artist):
        self.artist.append(artist)

    def update(self, picture):
        self.liked_drawings.append(picture)