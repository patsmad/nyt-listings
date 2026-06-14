from src.util.util_io import getFiles, readJSON, downloadFile, unzipGZFile, readTSV, mkdir, rmdir, data_path
from src.util.image import open_image, crop_image
from .db import DB
from src.api.api import API
from .model.box import InputBox
from .model.file import InputFile
from .model.item import InputItem
from .model.link import InputLink
from .model.link_info import InputLinkInfo
import re
import glob
import os
import datetime

class DBIO:
    def __init__(self, db: DB, api: API):
        self.db = db
        self.api = api

    def to_input_item(self, file_id: int, item: dict) -> InputItem:
        return InputItem(file_id=file_id, x=item['x'], y=item['y'])

    def to_input_box(self, item_id: int, box: dict) -> InputBox:
        return InputBox(item_id=item_id, left=box['left'], top=box['top'], width=box['width'], height=box['height'])

    def to_input_link(self, box_id: int, link: dict) -> InputLink:
        confirmed: bool = link['confirmed'] if link['confirmed'] is not None else False
        return InputLink(box_id=box_id, link=link['link'], confirmed=confirmed)

    def add_files(self) -> None:
        all_files = [file.name for file in self.db.fetch_all_files()]
        for file in getFiles('data/files/*'):
            file_name = os.path.basename(file)
            if file_name not in all_files:
                img = open_image(f'{data_path}/data/files/{file_name}')
                width, height = img.size
                date = re.findall('.*([0-9]{4}_[0-9]{2}_[0-9]{2}).*', file_name)[0]
                dt = datetime.datetime.strptime(date, '%Y_%m_%d')
                file_id: int = self.db.insert_file(
                    InputFile(**{'name': file_name, 'file_date': dt, 'width': width, 'height': height})
                )
                print(file_id)

    def update_imdb_data(self):
        mkdir('data/tmp')
        for fname in ['title.basics.tsv.gz', 'title.ratings.tsv.gz']:
            downloadFile(f'https://datasets.imdbws.com/{fname}', f'data/tmp/{fname}')
            unzipGZFile(f'data/tmp/{fname}')
        full_dict = {}
        for row in readTSV('data/tmp/title.basics.tsv'):
            link = f'https://www.imdb.com/title/{row["tconst"]}/'
            full_dict[link] = {
                'link': link,
                'title': row['primaryTitle'],
                'year': row['startYear'],
                'rating': 0.0,
                'votes': 0
            }
        for row in readTSV('data/tmp/title.ratings.tsv'):
            link = f'https://www.imdb.com/title/{row["tconst"]}/'
            if link in full_dict:
                full_dict[link]['rating'] = row['averageRating']
                full_dict[link]['votes'] = row['numVotes']

        with self.db.engine.connect() as con:
            for link in self.db.fetch_distinct_links():
                if link in full_dict:
                    try:
                        print(self.db._insert_or_update_link_info(con, InputLinkInfo(**full_dict[link])))
                    except:
                        print(full_dict[link])
            con.commit()
        rmdir('data/tmp')


    # Default: pass. To be used to run custom commands against the DB (like filling in new columns)
    def custom_runner(self):
        pass
