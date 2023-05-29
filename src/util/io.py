import gzip
import json
import os
from requests import get
import shutil

file_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = f'{file_path}/../..'

def pathExists(fname: str) -> bool:
    return os.path.exists(f'{data_path}/{fname}')

def mkdir(fname):
    if not pathExists(fname):
        os.mkdir(f'{data_path}/{fname}')

def rmdir(fname):
    if pathExists(fname):
        shutil.rmtree(f'{data_path}/{fname}')

def readJSON(fname: str) -> dict | list:
    with open(f'{data_path}/{fname}', 'r') as f:
        data = json.load(f)
    return data

def readOrCreateJSON(fname: str) -> dict | list:
    if not pathExists(fname):
        writeJSON({}, fname)
    return readJSON(fname)

def writeJSON(data: dict | list, fname: str) -> None:
    with open(f'{data_path}/{fname}', 'w') as f:
        json.dump(data, f)

def removeFile(fname):
    os.remove(f'{data_path}/{fname}')

def downloadFile(url, save_path):
    r = get(url, stream=True)
    with open(f'{data_path}/{save_path}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

def unzipGZFile(fname):
    with gzip.open(f'{data_path}/{fname}', 'rb') as f_in:
        with open(f'{data_path}/{fname.replace(".gz", "")}', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    removeFile(fname)

def readTSV(fname):
    with open(f'{data_path}/{fname}', 'r', encoding="utf8") as f:
        header = f.readline().strip().split('\t')
        line = f.readline().strip()
        while len(line) > 0:
            yield {header: datum for header, datum in zip(header, line.split('\t'))}
            line = f.readline().strip()
