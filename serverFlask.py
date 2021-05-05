import os

from flask import Flask, request
from src.models.Organisation import Organisation
from src.utils import ComplexEncoder
import json
from flask_cors import CORS

from pycvesearch import CVESearch

#### https://raw.githubusercontent.com/olbat/nvdcve/master/nvdcve/CVE-YYYY-XXXX.json
app = Flask(__name__)
CORS(app)
x = Organisation("src/resources/Components.json")


# cve = CVESearch()
# print(cve.search('microsoft/office'))

@app.route('/organisation')
def get_organisation():
    x.read_from_json_file("src/resources/Components.json")
    return json.dumps(x.reprJSON(), cls=ComplexEncoder)


@app.route('/user/<user_id>')
def getuser(user_id):
    app.logger.info('*****    Looking for userID (%s)  *****', user_id)
    user = x.get_user_by_id(user_id)
    if user:
        return json.dumps(user.reprJSON(), cls=ComplexEncoder), 200
    return "User Not Found", 404


@app.route('/user/<user_id>', methods=["POST"])
def set_suspicious(user_id):
    print(request.json["is_suspicious"])
    app.logger.info('*****    L (%s)  *****', request)
    user = x.get_user_by_id(user_id)
    if user:
        user.suspicious = request.json["is_suspicious"]
        x.save_organisation_to_file()
        return json.dumps(user.reprJSON(), cls=ComplexEncoder), 200
    return "User Not Found", 404


@app.route('/user/<user_id>', methods=["POST"])
def update_user(user_id):
    app.logger.info('*****    Looking for userID (%s)  *****', user_id)
    user = x.get_user_by_id(user_id)
    if user:
        return json.dumps(user.reprJSON(), cls=ComplexEncoder), 200
    return "User Not Found", 404


@app.route('/')
def not_found():
    return 'Error'


port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
