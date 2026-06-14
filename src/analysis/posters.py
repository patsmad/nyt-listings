from src.util.util_io import data_path
from src.util.image import getImage, resizeImage, writeImage
from src.db.db import DB
from src.util.tmdb_api import TMDBAPI
import glob
import re


class PosterFetcher:
    def __init__(self, db: DB, tmdb_api: TMDBAPI):
        self.db = db
        self.tmdb_api = tmdb_api

    def saved_keys(self):
        return [re.findall(r'.*\\(.*).jpg', file)[0] for file in glob.glob(f'{data_path}/data/posters/*')]

    def all_keys(self):
        print([link for link in self.db.fetch_distinct_links() if len(re.findall('https://www.imdb.com/title/(.*)/', link)) == 0])
        return [re.findall('https://www.imdb.com/title/(.*)/', link)[0] for link in self.db.fetch_distinct_links()]

    def get_poster_link(self, key):
        maybe_tmdb = self.tmdb_api.findIMDBResult(key)
        if len(maybe_tmdb) > 0:
            maybe_slug = maybe_tmdb[0]['poster_path']
            if maybe_slug is not None:
                return 'https://image.tmdb.org/t/p/w1280{}'.format(maybe_slug)

    def get_poster(self, key):
        maybe_poster_url = self.get_poster_link(key)
        if maybe_poster_url is not None:
            print(key, maybe_poster_url)
            poster_image_prior = getImage(maybe_poster_url)
            poster_image = resizeImage(poster_image_prior, (210, 140))
            writeImage(poster_image, f'{data_path}/data/posters/{key}.jpg')
        else:
            print(f'No poster for {key}')

    def fill_missing_posters(self):
        remaining_keys = list(set(self.all_keys()) - set(self.saved_keys()))
        print(len(remaining_keys))
        for key in remaining_keys:
            self.get_poster(key)
