# import json
# import pathlib
# from logging.config import dictConfig
#
# from flask_cors import CORS
# from flask import Flask
# from flask.logging import default_handler
#
# from src.models.Organisation import Organisation
# from src.utils import ComplexEncoder
#
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })
#
# app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
#
# app.logger.removeHandler(default_handler)
# x = Organisation(pathlib.Path(__file__).parent / "src/resources/Components.json")
#
#
# @app.route('/organisation')
# def get_organisation():
#     x.read_from_json_file(pathlib.Path(__file__).parent / "src/resources/Components.json")
#     return json.dumps(x.reprJSON(), cls=ComplexEncoder)
#
#
# @app.route('/user/<user_id>')
# def getuser(user_id):
#     app.logger.info('*****    Looking for userID (%s)  *****', user_id)
#     user = x.get_user_by_id(user_id)
#     if user:
#         return json.dumps(user.reprJSON(), cls=ComplexEncoder), 200
#     return "User Not Found", 404
#
#
# @app.route('/user/<user_id>', methods=["POST"])
# def update_user(user_id):
#     app.logger.info('*****    Looking for userID (%s)  *****', user_id)
#     user = x.get_user_by_id(user_id)
#     if user:
#         return json.dumps(user.reprJSON(), cls=ComplexEncoder), 200
#     return "User Not Found", 404
#
#
# @app.route('/')
# def not_found():
#     return 'Error'
#
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
#     x = Organisation("src/resources/Components.json")
#
