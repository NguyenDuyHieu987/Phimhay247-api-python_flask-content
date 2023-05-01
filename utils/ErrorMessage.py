def errorMessage(status_code):
    listError = {
        400: {
            "status_code": 400,
            "status_message": "The resource you requested could not be found.",
            "success": False,
        }
    }
    return listError[status_code]
