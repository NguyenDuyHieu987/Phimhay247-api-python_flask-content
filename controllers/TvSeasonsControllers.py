import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def tv_seasons(id, season_number):
    # try:
    tv = cvtJson(
        db["tvs"].find_one(
            {"id": int(id)},
            {
                "seasons": {
                    "$elemMatch": {"season_number": int(season_number)},
                },
            },
        )
    )
    id_season = tv["seasons"][0]["id"]

    season = cvtJson(
        db["seasons"].find_one(
            {"id": int(id_season), "season_number": int(season_number)}
        )
    )
    return season


# except:
#     return {
#         "results": [],
#         "total_pages": 0,
#     }
# finally:
#     return errorMessage(400)
