from flask import *


def years_routes(app):
    from controllers.YearsControllers import years

    @app.route("/year/<type>", methods=["GET"])
    def years_route(type):
        return years(type)
