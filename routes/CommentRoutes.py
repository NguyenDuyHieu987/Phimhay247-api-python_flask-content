from flask import *
from flask_cors import cross_origin
import configs
from controllers.CommentControlers import Comment


def comment_routes(app):
    comment = Comment()

    @app.route("/comment/<movieId>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_comment_by_movieid_route(movieId):
        return comment.get_commemt_by_movieid(movieId)

    @app.route("/comment/<movieId>/<parentId>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_comment_by_movieid_parentid_route(movieId, parentId):
        return comment.get_commemt_by_movieid_parentid(movieId, parentId)

    @app.route("/comment/<type>/<id>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def comment_route(type, id):
        return comment.post_comment(type, id)
