from builder import api_builder
from flask import Flask
from flask_cors import CORS
from util.config import Config

config = Config()
app = Flask(__name__)
CORS(app)

api = api_builder.build()

@app.route('/files/')
@config.api_check
def files() -> list[dict]:
   return [file.to_dict() for file in api.get_all_files()]

@app.route('/items/')
@config.api_check
def items() -> list[dict]:
   return [item.to_dict() for item in api.get_all_items()]

@app.route('/boxes/')
@config.api_check
def boxes() -> list[dict]:
   return [box.to_dict() for box in api.get_all_boxes()]

@app.route('/links/')
@config.api_check
def links() -> list[dict]:
   return [link.to_dict() for link in api.get_all_links()]

if __name__ == '__main__':
   app.run(debug = True)
