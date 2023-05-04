import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from configs.database import ConnectMongoDB

db = ConnectMongoDB()

# myclient = pymongo.MongoClient(
#     "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
# )

# db = myclient["Phimhay247_DB"]


def sortby(type):
    try:
        if type == "all":
            all_sortbys = cvtJson(db["sortbys"].find())
            return all_sortbys
        else:
            return errorMessage(400)
    except:
        return []
