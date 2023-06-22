from flask import *
from flask_cors import cross_origin
import configs
from controllers.ImagesController import Images


def images_routes(app, cache):
    images = Images()

    @app.route("/images/<id>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def images_route(id):
        return images.get_images(id)
