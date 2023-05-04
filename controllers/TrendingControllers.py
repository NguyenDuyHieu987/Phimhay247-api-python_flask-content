import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument
from configs.database import ConnectMongoDB

db = ConnectMongoDB()

# myclient = pymongo.MongoClient(
#     "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
# )

# db = myclient["Phimhay247_DB"]


def trending(type):
    try:
        if type == "all":
            page = request.args.get("page", default=1, type=int)
            trending = cvtJson(db["trendings"].find_one({"page": page}))
            return {
                "page": page,
                "results": trending["results"],
                "total_pages": trending["total_pages"],
            }
        else:
            return errorMessage(400)
    except:
        return {"results": [], "total_pages": 0}
