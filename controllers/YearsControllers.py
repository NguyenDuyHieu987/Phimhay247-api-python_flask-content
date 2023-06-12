import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Year(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def years(self, type):
        try:
            if type == "all":
                years = cvtJson(self.__db["years"].find())
                return {"result": years}
            else:
                raise NotInTypeError("country", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
