import random
from collections import defaultdict
import json
import operator
from parser import WikiArtHandler

class RecommenderData(object):
    def __init__(self):
        self.liked_drawings = -1
        self.wikiart_handler = WikiArtHandler()
        self.clusters = json.loads(open('data.json').read())

    def get_next(self):
        if self.liked_drawings == 1:
            return random.randint(0, 3250)
        cluster = self.clusters[self.liked_drawings]
        indices = [i for i, x in enumerate(self.clusters) if x == cluster]
        return random.choice(indices)
    def add_artist(self, artist):
        self.artist.append(artist)

    def update(self, picture):
        self.liked_drawings = picture