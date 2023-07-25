import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database


class Plan(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def plans(self):
        try:
            plans = cvtJson(
                self.__db["plans"].find().sort([("order", pymongo.ASCENDING)])
            )
            return {"results": plans}

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
