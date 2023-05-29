import json
import os

file_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = f'{file_path}/../..'

def pathExists(fname: str) -> bool:
    return os.path.exists(f'{data_path}/{fname}')

def readJSON(fname: str) -> dict | list:
    with open(f'{data_path}/{fname}', 'r') as f:
        data = json.load(f)
    return data

def readOrCreateJSON(fname: str) -> dict | list:
    if not pathExists(f'{data_path}/{fname}'):
        writeJSON({}, fname)
    return readJSON(fname)

def writeJSON(data: dict | list, fname: str) -> None:
    with open(f'{data_path}/{fname}', 'w') as f:
        json.dump(data, f)
