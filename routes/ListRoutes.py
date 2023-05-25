from flask import *
from flask_cors import cross_origin
import configs
from controllers.ListControllers import List


def list_routes(app, cache):
    list = List()
    ## Get list

    @app.route("/list/getlist", methods=["GET"])
    @cache.cached(timeout=3600)
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getlist_route():
        return list.getlist()

    ## Search list

    @app.route("/list/searchlist", methods=["GET"])
    @cache.cached(timeout=3600)
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_list_route():
        return list.search_list()

    ## Get item list

    @app.route("/list/getitem/<idmovie>", methods=["GET"])
    @cache.cached(timeout=3600)
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_list_route(idmovie):
        return list.getitem_list(idmovie)

    ## Add item to list

    @app.route("/list/add_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_list_route():
        return list.additem_list()

    ## Remove item from list

    @app.route("/list/remove_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_list_route():
        return list.remove_item_list()

    ## Remove all item from list

    @app.route("/list/removeall_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_list_route():
        return list.removeall_item_list()
