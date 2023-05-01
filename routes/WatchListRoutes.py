from flask import *
from flask_cors import cross_origin
import configs


def watchlist_routes(app):
    ## Get history
    from controllers.WatchListControllers import getwatchlist

    @app.route("/history/<idwatchlist>/gethistory", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getwatchlist_route(idwatchlist):
        return getwatchlist(idwatchlist)

    ## Search history
    from controllers.WatchListControllers import search_watchlist

    @app.route("/history/<idwatchlist>/searchhistory", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_watchlist_route(idwatchlist):
        return search_watchlist(idwatchlist)

    ## Get item history
    from controllers.WatchListControllers import getitem_watchlist

    @app.route("/history/<idwatchlist>/getitem/<idmovie>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_watchlist_route(idwatchlist, idmovie):
        return getitem_watchlist(idwatchlist, idmovie)

    ## Add item to history
    from controllers.WatchListControllers import additem_watchlist

    @app.route("/history/<idwatchlist>/add_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_watchlist_route(idwatchlist):
        return additem_watchlist(idwatchlist)

    ## Remove item from history
    from controllers.WatchListControllers import remove_item_watchlist

    @app.route("/history/<idwatchlist>/remove_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_watchlist_route(idwatchlist):
        return remove_item_watchlist(idwatchlist)

    ## Remove all item from history
    from controllers.WatchListControllers import removeall_item_watchlist

    @app.route("/history/<idwatchlist>/removeall_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_watchlist_route(idwatchlist):
        return removeall_item_watchlist(idwatchlist)
