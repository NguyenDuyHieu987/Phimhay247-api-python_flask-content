from flask_cors import CORS

api_normal_cors_config1 = {
    "allow_headers": "*",
    "origins": [
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
        "https://phimhay247.site",
        "https://phimhay247.tech",
        "https://dashboard.phimhay247.site",
        "https://dashboard.phimhay247.tech",
        "https://dash.phimhay247.site",
        "https://dash.phimhay247.tech",
        # www
        "https://www.phimhay247.site",
        "https://www.phimhay247.tech",
        "https://www.dashboard.phimhay247.site",
        "https://www.dashboard.phimhay247.tech",
        "https://www.dash.phimhay247.site",
        "https://www.dash.phimhay247.tech",
    ],
    "methods": ["GET"],
}

api_normal_cors_config2 = {
    "allow_headers": "*",
    "origins": [
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
        "https://phimhay247.site",
        "https://phimhay247.tech",
        "https://dashboard.phimhay247.site",
        "https://dashboard.phimhay247.tech",
        "https://dash.phimhay247.site",
        "https://dash.phimhay247.tech",
        # www
        "https://www.phimhay247.site",
        "https://www.phimhay247.tech",
        "https://www.dashboard.phimhay247.site",
        "https://www.dashboard.phimhay247.tech",
        "https://www.dash.phimhay247.site",
        "https://www.dash.phimhay247.tech",
    ],
    "methods": ["GET", "POST"],
}


api_admin_cors_config = {
    "allow_headers": "*",
    "origins": [
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
        "https://dashboard.phimhay247.site",
        "https://dashboard.phimhay247.tech",
        "https://dash.phimhay247.site",
        "https://dash.phimhay247.tech",
        # www
        "https://www.dashboard.phimhay247.site",
        "https://www.dashboard.phimhay247.tech",
        "https://www.dash.phimhay247.site",
        "https://www.dash.phimhay247.tech",
    ],
    "methods": ["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
}


def cors_app(app):
    CORS(
        app
        # resources={
        #     r"/auth/*": api_normal_cors_config2,
        #     r"/trending/*": api_normal_cors_config1,
        #     r"/recommend/*": api_normal_cors_config1,
        #     r"/search/*": api_normal_cors_config1,
        #     r"/movie/*": api_normal_cors_config2,
        #     r"/tv/*": api_normal_cors_config2,
        #     r"/discover/*": api_normal_cors_config1,
        #     r"/similar/*": api_normal_cors_config1,
        #     r"/country/*": api_normal_cors_config1,
        #     r"/genre/*": api_normal_cors_config1,
        #     r"/year/*": api_normal_cors_config1,
        #     r"/sortby/*": api_normal_cors_config1,
        #     r"/ranking/*": api_normal_cors_config1,
        #     r"/list/*": api_normal_cors_config2,
        #     r"/history/*": api_normal_cors_config2,
        #     r"/rating/*": api_normal_cors_config2,
        #     # r"/*": api_admin_cors_config,
        # },
    )
