from flask import *

# from flask_cors import cross_origin
import configs
from controllers.VideosController import Videos


def videos_routes(app, cache):
    prefix_route = "videos"

    videos = Videos()

    @app.route(f"/{prefix_route}/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_videos_route(id):
        return videos.get(id)
