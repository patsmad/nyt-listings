import json
import os

file_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = f'{file_path}/../..'

def readJSON(fname: str) -> dict:
    with open(f'{data_path}/{fname}', 'r') as f:
        data = json.load(f)
    return data
