from flask import Flask
from util.config import Config

config = Config()
app = Flask(__name__)

# TODO: Add in wrapper to check api key on each call automatically
# TODO: Add in api portion where the db connection will exist so that this is just parsing arguments and reformatting responses for frontend
# TODO: Start with just asking for the list of files, will want to convert from pydantic classes to internal model at this point
@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

if __name__ == '__main__':
   app.run(debug = True)
