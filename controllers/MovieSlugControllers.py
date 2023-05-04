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


def movie_slug(slug):
    try:
        if slug == "phimle":
            page = (request.args.get("page", default=1, type=int)) - 1

            phimle = cvtJson(
                db["movies"]
                .find(
                    {},
                    {
                        "images": 0,
                        "credits": 0,
                        "videos": 0,
                        "production_companies": 0,
                    },
                )
                .skip(page * 20)
                .limit(20)
            )

            return {
                "page": page + 1,
                "results": phimle,
                "total": db["movies"].count_documents({}),
            }
        elif slug == "nowplaying":
            page = request.args.get("page", default=1, type=int)
            nowplaying = cvtJson(db["nowplayings"].find_one({"page": page}))
            return {
                "page": page,
                "results": nowplaying["results"],
                "total_pages": nowplaying["total_pages"],
            }
        elif slug == "upcoming":
            page = request.args.get("page", default=1, type=int)
            upcoming = cvtJson(db["upcomings"].find_one({"page": page}))
            return {
                "page": page,
                "results": upcoming["results"],
                "total_pages": upcoming["total_pages"],
            }
        elif slug == "popular":
            page = request.args.get("page", default=1, type=int)
            popular = cvtJson(db["populars"].find_one({"page": page}))
            return {
                "page": page,
                "results": popular["results"],
                "total_pages": popular["total_pages"],
            }
        elif slug == "toprated":
            page = request.args.get("page", default=1, type=int)
            toprated = cvtJson(db["toprateds"].find_one({"page": page}))
            return {
                "page": page,
                "results": toprated["results"],
                "total_pages": toprated["total_pages"],
            }
        else:
            return errorMessage(400)
    except:
        return {
            "results": [],
            "total_pages": 0,
        }
    # finally:
    #     return errorMessage(400)
