from .io import readJSON

class Config:
    def __init__(self):
        config: dict = readJSON('config')
        self.api_key: str = config['api-key']

    def api_key_match(self, api_key: str) -> bool:
        return api_key == self.api_key
