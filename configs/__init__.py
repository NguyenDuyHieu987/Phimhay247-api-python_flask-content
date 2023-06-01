import os

TIME_OFFSET = int(os.getenv("TIME_OFFSET")) * 60 * 60

API_MORMAL_ORIGINS_CONFIG = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:3000",
    "https://phimhay247.site",
    "https://phimhay247.tech",
    # www
    "https://www.phimhay247.site",
    "https://www.phimhay247.tech",
    
    #test
    "https://famous-entremet-57ab43.netlify.app",
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
