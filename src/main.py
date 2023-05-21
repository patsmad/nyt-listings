from api.api import API
from api.fetcher import Fetcher
from db.db import DB
from util.config import Config

from flask import Flask
import sqlalchemy as sa

config = Config()
app = Flask(__name__)

# TODO: This is correct, but might want to think through best practice
engine: sa.Engine = sa.create_engine('sqlite:///../data/NYTListings.db')
db: DB = DB(engine)
fetcher: Fetcher = Fetcher(db)
api: API = API(fetcher)

# TODO: Add in wrapper to check api key on each call automatically
@app.route('/files/')
def files() -> list[dict]:
   return [file.to_dict() for file in api.get_all_files()]

# TODO: This should return file data in addition to items (not file_id). Item class?
@app.route('/items/')
def items() -> list[dict]:
   return [item.to_dict() for item in api.get_all_items()]

if __name__ == '__main__':
   app.run(debug = True)
