from flask import *

# from flask_cors import cross_origin
import configs
from controllers.AccountControllers import Account


def account_routes(app):
    prefix_route = "account"

    account = Account()

    @app.route(f"/{prefix_route}/confirm/<type>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def confirm_account_route(type):
        return account.confirm(type)

    @app.route(f"/{prefix_route}/change-password", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_password_account_route():
        return account.change_password()

    @app.route(f"/{prefix_route}/change-fullname", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_full_name_account_route():
        return account.change_full_name()

    @app.route(f"/{prefix_route}/change-email", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_email_retrieve_token_account_route():
        return account.change_email_retrieve_token()

    @app.route(f"/{prefix_route}/change-email", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_email_account_route():
        return account.change_email()

    @app.route(f"/{prefix_route}/verify-email", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def verify_email_account_route():
        return account.verify_email()

    @app.route(f"/{prefix_route}/reset-password", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def reset_password_retrieve_token_account_route():
        return account.reset_password_retrieve_token()

    @app.route(f"/{prefix_route}/reset-password", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def reset_password_account_route():
        return account.reset_password()
