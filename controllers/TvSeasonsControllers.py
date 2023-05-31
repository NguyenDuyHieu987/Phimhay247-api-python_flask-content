import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database


class TVSeason(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def tv_seasons(self, id, season_number):
        try:
            tv = cvtJson(
                self.__db["tvs"].find_one(
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
                self.__db["seasons"].find_one(
                    {"id": int(id_season), "season_number": int(season_number)}
                )
            )
            return season
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
