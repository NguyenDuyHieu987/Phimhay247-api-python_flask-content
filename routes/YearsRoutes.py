from flask import *
from flask_cors import cross_origin
import configs


def years_routes(app):
    from controllers.YearsControllers import years

    @app.route("/year/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def years_route(type):
        return years(type)
