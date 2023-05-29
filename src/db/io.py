from src.util.io import readJSON
from .db import DB
from .model.box import InputBox
from .model.file import InputFile
from .model.item import InputItem
from .model.link import InputLink

class DBIO:
    def __init__(self, db: DB):
        self.db = db

    def to_input_item(self, file_id: int, item: dict) -> InputItem:
        return InputItem(file_id=file_id, x=item['x'], y=item['y'])
    def to_input_box(self, item_id: int, box: dict) -> InputBox:
        return InputBox(item_id=item_id, left=box['left'], top=box['top'], width=box['width'], height=box['height'])

    def to_input_link(self, box_id: int, link: dict) -> InputLink:
        confirmed: bool = link['confirmed'] if link['confirmed'] is not None else False
        return InputLink(box_id=box_id, link=link['link'], confirmed=confirmed)

    # TODO: Would be nice to have an add / replace option here
    def from_file_to_db(self, fname) -> None:
        files_to_add: dict = readJSON(fname)
        for file in files_to_add:
            file_id: int = self.db.insert_file(InputFile(**{'name': file['name']}))
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
