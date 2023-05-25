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


sys.path.insert(0, "/Python/Phimhay247-api-python_flask-content")
sys.path.insert(0, "/mnt/d/Python/Phimhay247-api-python_flask-content")

app = Flask(__name__)
# CORS(app)

cache = Cache(
    app,
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_URL": os.getenv("REDIS_URL"),
        "CACHE_DEFAULT_TIMEOUT": 300,
    },
    # config={
    #     "CACHE_TYPE": "redis",
    #     "CACHE_REDIS_HOST": os.getenv("REDIS_HOST"),
    #     "CACHE_REDIS_PORT": os.getenv("REDIS_PORT"),
    #     "CACHE_DEFAULT_TIMEOUT": 300
    # },
)

cache.init_app(app)


# route app
from routes import route

route(app, cache)

if __name__ == "__main__":
    # app.run(debug=True, port=5000, use_reloader=True)

    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
