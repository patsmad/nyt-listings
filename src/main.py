from api.api import API
from builder import api_builder, db_io_builder
import click
from db.io import DBIO
from flask import Flask, request, send_from_directory, Response
from flask_cors import CORS
import json
from util.config import Config
from util.io import data_path, pathExists
from typing import Optional

config = Config()
app = Flask(__name__)
CORS(app)

api: API = api_builder.build()
db_io: DBIO = db_io_builder.build()


# TODO: Exceptions should be HTTP errors with a BMT themed splash page
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

@app.route('/link/', methods=['GET'])
@config.api_check
def link() -> dict:
   link: str = request.args.get('link')
   if link is not None:
       return api.get_link(link).to_dict()
   else:
       raise Exception('Must provide ?link=<link> for link request')

@app.route('/img/', methods=['GET'])
@config.api_check
def img() -> Response:
    maybe_file_id: Optional[str] = request.args.get('file_id')
    if maybe_file_id is not None:
        file_name: Optional[str] = api.get_file_name(int(maybe_file_id))
        if file_name is not None and pathExists(f'data/files/{file_name}'):
            return send_from_directory(f'{data_path}/data/files', file_name)
        else:
            raise Exception('Invalid filename request')
    else:
        raise Exception('Must provide ?filename=<filename> for img request')

@app.route('/link/update/', methods=['POST'])
@config.api_check
def link_update() -> dict:
    payload: dict = json.loads(request.data)
    updated_id: Optional[int] = api.update_link(payload)
    if updated_id is not None:
        return {'id': updated_id}
    else:
        raise Exception('Link id <{}> not found'.format(payload.get('id')))

@app.route('/link/add/', methods=['POST'])
@config.api_check
def link_add() -> dict:
    payload: dict = json.loads(request.data)
    id: int = api.add_link(payload)
    return {'id': id}

@app.route('/item/delete/', methods=['POST'])
@config.api_check
def item_delete() -> dict:
    payload: dict = json.loads(request.data)
    id: Optional[int] = api.delete_item(payload)
    if id is not None:
        return {'id': id}
    else:
        raise Exception('Item id <{}> not found'.format(payload.get('id')))

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
