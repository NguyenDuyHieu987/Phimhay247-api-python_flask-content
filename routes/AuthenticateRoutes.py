from flask import *
from flask_cors import cross_origin
import configs


def authenticate_routes(app):
    ## Login Facebook
    from controllers.AuthenticateControllers import loginfacebook

    @app.route("/auth/loginfacebook", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def loginfacebook_route():
        return loginfacebook()

    ## Login Google
    from controllers.AuthenticateControllers import logingoogle

    @app.route("/auth/logingoogle", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def logingoogle_route():
        return logingoogle()

    ## Log in
    from controllers.AuthenticateControllers import login

    @app.route("/auth/login", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def login_route():
        return login()

    ## Sigin up
    from controllers.AuthenticateControllers import signup

    @app.route("/auth/signup", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def signup_route():
        return signup()

    ## Get user by token
    from controllers.AuthenticateControllers import getuser_by_token

    @app.route("/auth/getusertoken", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getuser_by_token_route():
        return getuser_by_token()
