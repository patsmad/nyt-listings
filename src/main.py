from builder import api_builder
from flask import Flask
from util.config import Config

config = Config()
app = Flask(__name__)

api = api_builder.build()

# TODO: Add in wrapper to check api key on each call automatically
@app.route('/files/')
def files() -> list[dict]:
   return [file.to_dict() for file in api.get_all_files()]

@app.route('/items/')
def items() -> list[dict]:
   return [item.to_dict() for item in api.get_all_items()]

@app.route('/boxes/')
def boxes() -> list[dict]:
   return [box.to_dict() for box in api.get_all_boxes()]

@app.route('/links/')
def links() -> list[dict]:
   return [link.to_dict() for link in api.get_all_links()]

if __name__ == '__main__':
   app.run(debug = True)
