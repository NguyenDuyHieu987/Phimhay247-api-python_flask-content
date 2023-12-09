from flask import *

# from flask_cors import cross_origin
import configs
from controllers.CommentControlers import Comment


def comment_routes(app):
    comment = Comment()

    @app.route("/comment/get-all/<movieType>/<movieId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_comment_parent_route(movieType, movieId):
        return comment.get_parent(movieType, movieId)

    @app.route("/comment/get/<movieType>/<movieId>/<parentId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_comment_child_route(movieType, movieId, parentId):
        return comment.get_child(movieType, movieId, parentId)

    @app.route("/comment/post/<movieType>/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def comment_route(movieType, id):
        return comment.post_comment(movieType, id)

    @app.route("/comment/edit/<movieType>/<id>", methods=["PUT"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def edit_comment_route(movieType, id):
        return comment.edit_comment(movieType, id)

    @app.route("/comment/delete/<movieType>/<id>", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def delete_comment_route(movieType, id):
        return comment.delete_comment(movieType, id)

    @app.route("/comment/like/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def like_comment_route(id):
        return comment.like(id)

    @app.route("/comment/dislike/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def dislike_comment_route(id):
        return comment.dislike(id)

    @app.route("/comment/check-like-dislike/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def check_like_dislike_comment_route(id):
        return comment.check_like_dislike(id)
