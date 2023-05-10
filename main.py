from flask import *
from flask_cors import CORS
from flask_caching import Cache

# from flask_restful import Api

# from waitress import serve
from gevent.pywsgi import WSGIServer
import sys
from dotenv import load_dotenv

load_dotenv()


sys.path.insert(0, "/Python/Phimhay247-api-python_flask-content")
sys.path.insert(0, "/mnt/d/Python/Phimhay247-api-python_flask-content")
# print(sys.path)

app = Flask(__name__)
# CORS(app)

cache = Cache(
    app,
    # config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": "redis://localhost:6379/0"},
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": "0.0.0.0",
        "CACHE_REDIS_PORT": 6379,
    },
)

cache.init_app(app)


# route app
from routes import route

route(app, cache)

if __name__ == "__main__":
    # app.run(debug=True, port=5000, use_reloader=True)

    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
