from flask import *

# from flask_cors import cross_origin
import configs
from controllers.CommentControlers import Comment


def comment_routes(app):
    prefix_route = "comment"

    comment = Comment()

    @app.route(f"/{prefix_route}/get-all/<movieType>/<movieId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_all_parent_comment_route(movieType, movieId):
        return comment.get_all_parent(movieType, movieId)

    @app.route(f"/{prefix_route}/get/<movieType>/<movieId>/<parentId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_child_comment_route(movieType, movieId, parentId):
        return comment.get_child(movieType, movieId, parentId)

    @app.route(f"/{prefix_route}/post/<movieType>/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def post_comment_route(movieType, id):
        return comment.post(movieType, id)

    @app.route(f"/{prefix_route}/edit/<movieType>/<id>", methods=["PUT"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def edit_comment_route(movieType, id):
        return comment.edit(movieType, id)

    @app.route(f"/{prefix_route}/delete/<movieType>/<id>", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def delete_comment_route(movieType, id):
        return comment.delete(movieType, id)

    @app.route(f"/{prefix_route}/like/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def like_comment_route(id):
        return comment.like(id)

    @app.route(f"/{prefix_route}/dislike/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def dislike_comment_route(id):
        return comment.dislike(id)

    @app.route(f"/{prefix_route}/check-like-dislike/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def check_like_dislike_comment_route(id):
        return comment.check_like_dislike(id)
