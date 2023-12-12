from flask import *

# from flask_cors import cross_origin
import configs
from controllers.SearchControllers import Search


def search_routes(app, cache):
    search = Search()

    @app.route("/search/top-search", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def top_search_route():
        return search.top_search()

    @app.route("/search/top-search/search", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def searchin_top_search_route():
        return search.searchin_top_search()

    @app.route("/search/search-history", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_history_route_D():
        return search.search_history()

    @app.route("/search/search-history/search", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def searchin_history_route_D():
        return search.searchin_history()

    @app.route("/search/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def search_route(type):
        return search.search(type)

    @app.route("/search/add-search", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def add_search_route():
        return search.add_search()

    @app.route("/search/add-history", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def add_history_route_D():
        return search.add_history()

    @app.route("/search/remove-history", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_history_route_D():
        return search.remove_history()

    @app.route("/search/clear-history", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def clear_history_route_D():
        return search.clear_search()
