import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database
from utils.exceptions import DefaultError


class TVSeason(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def tv_seasons(self, id, season_number):
        try:
            tv = cvtJson(
                self.__db["tvs"].find_one(
                    {"id": str(id)},
                    {
                        "seasons": {
                            "$elemMatch": {"season_number": int(season_number)},
                        },
                    },
                )
            )
            if tv != None and len(tv["seasons"]) > 0:
                id_season = tv["seasons"][0]["id"]

                season = self.__db["seasons"].find_one(
                    {"id": str(id_season), "season_number": int(season_number)}
                )

                if season != None:
                    return cvtJson(season)
                else:
                    raise DefaultError("Season is not exist")
            else:
                raise DefaultError("Movie is not exist")

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
