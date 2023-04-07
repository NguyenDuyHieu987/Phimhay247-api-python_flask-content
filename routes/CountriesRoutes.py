from flask import *


def countries_routes(app):
    from controllers.CountriesControllers import countries

    @app.route("/country/<type>", methods=["GET"])
    def countries_route(type):
        return countries(type)
