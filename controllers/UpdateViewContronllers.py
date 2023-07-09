import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from pymongo import ReturnDocument
from configs.database import Database


class View(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def update_view(self, type, id):
        try:
            if type == "movie":
                self.__db["movies"].update_one(
                    {"id": str(id)},
                    {
                        "$inc": {"views": 1},
                    },
                )

                return {
                    "success": True,
                    "result": "Update views of movie successfully",
                }
            elif type == "tv":
                self.__db["tvs"].update_one(
                    {"id": str(id)},
                    {
                        "$inc": {"views": 1},
                    },
                )
                return {"success": True, "result": "Update views of tv successfully"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
