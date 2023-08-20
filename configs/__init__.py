import os

JWT_EXP_OFFSET = int(os.getenv("JWT_EXP_OFFSET")) * 60 * 60
OTP_EXP_OFFSET = int(os.getenv("OTP_EXP_OFFSET")) * 60
FORGOT_PASSWORD_EXP_OFFSET = int(os.getenv("FORGOT_PASSWORD_EXP_OFFSET")) * 60


API_MORMAL_ORIGINS_CONFIG = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:3000",
    "https://phimhay247.site",
    "https://phimhay247.tech",
    # www
    "https://www.phimhay247.site",
    "https://www.phimhay247.tech",
    "https://phimhay247-static-site.pages.dev",
]


API_ADMIN_ORIGINS_CONFIG = [
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
]

ALL_ORIGINS_CONFIG = API_MORMAL_ORIGINS_CONFIG + API_ADMIN_ORIGINS_CONFIG
