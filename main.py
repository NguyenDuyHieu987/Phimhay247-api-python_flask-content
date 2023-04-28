from flask import *
from flask_cors import CORS, cross_origin
from waitress import serve
from gevent.pywsgi import WSGIServer
from bson import json_util, ObjectId
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, "D:\Python\Phimhay247-api-python_flask-content")

app = Flask(__name__)
# CORS(app)

api_normal_cors_config1 = {
    "allow_headers": "*",
    "origins": [
        "http://localhost:8080",
        "http://localhost:3000",
        "https://phimhay247.site",
        "https://phimhay247.tech",
    ],
    "methods": ["GET"],
}

api_normal_cors_config2 = {
    "allow_headers": "*",
    "origins": [
        "http://localhost:8080",
        "http://localhost:3000",
        "https://phimhay247.site",
        "https://phimhay247.tech",
    ],
    "methods": ["GET", "POST"],
}


api_admin_cors_config = {
    "allow_headers": "*",
    "origins": [
        "http://localhost:8080/dashboard",
        "http://localhost:3000/dashboard",
        "https://phimhay247.site/dashboard",
        "https://phimhay247.tech/dashboard",
    ],
    "methods": ["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
}

CORS(
    app,
    resources={
        r"/auth/*": api_normal_cors_config2,
        r"/trending/*": api_normal_cors_config1,
        r"/recommend/*": api_normal_cors_config1,
        r"/search/*": api_normal_cors_config1,
        r"/movie/*": api_normal_cors_config2,
        r"/tv/*": api_normal_cors_config2,
        r"/discover/*": api_normal_cors_config1,
        r"/similar/*": api_normal_cors_config1,
        r"/country/*": api_normal_cors_config1,
        r"/genre/*": api_normal_cors_config1,
        r"/year/*": api_normal_cors_config1,
        r"/sortby/*": api_normal_cors_config1,
        r"/ranking/*": api_normal_cors_config1,
        r"/list/*": api_normal_cors_config2,
        r"/history/*": api_normal_cors_config2,
        r"/rating/*": api_normal_cors_config2,
        r"/*": api_admin_cors_config,
    },
)


# route app
from Routes import route

route(app)

if __name__ == "__main__":
    # app.run(debug=True, port=5000, use_reloader=True)

    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
