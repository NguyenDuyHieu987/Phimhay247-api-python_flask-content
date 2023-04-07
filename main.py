from flask import *
from flask_cors import CORS, cross_origin
from waitress import serve
from gevent.pywsgi import WSGIServer
from bson import json_util, ObjectId
import sys

sys.path.insert(0, "D:\Python\Phimhay247-api-python_flask-content")

app = Flask(__name__)
# CORS(app)

api_v1_cors_config = {
    "allow_headers": "*",
    "origins": "*",
    "methods": ["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
}

CORS(app, resources={r"/*": api_v1_cors_config})


# route app
from Routes import route

route(app)

if __name__ == "__main__":
    # app.run(debug=True, port=5000, use_reloader=True)
    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
