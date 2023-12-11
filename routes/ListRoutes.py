from flask import *

# from flask_cors import cross_origin
import configs
from controllers.ListControllers import List


def list_routes(app, cache):
    list = List()
    ## Get list

    @app.route("/list/get-all/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getall_list_route(type):
        return list.getall_list(type)

    ## Search list

    @app.route("/list/search/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_list_route(type):
        return list.search_list(type)

    ## Get item list

    @app.route("/list/get/<type>/<movieId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_list_route(type, movieId):
        return list.get_list(type, movieId)

    ## Add item to list

    @app.route("/list/add", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def add_list_route():
        return list.add_list()

    ## Remove item from list

    @app.route("/list/remove", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_list_route():
        return list.remove_list()

    ## Remove all item from list

    @app.route("/list/clear", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def clear_list_route():
        return list.clear_list()
