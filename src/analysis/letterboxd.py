from src.db.db import DB
from src.db.model.link import Link
from src.db.model.box import Box
from datetime import datetime, timedelta

# TODO: This is maybe a more general concept that needs to be put elsewhere
class LetterboxdBox:
    def __init__(self, link: Link, box: Box) -> None:
        self.link = link.link
        self.channel = box.channel
        self.time = box.time
        self.duration_minutes = box.duration_minutes

    def __eq__(self, other):
        return self.link == other.link and \
            self.channel == other.channel and \
            self.time == other.time and \
            self.duration_minutes == other.duration_minutes

    def __hash__(self):
        return hash(self.link) + hash(self.channel) + hash(self.time) + hash(self.duration_minutes)

    def str_time(self):
        return self.time.strftime('%Y-%m-%d %I:%M %p')

    def str_time_channel(self):
        return f'{self.str_time()} ({self.channel})'

    def __str__(self):
        return f'{self.link} {self.str_time_channel()}'

    def intersect(self, start_dt, end_dt):
        start_time = self.time
        end_time = self.time + timedelta(minutes=self.duration_minutes)
        return (start_time <= start_dt and end_time > start_dt) or \
            (end_time >= end_dt and start_time < end_dt) or \
            (start_time >= start_dt and end_time <= end_dt)

class Letterboxd:
    def __init__(self, db: DB) -> None:
        self.db: DB = db

    # TODO: Split out the unique/filter/sort into a separate function which this will take in
    def file_films(self, name: str, file_id: int, start_time: datetime, end_time: datetime) -> None:
        links: list[Link] = self.db.fetch_file_links(file_id)
        box_by_box_id: dict[int, Box] = {box.id: box for box in self.db.fetch_file_boxes(file_id)}
        link_id_to_box: dict[int, Box] = {link.id: box_by_box_id[link.box_id] for link in links}
        unique_boxes = set(LetterboxdBox(link, link_id_to_box[link.id]) for link in links)
        filtered_boxed = [b for b in unique_boxes if b.intersect(start_time, end_time)]
        sorted_boxes = sorted(filtered_boxed, key=lambda b: b.time)
        with open(f'../../data/letterboxd/{name}.csv', 'w') as f:
            f.write('Position,Const,Review\n')
            for i, box in enumerate(sorted_boxes):
                print(box.str_time_channel())
                f.write(f"{str(i)},{box.link.split('/title/')[1].split('/')[0]},{box.str_time_channel()}\n")
