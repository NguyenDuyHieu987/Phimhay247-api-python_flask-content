import os

JWT_EXP_OFFSET = int(os.getenv("JWT_EXP_OFFSET"))
OTP_EXP_OFFSET = int(os.getenv("OTP_EXP_OFFSET"))
FORGOT_PASSWORD_EXP_OFFSET = int(os.getenv("FORGOT_PASSWORD_EXP_OFFSET"))
CHANGE_EMAIL_EXP_OFFSET = int(os.getenv("CHANGE_EMAIL_EXP_OFFSET"))


API_MORMAL_ORIGINS_CONFIG = [
    "http://localhost:3000",
    "https://phimhay247z.org",
    # www
    "https://www.phimhay247z.org",
]


API_ADMIN_ORIGINS_CONFIG = [
    "http://localhost:8080",
    "https://dash.phimhay247z.org",
    "https://dashboard.phimhay247z.org",
]

ALL_ORIGINS_CONFIG = API_MORMAL_ORIGINS_CONFIG + API_ADMIN_ORIGINS_CONFIG
