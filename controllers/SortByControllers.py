from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Sortby(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def sortby(self, type):
        try:
            if type == "all":
                all_sortbys = cvtJson(self.__db["sortbys"].find())
                return {"result": all_sortbys}
            else:
                raise NotInTypeError("country", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
