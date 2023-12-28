from flask import *

# from flask_cors import cross_origin
import configs
from controllers.ListControllers import List


def list_routes(app, cache):
    prefix_route = "list"

    list = List()

    ## Get list

    @app.route(f"/{prefix_route}/get-all/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getall_list_route(type):
        return list.get_all(type)

    ## Search list

    @app.route(f"/{prefix_route}/search/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_list_route(type):
        return list.search(type)

    ## Get item list

    @app.route(f"/{prefix_route}/get/<type>/<movieId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_list_route(type, movieId):
        return list.get(type, movieId)

    ## Add item to list

    @app.route(f"/{prefix_route}/add", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def add_list_route():
        return list.add()

    ## Remove item from list

    @app.route(f"/{prefix_route}/remove", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_list_route():
        return list.remove()

    ## Remove all item from list

    @app.route(f"/{prefix_route}/clear", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def clear_list_route():
        return list.clear()
