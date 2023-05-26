from builder import api_builder
from flask import Flask, request
from flask_cors import CORS
from util.config import Config

config = Config()
app = Flask(__name__)
CORS(app)

api = api_builder.build()

@app.route('/files/', methods=['GET'])
@config.api_check
def files() -> list[dict]:
   return [file.to_dict() for file in api.get_all_files()]

@app.route('/file/', methods=['GET'])
@config.api_check
def file() -> dict:
   filename = request.args.get('filename')
   if filename is not None:
      return api.get_file(filename).to_dict()
   else:
      raise Exception('Must provide ?filename=<filename> for file request')

if __name__ == '__main__':
   app.run(debug = True)
