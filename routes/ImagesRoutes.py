from flask import *

# from flask_cors import cross_origin
import configs
from controllers.ImagesController import Images


def images_routes(app, cache):
    prefix_route = "images"

    images = Images()

    @app.route(f"/{prefix_route}/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_images_route(id):
        return images.get(id)
