from .model.item import Item, InputItem
from .model.box import Box, InputBox
from .model.link import Link, InputLink
from src.model.link import Link as ModelLink
from src.model.box import Box as ModelBox
from .model.link_info import LinkInfo, InputLinkInfo
from .model.file import File, InputFile
import sqlalchemy as sa
from typing import Optional

class DB:
    def __init__(self, engine: sa.Engine) -> None:
        self.engine = engine

    def fetch_all_files(self) -> list[File]:
        with self.engine.connect() as con:
            results = con.execute(
                sa.text('SELECT '
                        'file.id, '
                        'file.name, '
                        'file.file_date, '
                        'file.created_at, '
                        'file.updated_at FROM files file')
            ).fetchall()
        return [File(**file._asdict()) for file in results]

    def fetch_file(self, id: int) -> Optional[File]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'file.id, '
                        'file.name, '
                        'file.file_date, '
                        'file.created_at, '
                        'file.updated_at FROM files file WHERE file.id = :id'),
                {'id': id}
            ).fetchone()
        return File(**result._asdict()) if result is not None else None

    def insert_file(self, file: InputFile) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO files (name, file_date) VALUES(:name, :file_date) RETURNING files.id'),
                file.dict()
            ).first()[0]
            con.commit()
        return id

    def delete_file(self, id: int) -> Optional[int]:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM files WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_link_id_to_files(self, link: str) -> dict[int, File]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id as link_id, '
                        'file.id, '
                        'file.name, '
                        'file.file_date, '
                        'file.created_at, '
                        'file.updated_at FROM links link '
                        'JOIN boxes box ON link.box_id = box.id '
                        'JOIN items item ON box.item_id = item.id '
                        'JOIN files file ON item.file_id = file.id '
                        'WHERE link.link = :link'), {'link': link}
            )
        return {file.link_id: File(**file._asdict()) for file in result.fetchall()}

    def _insert_item(self, con: sa.Connection, item: InputItem) -> int:
        return con.execute(
            sa.text('INSERT INTO items (file_id, x, y) VALUES(:file_id, :x, :y) RETURNING items.id'),
            item.dict()
        ).first()[0]

    def insert_item(self, item: InputItem) -> int:
        with self.engine.connect() as con:
            id = self._insert_item(con, item)
            con.commit()
        return id

    def insert_items(self, items: list[InputItem]) -> list[int]:
        with self.engine.connect() as con:
            ids = [self._insert_item(con, item) for item in items]
            con.commit()
        return ids

    def delete_item(self, id: int) -> Optional[int]:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM items WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_items(self, file_id: int) -> list[Item]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'item.id, '
                        'item.file_id, '
                        'item.x, '
                        'item.y, '
                        'item.created_at, '
                        'item.updated_at FROM items item JOIN files file ON item.file_id = file.id '
                        'WHERE file.id = :file_id'), {'file_id': file_id}
            )
        return [Item(**item._asdict()) for item in result.fetchall()]

    def fetch_link_id_to_items(self, link: str) -> dict[int, Item]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id as link_id, '
                        'item.id, '
                        'item.x, '
                        'item.y, '
                        'item.file_id, '
                        'item.created_at, '
                        'item.updated_at FROM links link '
                        'JOIN boxes box ON link.box_id = box.id '
                        'JOIN items item ON box.item_id = item.id '
                        'WHERE link.link = :link'), {'link': link}
            )
        return {item.link_id: Item(**item._asdict()) for item in result.fetchall()}

    def _insert_box(self, con: sa.Connection, box: InputBox) -> int:
        return con.execute(
            sa.text('INSERT INTO boxes (item_id, left, top, width, height, channel, time, duration_minutes, vcr_code) '
                    'VALUES(:item_id, :left, :top, :width, :height, :channel, :time, :duration_minutes, :vcr_code) RETURNING boxes.id'),
            box.dict()
        ).first()[0]

    def insert_box(self, box: InputBox) -> int:
        with self.engine.connect() as con:
            id = self._insert_box(con, box)
            con.commit()
        return id

    def insert_boxes(self, boxes: list[InputBox]) -> list[int]:
        with self.engine.connect() as con:
            ids = [self._insert_box(con, box) for box in boxes]
            con.commit()
        return ids

    def update_box(self, box: ModelBox) -> Optional[int]:
        with self.engine.connect() as con:
            maybeId = con.execute(
                sa.text('UPDATE boxes '
                        'SET left = :left, '
                        'top = :top, '
                        'width = :width, '
                        'height = :height, '
                        'channel = :channel, '
                        'time = :time, '
                        'duration_minutes = :duration_minutes, '
                        'vcr_code = :vcr_code, '
                        'updated_at = CURRENT_TIMESTAMP '
                        'WHERE id = :id RETURNING id'),
                {'id': box.id, 'left': box.left, 'top': box.top, 'width': box.width, 'height': box.height,
                 'channel': box.channel, 'time': box.formatted_time(),
                 'duration_minutes': box.duration_minutes, 'vcr_code': box.vcr_code}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def delete_box(self, id: int) -> Optional[int]:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM boxes WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_boxes(self, file_id: int) -> list[Box]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'box.id, '
                        'box.item_id, '
                        'box.left, '
                        'box.top, '
                        'box.width, '
                        'box.height, '
                        'box.channel, '
                        'box.time, '
                        'box.duration_minutes, '
                        'box.vcr_code, '
                        'box.created_at, '
                        'box.updated_at FROM boxes box '
                        'JOIN items item ON box.item_id = item.id '
                        'JOIN files file ON item.file_id = file.id '
                        'WHERE file.id = :file_id'), {'file_id': file_id}
            )
        return [Box(**box._asdict()) for box in result.fetchall()]

    def fetch_link_id_to_boxes(self, link: str) -> dict[int, Box]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id as link_id, '
                        'box.id, '
                        'box.item_id, '
                        'box.left, '
                        'box.top, '
                        'box.width, '
                        'box.height, '
                        'box.channel, '
                        'box.time, '
                        'box.duration_minutes, '
                        'box.vcr_code, '
                        'box.created_at, '
                        'box.updated_at FROM links link '
                        'JOIN boxes box ON link.box_id = box.id '
                        'WHERE link.link = :link'), {'link': link}
            )
        return {box.link_id: Box(**box._asdict()) for box in result.fetchall()}

    def fetch_box(self, box_id: int) -> Optional[Box]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'box.id, '
                        'box.item_id, '
                        'box.left, '
                        'box.top, '
                        'box.width, '
                        'box.height, '
                        'box.channel, '
                        'box.time, '
                        'box.duration_minutes, '
                        'box.vcr_code, '
                        'box.created_at, '
                        'box.updated_at FROM boxes box '
                        'WHERE box.id = :id'), {'id': box_id}
            ).fetchone()
        return Box(**result._asdict()) if result is not None else None

    def _insert_link(self, con: sa.Connection, link: InputLink) -> int:
        return con.execute(
            sa.text('INSERT INTO links (box_id, link, confirmed) '
                    'VALUES(:box_id, :link, :confirmed) RETURNING links.id'),
            link.dict()
        ).first()[0]

    def insert_link(self, link: InputLink) -> int:
        with self.engine.connect() as con:
            id = self._insert_link(con, link)
            con.commit()
        return id

    def insert_links(self, links: list[InputLink]) -> list[int]:
        with self.engine.connect() as con:
            ids = [self._insert_link(con, link) for link in links]
            con.commit()
        return ids

    def delete_link(self, id: int) -> Optional[int]:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM links WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def update_link(self, link: ModelLink) -> Optional[int]:
        with self.engine.connect() as con:
            maybeId = con.execute(
                sa.text('UPDATE links '
                        'SET link = :link, '
                        'confirmed = :confirmed, '
                        'updated_at = CURRENT_TIMESTAMP '
                        'WHERE id = :id RETURNING id'),
                {'id': link.id, 'link': link.link, 'confirmed': link.confirmed}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_links(self, file_id: int) -> list[Link]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id, '
                        'link.box_id, '
                        'link.link, '
                        'link.confirmed, '
                        'link.created_at, '
                        'link.updated_at FROM links link '
                        'JOIN boxes box ON link.box_id = box.id '
                        'JOIN items item ON box.item_id = item.id '
                        'JOIN files file ON item.file_id = file.id '
                        'WHERE file.id = :file_id'), {'file_id': file_id}
            )
        return [Link(**link._asdict()) for link in result.fetchall()]

    def fetch_link(self, link_id: int) -> Optional[Link]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id, '
                        'link.box_id, '
                        'link.link, '
                        'link.confirmed, '
                        'link.created_at, '
                        'link.updated_at FROM links link '
                        'WHERE link.id = :id'), {'id': link_id}
            ).fetchone()
        return Link(**result._asdict()) if result is not None else None

    def fetch_box_links(self, box_id: int) -> list[Link]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id, '
                        'link.box_id, '
                        'link.link, '
                        'link.confirmed, '
                        'link.created_at, '
                        'link.updated_at FROM links link '
                        'WHERE link.box_id = :box_id'), {'box_id': box_id}
            )
        return [Link(**l._asdict()) for l in result.fetchall()]

    def fetch_all_links_for_link(self, link: str) -> list[Link]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link.id, '
                        'link.box_id, '
                        'link.link, '
                        'link.confirmed, '
                        'link.created_at, '
                        'link.updated_at FROM links link '
                        'WHERE link.link = :link'), {'link': link}
            )
        return [Link(**l._asdict()) for l in result.fetchall()]

    def fetch_distinct_links(self):
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT DISTINCT link FROM links')
            ).fetchall()
        return [link[0] for link in result]

    def _fetch_link_info_id(self, con: sa.Connection, link_info: InputLinkInfo) -> int | None:
        id = con.execute(
            sa.text('SELECT id FROM link_info WHERE link = :link'),
            link_info.dict()
        ).fetchone()
        if id is not None:
            return id[0]

    def _insert_link_info(self, con: sa.Connection, link_info: InputLinkInfo) -> int:
        return con.execute(
            sa.text('INSERT INTO link_info (link, title, year, rating, votes) '
                    'VALUES(:link, :title, :year, :rating, :votes) RETURNING link_info.id'),
            link_info.dict()
        ).first()[0]

    def _update_link_info(self, con: sa.Connection, link_info: InputLinkInfo, link_info_id: int) -> int:
        return con.execute(
            sa.text('UPDATE link_info '
                    'SET title = :title, year = :year, rating = :rating, votes = :votes, updated_at = CURRENT_TIMESTAMP '
                    'WHERE id = :id RETURNING id'),
            {'title': link_info.title, 'year': link_info.year, 'rating': link_info.rating, 'votes': link_info.votes, 'id': link_info_id}
        ).first()[0]

    def _insert_or_update_link_info(self, con: sa.Connection, link_info: InputLinkInfo) -> int:
        maybe_id = self._fetch_link_info_id(con, link_info)
        if maybe_id is None:
            id = self._insert_link_info(con, link_info)
        else:
            id = self._update_link_info(con, link_info, maybe_id)
        return id

    def insert_or_update_link_info(self, link_info: InputLinkInfo) -> int:
        with self.engine.connect() as con:
            id = self._insert_or_update_link_info(con, link_info)
            con.commit()
        return id

    def fetch_file_links_info(self, file_id: int) -> list[LinkInfo]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link_info.id, '
                        'link_info.link, '
                        'link_info.title, '
                        'link_info.year, '
                        'link_info.rating, '
                        'link_info.votes, '
                        'link_info.created_at, '
                        'link_info.updated_at FROM link_info link_info '
                        'JOIN links link ON link_info.link = link.link '
                        'JOIN boxes box ON link.box_id = box.id '
                        'JOIN items item ON box.item_id = item.id '
                        'JOIN files file ON item.file_id = file.id '
                        'WHERE file.id = :file_id'), {'file_id': file_id}
            )
        return [LinkInfo(**link_info._asdict()) for link_info in result.fetchall()]

    def get_link_info(self, link: str) -> Optional[LinkInfo]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'link_info.id, '
                        'link_info.link, '
                        'link_info.title, '
                        'link_info.year, '
                        'link_info.rating, '
                        'link_info.votes, '
                        'link_info.created_at, '
                        'link_info.updated_at FROM link_info link_info '
                        'WHERE link_info.link = :link'), {'link': link}
            ).fetchone()
        if result is not None:
            return LinkInfo(**result._asdict())
