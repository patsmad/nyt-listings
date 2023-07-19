from src.util.util_io import readJSON, downloadFile, unzipGZFile, readTSV, mkdir, rmdir, data_path
from src.util.image import open_image, crop_image
from src.util.ocr import get_text
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

    def from_file_to_db(self, fname) -> None:
        files_to_add: dict = readJSON(fname)
        for file in files_to_add:
            file_id: int = self.db.insert_file(InputFile(**{'name': file['name'], 'date': None}))
            count = 0
            with self.db.engine.connect() as con:
                for item in file['items']:
                    count += 1
                    item_id: int = self.db._insert_item(con,self.to_input_item(file_id, item))
                    for box in item['boxes']:
                        box_id: int = self.db._insert_box(con, self.to_input_box(item_id, box))
                        for link in box['links']:
                            self.db._insert_link(con, self.to_input_link(box_id, link))
                con.commit()
            print(file_id, count)

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

    def fill_vcr_links(self, links):
        for link in links.split(','):
            vcr_code_pattern: re.Pattern = re.compile('[^0-9]+([0-9]{5,})[^0-9]*')
            link_links = self.db.fetch_all_links_for_link(link)
            link_to_boxes = self.db.fetch_link_id_to_boxes(link)
            link_to_files = self.db.fetch_link_id_to_files(link)
            for link_link in link_links:
                box = link_to_boxes[link_link.id]
                file = link_to_files[link_link.id]
                if box.vcr_code is None:
                    img = open_image(f'{data_path}/data/files/{file.name}')
                    cropped_image = crop_image(img, box.left, box.top, box.width, box.height)
                    text = get_text(cropped_image)
                    vcr_codes = re.findall(vcr_code_pattern, text)
                    if len(vcr_codes) > 0:
                        vcr_code = vcr_codes[0]
                        year, month, day = file.file_date.year, file.file_date.month, file.file_date.day
                        payload = {'id': box.id, 'year': year, 'month': month, 'day': day, 'vcr_code': vcr_code}
                        id = self.api.update_box(payload)
                        print(id, payload)
                    else:
                        print('No VCR Code found')
                else:
                    print('VCR Code already found')

    def fill_vcr_files(self, files):
        for file in glob.glob(f'{data_path}/data/files/{files}'):
            file_name = os.path.basename(file)
            print(file_name)
            file = self.db.fetch_file_by_name(file_name)
            vcr_code_pattern: re.Pattern = re.compile('[^0-9]+([0-9]{5,})[^0-9]*')
            links = self.db.fetch_file_links(file.id)
            box_by_box_id = {box.id: box for box in self.db.fetch_file_boxes(file.id)}
            for link in links:
                box = box_by_box_id[link.box_id]
                if box.vcr_code is None:
                    img = open_image(f'{data_path}/data/files/{file.name}')
                    cropped_image = crop_image(img, box.left, box.top, box.width, box.height)
                    text = get_text(cropped_image)
                    vcr_codes = re.findall(vcr_code_pattern, text)
                    if len(vcr_codes) > 0:
                        vcr_code = vcr_codes[0]
                        year, month, day = file.file_date.year, file.file_date.month, file.file_date.day
                        payload = {'id': box.id, 'year': year, 'month': month, 'day': day, 'vcr_code': vcr_code}
                        id = self.api.update_box(payload)
                        print(id, payload)
                    else:
                        print('No VCR Code found')
                else:
                    print('VCR Code already found')


    # Default: pass. To be used to run custom commands against the DB (like filling in new columns)
    def custom_runner(self):
        pass
