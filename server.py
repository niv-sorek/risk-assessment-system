import json
import sys
from os.path import dirname, abspath

from flask import Flask, jsonify, request

# Trying to find module in the parent package
from src.models.Organisation import Organisation
from src.utils import ComplexEncoder

app = Flask(__name__)

x = Organisation("My Org")
x.read_data_from_json_file('src/resources/Components.json')


@app.route('/organisation')
def get_organisation():
    return json.dumps(x.reprJSON(), cls=ComplexEncoder)


@app.route('/user/<user_id>')
def getuser(user_id):
    for u in x.users:
        if u.user_id == user_id:
            return json.dumps(u.reprJSON(), cls=ComplexEncoder)
    return 'not found'


@app.route('/')
def not_found():
    return 'Error'
