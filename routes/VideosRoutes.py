from flask import *
from flask_cors import cross_origin
import configs
from controllers.VideosController import Videos


def videos_routes(app, cache):
    videos = Videos()

    @app.route("/videos/<id>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def videos_route(id):
        return videos.get_videos(id)
