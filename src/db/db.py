import sqlalchemy as sa
from model.item import Item

class DB:
    engine: sa.Engine = sa.create_engine('sqlite:///../../data/NYTListings.db')

    def fetch_all_items(self) -> list[Item]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT * FROM items')
            )
        return [Item(**item._asdict()) for item in result.fetchall()]

    def insert_item(self, filename: str, x: int, y: int) -> int:
        with self.engine.connect() as con:
            id = con.execute(
                sa.text('INSERT INTO items (filename, x, y) VALUES(:filename, :x, :y) RETURNING items.id'),
                {'filename': filename, 'x': x, 'y': y}
            ).first()[0]
            con.commit()
        return id

    def delete_item(self, id: int) -> int | None:
        with self.engine.connect() as con:
            maybeId = con.execute(
                sa.text('DELETE FROM items WHERE id = :id RETURNING id'), {'id': id}
            ).first()
            con.commit()
        return maybeId[0] if maybeId is not None else None

    def fetch_file_items(self, filename: str) -> list[Item]:
        with self.engine.connect() as con:
            result = con.execute(
                sa.text('SELECT * FROM items WHERE filename = :filename'), {'filename': filename}
            )
        return [Item(**item._asdict()) for item in result.fetchall()]

db = DB()
# print(db.delete_item(5))
# print(db.insert_item('test2.png', 0, 0))
# print(db.insert_item('test2.png', 0, 0))
for item in db.fetch_all_items():
    print(item)
