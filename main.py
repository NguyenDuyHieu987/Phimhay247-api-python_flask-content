from flask import *
from flask_cors import CORS
from flask_caching import Cache
import os

# from flask_restful import Api
# from waitress import serve
from gevent.pywsgi import WSGIServer
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, "/Python/The-Movie-Flask-Api")
sys.path.insert(0, "/mnt/d/Python/The-Movie-Flask-Api")


app = Flask(__name__)

import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

CORS(
    app,
    # resources={
    #     r"/*": {
    #         "origins": [
    #             "http://localhost:3000",
    #             "http://localhost:8080",
    #             "https://phimhay247z.org",
    #             "https://dash.phimhay247z.org",
    #             "https://dashboard.phimhay247z.org",
    #             # www
    #             "https://www.phimhay247z.org",
    #         ],
    #     }
    # },
    origins=[
        "https://phimhay247z.org",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://dash.phimhay247z.org",
        "https://dashboard.phimhay247z.org",
        # www
        "https://www.phimhay247z.org",
    ],
    supports_credentials=True,
)

cache = Cache(
    app,
    # config={
    #     "CACHE_TYPE": "RedisCache",
    #     "CACHE_REDIS_URL": os.getenv("REDIS_URL"),
    #     "CACHE_DEFAULT_TIMEOUT": 300,
    # },
    config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": os.getenv("REDIS_URL"),
        "CACHE_REDIS_HOST": os.getenv("REDIS_HOST"),
        "CACHE_REDIS_PORT": os.getenv("REDIS_PORT"),
        "CACHE_REDIS_PASSWORD": os.getenv("REDIS_PASSWORD"),
        "CACHE_DEFAULT_TIMEOUT": int(os.getenv("REDIS_CACHE_TIME")),
    },
)

cache.init_app(app)

# route app
from routes import route

route(app, cache)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", debug=True, port=5000, use_reloader=True)

    http_server = WSGIServer(("", 5001), app, log=None)
    http_server.serve_forever()
