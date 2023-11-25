from flask import *
from werkzeug import exceptions


def error_handler(app):
    @app.errorhandler(exceptions.BadRequest)
    def handle_bad_request(err):
        return make_response(err, 400)

    app.register_error_handler(400, handle_bad_request)

    @app.errorhandler(exceptions.InternalServerError)
    def handle_error_internal_server_error(err):
        return make_response(err, 500)

    app.register_error_handler(500, handle_error_internal_server_error)
