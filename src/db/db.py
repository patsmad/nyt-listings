from .model.item import Item
from .model.box import Box
from .model.link import Link
from .model.file import File
import sqlalchemy as sa

class DB:
    def __init__(self, engine: sa.Engine):
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

    def insert_file(self, name: str) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO files (name) VALUES(:name) RETURNING files.id'),
                {'name': name}
            ).first()[0]
            con.commit()
        return id

    def delete_file(self, name: str) -> int | None:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM files WHERE name = :name RETURNING id'), {'name': name}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_all_items(self) -> list[Item]:
        with self.engine.connect() as con:
            results = con.execute(
                sa.text('SELECT '
                        'item.id, '
                        'item.file_id, '
                        'item.x, '
                        'item.y, '
                        'item.created_at, '
                        'item.updated_at FROM items item')
            ).fetchall()
        return [Item(**item._asdict()) for item in results]

    def insert_item(self, file_id: int, x: int, y: int) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO items (file_id, x, y) VALUES(:file_id, :x, :y) RETURNING items.id'),
                {'file_id': file_id, 'x': x, 'y': y}
            ).first()[0]
            con.commit()
        return id

    def delete_item(self, id: int) -> int | None:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM items WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_items(self, filename: str) -> list[Item]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT '
                        'item.id, '
                        'item.file_id, '
                        'item.x, '
                        'item.y, '
                        'item.created_at, '
                        'item.updated_at FROM items item JOIN files file ON item.file_id = file.id '
                        'WHERE file.name = :filename'), {'filename': filename}
            )
        return [Item(**item._asdict()) for item in result.fetchall()]

    def fetch_all_boxes(self) -> list[Box]:
        with self.engine.connect() as con:
            results = con.execute(
                sa.text('SELECT '
                        'box.id, '
                        'box.item_id, '
                        'box.left, '
                        'box.top, '
                        'box.width, '
                        'box.height, '
                        'box.created_at, '
                        'box.updated_at FROM boxes box')
            ).fetchall()
        return [Box(**box._asdict()) for box in results]

    def insert_box(self, item_id: int, left: int, top: int, width: int, height: int) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO boxes (item_id, left, top, width, height) '
                        'VALUES(:item_id, :left, :top, :width, :height) RETURNING boxes.id'),
                {'item_id': item_id, 'left': left, 'top': top, 'width': width, 'height': height}
            ).first()[0]
            con.commit()
        return id

    def delete_box(self, id: int) -> int | None:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM boxes WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_boxes(self, filename: str) -> list[Box]:
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
                        'WHERE file.name = :filename'), {'filename': filename}
            )
        return [Box(**box._asdict()) for box in result.fetchall()]

    def fetch_all_links(self) -> list[Link]:
        with self.engine.connect() as con:
            results = con.execute(
                sa.text('SELECT '
                        'link.id, '
                        'link.box_id, '
                        'link.link, '
                        'link.confirmed, '
                        'link.created_at, '
                        'link.updated_at FROM links link')
            ).fetchall()
        return [Link(**link._asdict()) for link in results]

    def insert_link(self, box_id: int, link: str, confirmed: bool | None = None) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO links (box_id, link, confirmed) '
                        'VALUES(:box_id, :link, :confirmed) RETURNING links.id'),
                {'box_id': box_id, 'link': link, 'confirmed': confirmed if confirmed is not None else 0}
            ).first()[0]
            con.commit()
        return id

    def delete_link(self, id: int) -> int | None:
        with self.engine.connect() as con:
            con.execute(sa.text('PRAGMA foreign_keys = ON'))
            maybeId = con.execute(
                sa.text('DELETE FROM links WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_links(self, filename: str) -> list[Link]:
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
                        'WHERE file.name = :filename'), {'filename': filename}
            )
        return [Link(**link._asdict()) for link in result.fetchall()]
