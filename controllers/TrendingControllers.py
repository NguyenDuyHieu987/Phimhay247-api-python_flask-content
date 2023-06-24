from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database
from werkzeug.exceptions import HTTPException


class Trend(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def trending(self, type):
        try:
            if type == "all":
                page = request.args.get("page", default=1, type=int) - 1
                limit = request.args.get("limit", default=20, type=int)

                trending = (
                    self.__db["trendings"].find({}).skip(page * limit).limit(limit)
                )

                return make_response(
                    {
                        "page": page + 1,
                        "results": cvtJson(trending),
                        "total": self.__db["trendings"].count_documents({}),
                        "page_size": 20,
                    }
                )
            else:
                raise NotInTypeError("trending", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
