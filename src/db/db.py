from .model.item import Item, InputItem
from .model.box import Box, InputBox
from .model.link import Link, InputLink
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
                        'file.created_at, '
                        'file.updated_at FROM files file WHERE file.id = :id'),
                {'id': id}
            ).fetchone()
        return File(**result._asdict()) if result is not None else None

    def insert_file(self, file: InputFile) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO files (name) VALUES(:name) RETURNING files.id'),
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

    def _insert_box(self, con: sa.Connection, box: InputBox) -> int:
        return con.execute(
            sa.text('INSERT INTO boxes (item_id, left, top, width, height) '
                    'VALUES(:item_id, :left, :top, :width, :height) RETURNING boxes.id'),
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
                        'box.created_at, '
                        'box.updated_at FROM boxes box '
                        'JOIN items item ON box.item_id = item.id '
                        'JOIN files file ON item.file_id = file.id '
                        'WHERE file.id = :file_id'), {'file_id': file_id}
            )
        return [Box(**box._asdict()) for box in result.fetchall()]

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
