from api.api import API
from builder import api_builder, db_io_builder, poster_fetcher_builder
import click
from db.io import DBIO
from analysis.posters import PosterFetcher
from flask import Flask, request, send_from_directory, Response, send_file
from flask_cors import CORS
import json
import re
from util.config import Config
from util.util_io import data_path, pathExists
from util.image import open_image, crop_image, image_to_buf
from typing import Optional

config = Config()
app = Flask(__name__)
CORS(app)

api: API = api_builder.build()
db_io: DBIO = db_io_builder.build()
poster_fetcher: PosterFetcher = poster_fetcher_builder.build()


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
    maybe_box: Optional[str] = request.args.get('box')
    if maybe_file_id is not None:
        file_name: Optional[str] = api.get_file_name(int(maybe_file_id))
        if file_name is not None and pathExists(f'data/files/{file_name}'):
            if maybe_box is None:
                return send_from_directory(f'{data_path}/data/files', file_name)
            else:
                left, top, width, height = map(int, maybe_box.split(','))
                img = open_image(f'{data_path}/data/files/{file_name}')
                buf = image_to_buf(crop_image(img, left, top, width, height))
                return send_file(buf, 'image/png')
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

@app.route('/item/add/', methods=['POST'])
@config.api_check
def item_add() -> dict:
    payload: dict = json.loads(request.data)
    id: int = api.add_item(payload)
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

@app.route('/box/update/', methods=['POST'])
@config.api_check
def box_update() -> dict:
    payload: dict = json.loads(request.data)
    updated_id: Optional[int] = api.update_box(payload)
    if updated_id is not None:
        return {'id': updated_id}
    else:
        raise Exception('Box id <{}> not found'.format(payload.get('id')))

@app.route('/vcr_code/update/', methods=['POST'])
@config.api_check
def vcr_code_update() -> dict:
    payload: dict = json.loads(request.data)
    updated_id: Optional[int] = api.update_box(payload)
    if updated_id is not None:
        return {'id': updated_id}
    else:
        raise Exception('Box id <{}> not found'.format(payload.get('id')))

@app.route('/channel/update/', methods=['POST'])
@config.api_check
def channel_update() -> dict:
    payload: dict = json.loads(request.data)
    updated_id: Optional[int] = api.update_box(payload)
    if updated_id is not None:
        return {'id': updated_id}
    else:
        raise Exception('Box id <{}> not found'.format(payload.get('id')))

@app.route('/time/update/', methods=['POST'])
@config.api_check
def time_update() -> dict:
    payload: dict = json.loads(request.data)
    updated_id: Optional[int] = api.update_box(payload)
    if updated_id is not None:
        return {'id': updated_id}
    else:
        raise Exception('Box id <{}> not found'.format(payload.get('id')))

@app.route('/duration/update/', methods=['POST'])
@config.api_check
def duration_update() -> dict:
    payload: dict = json.loads(request.data)
    updated_id: Optional[int] = api.update_box(payload)
    if updated_id is not None:
        return {'id': updated_id}
    else:
        raise Exception('Box id <{}> not found'.format(payload.get('id')))

@app.route('/poster/', methods=['GET'])
@config.api_check
def poster() -> Response:
    maybe_link: Optional[str] = request.args.get('link')
    if maybe_link is not None:
        key: list = re.findall('https://www.imdb.com/title/(.*)/', maybe_link)
        if len(key) > 0 and pathExists(f'data/posters/{key[0]}.jpg'):
            return send_from_directory(f'{data_path}/data/posters', f'{key[0]}.jpg')
        else:
            return send_from_directory(f'{data_path}/data/posters', 'no_poster.jpg')
    else:
        raise Exception('Must provide ?link=<link> for poster request')

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
def fill_missing_posters():
    poster_fetcher.fill_missing_posters()

@click.command()
def custom_runner():
    db_io.custom_runner()

@click.command()
@click.argument('links')
def fill_vcr_links(links):
    db_io.fill_vcr_links(links)

@click.command()
@click.argument('files')
def fill_vcr_files(files):
    db_io.fill_vcr_files(files)

@click.command()
def server():
    app.run(debug=True)

cli.add_command(server)
cli.add_command(from_file_to_db)
cli.add_command(update_imdb_data)
cli.add_command(fill_missing_posters)
cli.add_command(custom_runner)
cli.add_command(fill_vcr_links)
cli.add_command(fill_vcr_files)

if __name__ == '__main__':
    cli()
