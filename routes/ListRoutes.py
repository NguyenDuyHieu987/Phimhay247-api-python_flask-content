from flask import *
from flask_cors import cross_origin
import configs
from controllers.ListControllers import List


def list_routes(app, cache):
    list = List()
    ## Get list

    @cache.cached(timeout=3600)
    @app.route("/list/<idlist>/getlist", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getlist_route(idlist):
        return list.getlist(idlist)

    ## Search list

    @cache.cached(timeout=3600)
    @app.route("/list/<idlist>/searchlist", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_list_route(idlist):
        return list.search_list(idlist)

    ## Get item list

    @cache.cached(timeout=3600)
    @app.route("/list/<idlist>/getitem/<idmovie>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_list_route(idlist, idmovie):
        return list.getitem_list(idlist, idmovie)

    ## Add item to list

    @app.route("/list/<idlist>/add_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_list_route(idlist):
        return list.additem_list(idlist)

    ## Remove item from list

    @app.route("/list/<idlist>/remove_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_list_route(idlist):
        return list.remove_item_list(idlist)

    ## Remove all item from list

    @app.route("/list/<idlist>/removeall_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_list_route(idlist):
        return list.removeall_item_list(idlist)
