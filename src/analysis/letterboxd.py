from src.db.db import DB
from src.db.model.link import Link
from src.db.model.box import Box
from datetime import datetime, timedelta
from typing import Callable

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

    def str_date(self):
        return self.time.strftime('%Y-%m-%d')

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

    def start_time_bound(self, start_dt: datetime, end_dt: datetime) -> bool:
        start_time = self.time
        return start_time >= start_dt and start_time <= end_dt

class Letterboxd:
    def __init__(self, db: DB) -> None:
        self.db: DB = db

    # TODO: Split out the unique/filter/sort into a separate function which this will take in
    def file_films(self, name: str, file_ids: list[int], start_time: datetime, end_time: datetime) -> None:
        links: list[Link] = [link for file_id in file_ids for link in self.db.fetch_file_links(file_id)]
        box_by_box_id: dict[int, Box] = {box.id: box for file_id in file_ids for box in self.db.fetch_file_boxes(file_id)}
        link_id_to_box: dict[int, Box] = {link.id: box_by_box_id[link.box_id] for link in links}
        unique_boxes = set(LetterboxdBox(link, link_id_to_box[link.id]) for link in links)
        filtered_boxes = [b for b in unique_boxes if b.time is not None and b.start_time_bound(start_time, end_time)]
        sorted_boxes = sorted(filtered_boxes, key=lambda b: b.time)
        box_list = {}
        for box in sorted_boxes:
            if box.link not in box_list:
                box_list[box.link] = []
            box_list[box.link].append(box)
        sorted_links = sorted(box_list, key=lambda link: box_list[link][0].time)
        with open(f'../../data/letterboxd/{name}.csv', 'w') as f:
            f.write('Position,Const,Review\n')
            for i, link in enumerate(sorted_links):
                note = ' '.join([box.str_time_channel() for box in box_list[link]])
                print(link, note)
                f.write(f"{str(i)},{link.split('/title/')[1].split('/')[0]},{note}\n")

    # TODO: For now I'll just grab all links in the files themselves, later I'll use unique
    def link_films(self, name: str, link: str) -> None:
        file_map = {file.id: file.name.split('.')[0] for file in self.db.fetch_link_id_to_files(link).values()}
        link_map: dict[str, list[str]] = {}
        for file_id, file_name in file_map.items():
            for link in self.db.fetch_file_links_info(file_id):
                if link.link not in link_map:
                    link_map[link.link] = []
                link_map[link.link].append(file_name)
        with open(f'../../data/letterboxd/{name}.csv', 'w') as f:
            f.write('Position,Const,Review\n')
            for i, (link, file_names) in enumerate(link_map.items()):
                f.write(f"{str(i)},{link.split('/title/')[1].split('/')[0]},{' '.join(file_names)}\n")

    def channel_films(self, name: str, channel: str, start_time: datetime, end_time: datetime, time_delta: timedelta) -> None:
        boxes = []
        time = start_time
        while time <= end_time:
            print(time)
            for box in self.db.fetch_channel_time_box(channel, time):
                links = self.db.fetch_box_links(box.id)
                for link in links:
                    boxes.append(LetterboxdBox(link, box))
            time += time_delta
        unique_boxes = set(boxes)
        print(len(unique_boxes))
        sorted_boxes = sorted(unique_boxes, key=lambda b: b.time)
        link_to_boxes = {}
        for box in sorted_boxes:
            if box.link not in link_to_boxes:
                link_to_boxes[box.link] = []
            link_to_boxes[box.link].append(box)
        sorted_links = sorted(link_to_boxes, key=lambda x: link_to_boxes[x][0].time)
        with open(f'../../data/letterboxd/{name}.csv', 'w') as f:
            f.write('Position,Const,Review\n')
            for i, link in enumerate(sorted_links):
                all_times = '; '.join([box.str_date() for box in link_to_boxes[link]])
                print(link, all_times)
                f.write(f"{str(i)},{link.split('/title/')[1].split('/')[0]},{all_times}\n")

# import sqlalchemy as sa
# engine = sa.create_engine('sqlite:///../../data/NYTListings.db')
# db = DB(engine)
# l = Letterboxd(db)
# start_time = datetime(1990, 1, 1, 20, 0, 0)
# end_time = datetime(1991, 1, 1, 19, 0, 0)
# l.channel_films('SHO_1990_8PM', 'SHO', start_time, end_time, timedelta(days = 1))
# l.channel_films('MAX_1990_8PM', 'MAX', start_time, end_time, timedelta(days = 1))
# l.channel_films('HBO_1990_8PM', 'HBO', start_time, end_time, timedelta(days = 1))
# l.link_films('Clifford', 'https://www.imdb.com/title/tt0109447/')
# l.file_films('Sept1_1999', [3529, 3530], datetime(1999, 9, 1, 0, 0), datetime(1999, 9, 1, 23, 59))
