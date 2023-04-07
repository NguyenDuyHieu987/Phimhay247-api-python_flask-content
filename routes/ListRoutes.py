from flask import *


def list_routes(app):
    ## Get list
    from controllers.ListControllers import getlist

    @app.route("/list/<idlist>/getlist", methods=["GET"])
    def getlist_route(idlist):
        return getlist(idlist)

    ## Search list
    from controllers.ListControllers import search_list

    @app.route("/list/<idlist>/searchlist", methods=["GET"])
    def search_list_route(idlist):
        return search_list(idlist)

    ## Get item list
    from controllers.ListControllers import getitem_list

    @app.route("/list/<idlist>/getitem/<idmovie>", methods=["GET"])
    def getitem_list_route(idlist, idmovie):
        return getitem_list(idlist, idmovie)

    ## Add item to list
    from controllers.ListControllers import additem_list

    @app.route("/list/<idlist>/add_item", methods=["POST"])
    def additem_list_route(idlist):
        return additem_list(idlist)

    ## Remove item from list
    from controllers.ListControllers import remove_item_list

    @app.route("/list/<idlist>/remove_item", methods=["POST"])
    def remove_item_list_route(idlist):
        return remove_item_list(idlist)

    ## Remove all item from list
    from controllers.ListControllers import removeall_item_list

    @app.route("/list/<idlist>/removeall_item", methods=["POST"])
    def removeall_item_list_route(idlist):
        return removeall_item_list(idlist)
