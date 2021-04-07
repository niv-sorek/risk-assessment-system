from flask import Flask
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
def update_user(user_id):
    app.logger.info('*****    Looking for userID (%s)  *****', user_id)
    user = x.get_user_by_id(user_id)
    if user:
        return json.dumps(user.reprJSON(), cls=ComplexEncoder), 200
    return "User Not Found", 404


@app.route('/')
def not_found():
    return 'Error'


if __name__ == "__main__":
    app.run(debug=True, port=5000)
