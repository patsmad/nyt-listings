from src.util.util_io import data_path
from src.util.request import soupifyURL
from src.util.image import getImage, resizeImage, writeImage
from src.db.db import DB
import glob
import re


class PosterFetcher:
    def __init__(self, db: DB):
        self.db = db

    def saved_keys(self):
        return [re.findall('.*\\\(.*).jpg', file)[0] for file in glob.glob(f'{data_path}/data/posters/*')]

    def all_keys(self):
        return [re.findall('https://www.imdb.com/title/(.*)/', link)[0] for link in self.db.fetch_distinct_links()]

    def get_poster_link(self, key):
        soup = soupifyURL(f'https://www.imdb.com/title/{key}/')
        poster = [link for link in soup.find_all('a', href=True)
                  if '/mediaviewer/rm' in link['href'] and 'ref_=tt_ov_i' in link['href']]
        if len(poster) > 0:
            return 'https://www.imdb.com{}'.format(poster[0]['href'].split('?')[0])

    def get_poster_src(self, poster_url):
        soup = soupifyURL(poster_url)
        for img in soup.find_all('img'):
            if 'media-amazon' in img['src']:
                if img.has_attr('data-image-id') and 'curr' in img['data-image-id']:
                    return img['src']

    def get_poster(self, key):
        maybe_poster_url = self.get_poster_link(key)
        if maybe_poster_url is not None:
            maybe_poster_src = self.get_poster_src(maybe_poster_url)
            if maybe_poster_src is not None:
                print(key, maybe_poster_url)
                poster_image_prior = getImage(maybe_poster_src)
                poster_image = resizeImage(poster_image_prior, (210, 140))
                writeImage(poster_image, f'{data_path}/data/posters/{key}.jpg')
            else:
                print(f'No poster src for {key}')
        else:
            print(f'No poster for {key}')

    def fill_missing_posters(self):
        remaining_keys = list(set(self.all_keys()) - set(self.saved_keys()))
        print(len(remaining_keys))
        for key in remaining_keys:
            self.get_poster(key)
