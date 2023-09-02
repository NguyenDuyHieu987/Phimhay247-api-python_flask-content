import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from pymongo import ReturnDocument
import os
import jwt
from collections import ChainMap

# import uuid
from configs.database import Database


class Movie(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def detail_movie(self, id):
        try:
            append_to_response = request.args.get(
                "append_to_response", default="", type=str
            )
            # exceptValue = {"images": 0, "credits": 0, "videos": 0}
            extraValue = {
                "images": [],
                "videos": [],
                "credits": []
            }

            if append_to_response != "":
                if "images" in append_to_response.split(","):
                    # images = self.__db["images"].find_one(
                    #     {"movie_id": str(id)})
                    # extraValue["images"] = images["items"]

                    extraValue["images"] = [{
                        "$lookup": {
                            "from": 'images',
                            "localField": 'id',
                            "foreignField": 'movie_id',
                            "as": 'images',
                        },
                    },
                        {"$unwind": '$images'},
                        {
                            "$addFields": {
                                "images": '$images.items',
                            },
                    }]

                if "videos" in append_to_response.split(","):
                    # videos = self.__db["videos"].find_one(
                    #     {"movie_id": str(id)})
                    # extraValue["videos"] = videos["items"]

                    extraValue["videos"] = [
                        {
                            "$lookup": {
                                "from": 'videos',
                                "localField": 'id',
                                "foreignField": 'movie_id',
                                "as": 'videos',
                            },
                        },
                        {"$unwind": '$videos'},
                        {
                            "$addFields": {
                                "videos": '$videos.items',
                            },
                        },
                    ]

                if "credits" in append_to_response.split(","):
                    # credits = self.__db["credits"].find_one(
                    #     {"movie_id": str(id)})
                    # extraValue["credits"] = credits["items"]

                    extraValue["credits"] = [
                        {
                            "$lookup": {
                                "from": 'credits',
                                "localField": 'id',
                                "foreignField": 'movie_id',
                                "as": 'credits',
                            },
                        },
                        {"$unwind": '$credits'},
                        {
                            "$addFields": {
                                "credits": '$credits.items',
                            },
                        },
                    ]

            # movie = self.__db["movies"].find_one({"id": str(id)}, exceptValue)

            # movie = self.__db["movies"].find_one({"id": str(id)}) | extraValue

            movie = cvtJson(self.__db["movies"].aggregate([
                {
                    "$match": {"id": id},
                },
                *extraValue["images"],
                *extraValue["videos"],
                *extraValue["credits"],
            ]))

            headers = request.headers

            if "Authorization" not in headers:
                if len(movie) > 0:
                    return movie[0]
                else:
                    return {"not_found": True, "result": "Can not find the movie"}
            else:
                user_token = request.headers["Authorization"].replace(
                    "Bearer ", "")

                jwtUser = jwt.decode(
                    user_token,
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithms=["HS256"],
                )

                extraValue2 = {}

                item_list = self.__db["lists"].find_one(
                    {
                        "user_id": jwtUser["id"],
                        "movie_id": id,
                        "media_type": "movie",
                    },
                )

                if item_list != None:
                    extraValue2 = extraValue2 | {"in_list": True}

                item_history = self.__db["histories"].find_one(
                    {
                        "user_id": jwtUser["id"],
                        "movie_id": id,
                        "media_type": "movie",
                    },
                )

                if item_history != None:
                    extraValue2 = extraValue2 | {
                        "history_progress": {
                            "duration": item_history["duration"],
                            "percent": item_history["percent"],
                            "seconds": item_history["seconds"],
                        },
                    }

                rates = self.__db["rates"].find_one(
                    {
                        "user_id": jwtUser["id"],
                        "movie_id": str(id),
                        "movie_type": "movie",
                    }
                )

                if rates != None:
                    extraValue2 = extraValue2 | {
                        "rated_value": rates["rate_value"],
                    }

                return cvtJson(movie[0] | extraValue2)

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def add_movie(self):
        try:
            formMovie = request.form

            # id = uuid.uuid1().time_mid
            movie = self.__db["phimles"].find_one({"id": int(formMovie["id"])})
            tv = self.__db["phimbos"].find_one({"id": int(formMovie["id"])})
            # while movie != None and tv != None:
            #     id = uuid.uuid1().time_mid
            #     movie = self.__db["phimles"].find_one({"id": int(id)})

            if movie == None and tv == None:
                self.__db["phimles"].insert_one(
                    {
                        "id": int(formMovie["id"]),
                        "name": formMovie["name"],
                        "original_name": formMovie["original_name"],
                        "original_language": formMovie["original_language"],
                        "poster_path": formMovie["poster_path"],
                        "backdrop_path": formMovie["backdrop_path"],
                        "release_date": formMovie["release_date"],
                        "genres": json.loads(formMovie["genres"]),
                        "overview": formMovie["overview"],
                        "budget": int(formMovie["budget"]),
                        "revenue": int(formMovie["revenue"]),
                        "runtime": int(formMovie["runtime"]),
                        "status": formMovie["status"],
                        "views": 0,
                        "media_type": "movie",
                    },
                )
                return {"success": True, "result": "Add movie successfully"}
            else:
                return {
                    "success": False,
                    "already": True,
                    "result": "Movie is already exist",
                }

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def edit_movie(self, id):
        try:
            formMovie = request.form

            movie = self.__db["phimles"].find_one_and_update(
                {"id": str(id)},
                {
                    "$set": {
                        "name": formMovie["name"],
                        "original_name": formMovie["original_name"],
                        "original_language": formMovie["original_language"],
                        "release_date": formMovie["release_date"],
                        "genres": json.loads(formMovie["genres"]),
                        "overview": formMovie["overview"],
                        "budget": int(formMovie["budget"]),
                        "revenue": int(formMovie["revenue"]),
                        "runtime": int(formMovie["runtime"]),
                        "views": int(formMovie["views"]),
                        "status": formMovie["status"],
                    },
                },
                return_document=ReturnDocument.AFTER,
            )

            return {
                "success": True,
                "result": cvtJson(movie),
                "message": "Edit movie successfully",
            }
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def update_view(self, id):
        try:
            movie_dumps = self.__db["movies"].find_one({"id": str(id)})
            new_views = int(movie_dumps["views"]) + 1

            self.__db["movies"].update_one(
                {"id": str(id)},
                {
                    "$set": {
                        "views": new_views,
                    },
                },
            )

            return {
                "success": True,
                "result": "Update views of movie successfully",
            }
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
