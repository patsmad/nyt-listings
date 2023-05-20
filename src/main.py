from api.api import API
from api.fetcher import Fetcher
from db.db import DB
from model.builder import FileBuilder
from util.config import Config

from flask import Flask
import sqlalchemy as sa

config = Config()
app = Flask(__name__)

# TODO: This is correct, but might want to think through best practice
engine: sa.Engine = sa.create_engine('sqlite:///../data/NYTListings.db')
db: DB = DB(engine)
fileBuilder: FileBuilder = FileBuilder()
fetcher: Fetcher = Fetcher(db, fileBuilder)
api: API = API(fetcher)

# TODO: Add in wrapper to check api key on each call automatically
@app.route('/files/')
def files():
   return [file.to_dict() for file in api.get_all_files()]

if __name__ == '__main__':
   app.run(debug = True)
