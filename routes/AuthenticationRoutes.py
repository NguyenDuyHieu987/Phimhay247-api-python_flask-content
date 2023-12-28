from flask import *

from flask_cors import cross_origin
import configs
from controllers.AuthenticationControllers import Authentication


def authentication_routes(app):
    prefix_route = "auth"

    authentication = Authentication()

    ## Log in

    @app.route(f"/{prefix_route}/login", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def login_authentication_route():
        return authentication.login()

    ## Login Facebook

    @app.route(f"/{prefix_route}/login-facebook", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def loginfacebook_authentication_route():
        return authentication.loginfacebook()

    ## Login Google

    @app.route(f"/{prefix_route}/login-google", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def logingoogle_authentication_route():
        return authentication.logingoogle()

    ## Get user by token

    @app.route(f"/{prefix_route}/getuser", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getuser_by_token_authentication_route():
        return authentication.getuser_by_token()

    ## Sign up

    @app.route(f"/{prefix_route}/signup", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def signup_authentication_route():
        return authentication.signup()

    ## Verify Sign up

    @app.route(f"/{prefix_route}/verify-signup/<type>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def verify_signup_authentication_route(type):
        return authentication.signup_verify(type)

    ## Log out

    @app.route(f"/{prefix_route}/logout", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def logout_authentication_route():
        return authentication.logout()

    ## Forgot Password

    @app.route(f"/{prefix_route}/forgot-password/<type>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def forgot_password_authentication_route(type):
        return authentication.forgot_password(type)
