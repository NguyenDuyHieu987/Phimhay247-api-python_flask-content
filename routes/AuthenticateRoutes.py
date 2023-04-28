from flask import *


def authenticate_routes(app):
    ## Login Facebook
    from controllers.AuthenticateControllers import loginfacebook

    @app.route("/auth/loginfacebook", methods=["POST"])
    def loginfacebook_route():
        return loginfacebook()

    ## Login Google
    from controllers.AuthenticateControllers import logingoogle

    @app.route("/auth/logingoogle", methods=["POST"])
    def logingoogle_route():
        return logingoogle()

    ## Log in
    from controllers.AuthenticateControllers import login

    @app.route("/auth/login", methods=["POST"])
    def login_route():
        return login()

    ## Sigin up
    from controllers.AuthenticateControllers import signup

    @app.route("/auth/signup", methods=["POST"])
    def signup_route():
        return signup()

    ## Get user by token
    from controllers.AuthenticateControllers import getuser_by_token

    @app.route("/auth/getusertoken", methods=["POST"])
    def getuser_by_token_route():
        return getuser_by_token()
