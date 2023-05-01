import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def tv_slug(slug):
    try:
        if slug == "phimbo":
            page = (request.args.get("page", default=1, type=int)) - 1
            phimbo = cvtJson(
                db["tvs"]
                .find(
                    {},
                    {
                        "images": 0,
                        "credits": 0,
                        "videos": 0,
                        "production_companies": 0,
                        "seasons": 0,
                    },
                )
                .skip(page * 20)
                .limit(20)
            )

            return {
                "page": page + 1,
                "results": phimbo,
                "total": db["tvs"].count_documents({}),
            }
        elif slug == "airingtoday":
            page = request.args.get("page", default=1, type=int)
            nowplaying = cvtJson(db["tvairingtodays"].find_one({"page": page}))
            return {
                "page": page,
                "results": nowplaying["results"],
                "total_pages": nowplaying["total_pages"],
            }
        elif slug == "ontheair":
            page = request.args.get("page", default=1, type=int)
            upcoming = cvtJson(db["tvontheairs"].find_one({"page": page}))
            return {
                "page": page,
                "results": upcoming["results"],
                "total_pages": upcoming["total_pages"],
            }
        elif slug == "popular":
            page = request.args.get("page", default=1, type=int)
            popular = cvtJson(db["tvpopulars"].find_one({"page": page}))
            return {
                "page": page,
                "results": popular["results"],
                "total_pages": popular["total_pages"],
            }
        elif slug == "toprated":
            page = request.args.get("page", default=1, type=int)
            toprated = cvtJson(db["tvtoprateds"].find_one({"page": page}))
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
