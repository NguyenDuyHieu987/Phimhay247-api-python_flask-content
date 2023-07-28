import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import DefaultError
from flask import *
from pymongo import ReturnDocument
from datetime import datetime
from configs.database import Database
import os
import jwt
import uuid


class List(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def getlist(self, type):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            skip = request.args.get("skip", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            if type == "all":
                list = (
                    self.__db["lists"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                        }
                    )
                    .skip(skip * limit)
                    .limit(limit)
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                total = self.__db["lists"].count_documents(
                    {
                        "user_id": jwtUser["id"],
                    }
                )

                return {
                    "results": cvtJson(list) if list != None else [],
                    "total": total,
                }

            elif type == "movie":
                list = (
                    self.__db["lists"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                            "media_type": type,
                        },
                    )
                    .skip(skip * limit)
                    .limit(limit)
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                total = self.__db["lists"].count_documents(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                    },
                )

                return {
                    "results": cvtJson(list) if list != None else [],
                    "total": total,
                }

            elif type == "tv":
                list = (
                    self.__db["lists"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                            "media_type": type,
                        },
                    )
                    .skip(skip * limit)
                    .limit(limit)
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                total = self.__db["lists"].count_documents(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                    },
                )

                return {
                    "results": cvtJson(list) if list != None else [],
                    "total": total,
                }

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def search_list(self, type):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            # skip = request.args.get("skip", default=0, type=int)
            query = request.args.get("query", default="", type=str)

            if type == "all":
                list = (
                    self.__db["lists"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ],
                        }
                    )
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                return {
                    "results": cvtJson(list) if list != None else [],
                    "total": len(cvtJson(list)) if list != None else 0,
                }

            elif type == "movie":
                list = self.__db["lists"].find(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ],
                    },
                )

                return {
                    "results": cvtJson(list) if list != None else [],
                    "total": len(cvtJson(list)) if list != None else 0,
                }

            elif type == "tv":
                list = self.__db["lists"].find(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ],
                    },
                )

                return {
                    "results": cvtJson(list) if list != None else [],
                    "total": len(cvtJson(list)) if list != None else 0,
                }

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def getitem_list(self, type, movieId):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            item_list = self.__db["lists"].find_one(
                {
                    "user_id": jwtUser["id"],
                    "movie_id": movieId,
                    "media_type": type,
                },
            )

            if item_list != None:
                return {"success": True, "result": cvtJson(item_list)}
            else:
                return {"success": False, "result": "Failed to get item in list"}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def additem_list(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            movie_id = request.form["movie_id"]
            media_type = request.form["media_type"]
            idItemList = str(uuid.uuid4())

            if media_type == "movie":
                movie = self.__db["movies"].find_one(
                    {"id": movie_id},
                )

                if movie != None:
                    item_lists = self.__db["lists"].find_one(
                        {
                            "user_id": jwtUser["id"],
                            "movie_id": movie_id,
                            "media_type": media_type,
                        },
                    )

                    if item_lists == None:
                        self.__db["lists"].insert_one(
                            {
                                "id": str(idItemList),
                                "user_id": jwtUser["id"],
                                "movie_id": movie_id,
                                "name": movie["name"],
                                "original_name": movie["original_name"],
                                "original_language": movie["original_language"],
                                "media_type": media_type,
                                "genres": movie["genres"],
                                "backdrop_path": movie["backdrop_path"],
                                "poster_path": movie["poster_path"],
                                "dominant_backdrop_color": movie[
                                    "dominant_backdrop_color"
                                ],
                                "dominant_poster_color": movie["dominant_poster_color"],
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        return {
                            "success": True,
                            "results": "Add item to list suucessfully",
                        }
                    else:
                        raise DefaultError("Movie already exist in list")

                else:
                    raise DefaultError("Movie is not exists")

            elif media_type == "tv":
                tv = self.__db["tvs"].find_one(
                    {"id": movie_id},
                )

                if tv != None:
                    item_lists = self.__db["lists"].find_one(
                        {
                            "user_id": jwtUser["id"],
                            "movie_id": movie_id,
                            "media_type": media_type,
                        },
                    )

                    if item_lists != None:
                        raise DefaultError("Movie already exist in list")
                    else:
                        self.__db["lists"].insert_one(
                            {
                                "id": str(idItemList),
                                "user_id": jwtUser["id"],
                                "movie_id": movie_id,
                                "name": tv["name"],
                                "original_name": tv["original_name"],
                                "original_language": tv["original_language"],
                                "media_type": media_type,
                                "genres": tv["genres"],
                                "backdrop_path": tv["backdrop_path"],
                                "poster_path": tv["poster_path"],
                                "dominant_backdrop_color": tv[
                                    "dominant_backdrop_color"
                                ],
                                "dominant_poster_color": tv["dominant_poster_color"],
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        return {
                            "success": True,
                            "results": "Add item to list suucessfully",
                        }
                else:
                    raise DefaultError("Movie is not exists")

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except DefaultError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def remove_item_list(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            movie_id = request.form["movie_id"]
            media_type = request.form["media_type"]

            resultDelete1 = self.__db["lists"].delete_one(
                {
                    "user_id": jwtUser["id"],
                    "movie_id": movie_id,
                    "media_type": media_type,
                },
            )

            if resultDelete1.deleted_count == 1:
                return {
                    "success": True,
                    "results": "Remove item from list suucessfully",
                }
            else:
                raise DefaultError("Delete movie from list failed")

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def removeall_item_list(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            resultDelete = self.__db["lists"].delete_many(
                {"user_id": jwtUser["id"]},
            )

            if resultDelete.deleted_count >= 1:
                list = (
                    self.__db["lists"].find({"user_id": jwtUser["id"]}).skip(0).limit(1)
                )
                return {"success": True, "results": cvtJson(list)}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
