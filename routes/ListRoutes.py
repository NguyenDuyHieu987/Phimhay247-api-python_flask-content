from flask import *
from flask_cors import cross_origin
import configs
from controllers.ListControllers import List


def list_routes(app, cache):
    list = List()
    ## Get list

    @app.route("/list/get/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getlist_route(type):
        return list.getlist(type)

    ## Search list

    @app.route("/list/search/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_list_route(type):
        return list.search_list(type)

    ## Get item list

    @app.route("/list/getitem/<type>/<movieId>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_list_route(type, movieId):
        return list.getitem_list(type, movieId)

    ## Add item to list

    @app.route("/list/additem", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_list_route():
        return list.additem_list()

    ## Remove item from list

    @app.route("/list/removeitem", methods=["DELETE"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_list_route():
        return list.remove_item_list()

    ## Remove all item from list

    @app.route("/list/removeallitem", methods=["DELETE"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_list_route():
        return list.removeall_item_list()
