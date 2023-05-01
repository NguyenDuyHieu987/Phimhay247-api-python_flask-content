from flask import *
from flask_cors import CORS

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


# route app
from Routes import route

route(app)

if __name__ == "__main__":
    # app.run(debug=True, port=5000, use_reloader=True)

    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
