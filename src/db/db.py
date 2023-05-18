from model.item import Item
from model.box import Box
from model.link import Link
import sqlalchemy as sa

class DB:
    engine: sa.Engine = sa.create_engine('sqlite:///../../data/NYTListings.db')

    def fetch_all_items(self) -> list[Item]:
        with self.engine.connect() as con:
            results = con.execute(
                sa.text('SELECT '
                        'item.id, '
                        'item.filename, '
                        'item.x, '
                        'item.y, '
                        'item.created_at, '
                        'item.updated_at FROM items item')
            ).fetchall()
        return [Item(**item._asdict()) for item in results]

    def insert_item(self, filename: str, x: int, y: int) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO items (filename, x, y) VALUES(:filename, :x, :y) RETURNING items.id'),
                {'filename': filename, 'x': x, 'y': y}
            ).first()[0]
            con.commit()
        return id

    # TODO: add foreign key support as event listener on all sqlalchemy events
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
                        'item.filename, '
                        'item.x, '
                        'item.y, '
                        'item.created_at, '
                        'item.updated_at FROM items item WHERE filename = :filename'), {'filename': filename}
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

    # TODO: add foreign key support as event listener on all sqlalchemy events
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
                        'WHERE item.filename = :filename'), {'filename': filename}
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

    # TODO: add foreign key support as event listener on all sqlalchemy events
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
                        'WHERE item.filename = :filename'), {'filename': filename}
            )
        return [Link(**link._asdict()) for link in result.fetchall()]
