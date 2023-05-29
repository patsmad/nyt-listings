from api.api import API
from builder import api_builder, db_io_builder
import click
from db.io import DBIO
from flask import Flask, request
from flask_cors import CORS
from util.config import Config

config = Config()
app = Flask(__name__)
CORS(app)

api: API = api_builder.build()
db_io: DBIO = db_io_builder.build()

@app.route('/files/', methods=['GET'])
@config.api_check
def files() -> list[dict]:
   return [file.to_dict() for file in api.get_all_files()]

@app.route('/file/', methods=['GET'])
@config.api_check
def file() -> dict:
   file_id: int = int(request.args.get('file_id'))
   if file_id is not None:
      return api.get_file(file_id).to_dict()
   else:
      raise Exception('Must provide ?filename=<filename> for file request')

@click.group()
def cli():
    pass

@click.command()
@click.argument('filename')
def from_file_to_db(filename):
    db_io.from_file_to_db(filename)

@click.command()
def update_imdb_data():
    db_io.update_imdb_data()

@click.command()
def server():
    app.run(debug=True)

cli.add_command(server)
cli.add_command(from_file_to_db)
cli.add_command(update_imdb_data)

# TODO: AllLinks would be the next most useful endpoint here. It would return a list of FileLinks which would
# be something like FileLink(file_id, file_name, item_id, box_id, link)
# The item/box info is somewhat unnecessary at the moment, this would be for a table for example
# Eventually we'd also want to produce an AnnotatedFile whereby you can specific the specific single link to make the file from
# Those would need the ability to get a single item and box based on id
# But first I think I would like to put the above endpoint to work on a frontend system

if __name__ == '__main__':
    cli()
