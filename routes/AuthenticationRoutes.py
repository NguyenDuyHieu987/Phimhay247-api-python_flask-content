from flask import *

# from flask_cors import cross_origin
import configs
from controllers.AuthenticationControllers import Authentication


def authentication_routes(app):
    authentication = Authentication()
    ## Log in

    @app.route("/auth/login", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def login_route():
        return authentication.login()

    ## Login Facebook

    @app.route("/auth/login-facebook", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def loginfacebook_route():
        return authentication.loginfacebook()

    ## Login Google

    @app.route("/auth/login-google", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def logingoogle_route():
        return authentication.logingoogle()

    ## Get user by token

    @app.route("/auth/getuser", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getuser_by_token_route():
        return authentication.getuser_by_token()

    ## Sign up

    @app.route("/auth/signup", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def signup_route():
        return authentication.signup()

    ## Verify Sign up

    @app.route("/auth/verify-signup/<type>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def verify_signup_route(type):
        return authentication.signup_verify(type)

    ## Forgot Password

    @app.route("/auth/forgot-password/<type>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def forgot_password_route(type):
        return authentication.forgot_password(type)

    ## Log out

    @app.route("/auth/logout", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def logout_route():
        return authentication.logout()
