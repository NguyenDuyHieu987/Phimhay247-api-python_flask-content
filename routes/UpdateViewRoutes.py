from flask import *
# from flask_cors import cross_origin
import configs
from controllers.UpdateViewContronllers import View


def update_view_routes(app):
    view = View()

    @app.route("/update-view/<type>/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def update_view_routes(type, id):
        return view.update_view(type, id)
