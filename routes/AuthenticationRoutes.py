from flask import *
from flask_cors import cross_origin
import configs
from controllers.AuthenticationControllers import Authentication


def authentication_routes(app):
    authentication = Authentication()
    ## Login Facebook

    @app.route("/auth/loginfacebook", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def loginfacebook_route():
        return authentication.loginfacebook()

    ## Login Google

    @app.route("/auth/logingoogle", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def logingoogle_route():
        return authentication.logingoogle()

    ## Log in

    @app.route("/auth/login", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def login_route():
        return authentication.login()

    ## Get user by token

    @app.route("/auth/getusertoken", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getuser_by_token_route():
        return authentication.getuser_by_token()

    ## Sign up

    @app.route("/auth/signup", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def signup_route():
        return authentication.signup()

    ## Verify Email by token

    @app.route("/auth/verify/email", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def auth_verify_email_route():
        return authentication.verify_email()
