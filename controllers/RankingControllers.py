import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from configs.database import Database


class Rank(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def ranking(self, slug):
        try:
            if slug == "day":
                page = (request.args.get("page", default=1, type=int)) - 1
                phimbo = cvtJson(
                    self.__db["tvs"]
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
                    "total": self.__db["tvs"].count_documents({}),
                }
            elif slug == "week":
                page = request.args.get("page", default=1, type=int)
                nowplaying = cvtJson(
                    self.__db["tvairingtodays"].find_one({"page": page})
                )
                return {
                    "page": page,
                    "results": nowplaying["results"],
                    "total_pages": nowplaying["total_pages"],
                }
            elif slug == "month":
                page = request.args.get("page", default=1, type=int)
                upcoming = cvtJson(self.__db["tvontheairs"].find_one({"page": page}))
                return {
                    "page": page,
                    "results": upcoming["results"],
                    "total_pages": upcoming["total_pages"],
                }
            elif slug == "all":
                page = request.args.get("page", default=1, type=int)
                popular = cvtJson(self.__db["tvpopulars"].find_one({"page": page}))
                return {
                    "page": page,
                    "results": popular["results"],
                    "total_pages": popular["total_pages"],
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
