import json
from logging.config import dictConfig

from flask import Flask
# Trying to find module in the parent package
from flask.logging import default_handler

from src.models.Organisation import Organisation
from src.utils import ComplexEncoder

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

app.logger.removeHandler(default_handler)
x = Organisation("My Org")
x.read_data_from_json_file('src/resources/Components.json')


@app.route('/organisation')
def get_organisation():
    return json.dumps(x.reprJSON(), cls=ComplexEncoder)


@app.route('/user/<user_id>')
def getuser(user_id):
    app.logger.info('*****    Looking for userID (%s)  *****', user_id)

    for u in x.users:
        if u.user_id == user_id:
            return json.dumps(u.reprJSON(), cls=ComplexEncoder), 200
    app.logger.error('no users found')
    return {}, 404


@app.route('/')
def not_found():
    return 'Error'
