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
    
            headers = request.headers
            
            extraValue2 = {
                "list":[],
                "history":[],
                "rate":[],
            }

            if "Authorization" in headers or request.cookies.get("user_token") != None:
                user_token = request.headers["Authorization"].replace(
                    "Bearer ", ""
                ) or request.cookies.get("user_token")

                jwtUser = jwt.decode(
                    user_token,
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithms=["HS256"],
                )

                # item_list = self.__db["lists"].find_one(
                #     {
                #         "user_id": jwtUser["id"],
                #         "movie_id": id,
                #         "media_type": "movie",
                #     },
                # )

                # if item_list != None:
                #     extraValue2 = extraValue2 | {"in_list": True}
                    
                extraValue2["list"] = [
                    {
                        "$lookup": {
                        "from": 'lists',
                        "localField": 'id',
                        "foreignField": 'movie_id',
                        "pipeline": [
                            {
                            "$match": {
                                "$and": [
                                { "$expr": { "$eq": ['$media_type', 'movie'] } },
                                { "$expr": { "$eq": ['$user_id', jwtUser["id"]] } },
                                ],
                            },
                            },
                        ],
                        "as": 'in_list',
                        },
                    },
                    {
                        "$addFields": {
                            "in_list": {
                                "$eq": [{ "$size": '$in_list' }, 1],
                            },
                        },
                    },
                ]   

                # item_history = self.__db["histories"].find_one(
                #     {
                #         "user_id": jwtUser["id"],
                #         "movie_id": id,
                #         "media_type": "movie",
                #     },
                # )

                # if item_history != None:
                #     extraValue2 = extraValue2 | {
                #         "history_progress": {
                #             "duration": item_history["duration"],
                #             "percent": item_history["percent"],
                #             "seconds": item_history["seconds"],
                #         },
                #     }
                
                extraValue2["history"] = [
                    {
                        "$lookup": {
                        "from": 'histories',
                        "localField": 'id',
                        "foreignField": 'movie_id',
                        "pipeline": [
                            {
                            "$match": {
                                "$and": [
                                { "$expr": { "$eq": ['$media_type', 'movie'] } },
                                { "$expr": { "$eq": ['$user_id', jwtUser["id"]] } },
                                ],
                            },
                            },
                        ],
                        "as": 'in_list',
                        },
                    },
                    {
                        "$addFields": {
                            "history_progress": {
                                "$cond": [
                                    {
                                        "$eq": [{ "$size": '$history_progress' }, 1],
                                    },
                                    {
                                        "duration": '$history_progress.duration',
                                        "percent": '$history_progress.percent',
                                        "seconds": '$history_progress.seconds',
                                    },
                                    '$$REMOVE',
                                ],
                            },
                        },
                    },
                ]   
                
                
                # rates = self.__db["rates"].find_one(
                #     {
                #         "user_id": jwtUser["id"],
                #         "movie_id": str(id),
                #         "movie_type": "movie",
                #     }
                # )

                # if rates != None:
                #     extraValue2 = extraValue2 | {
                #         "rated_value": rates["rate_value"],
                #     }
                          
                extraValue2["rate"] = [
                    {
                        "$lookup": {
                        "from": 'rates',
                        "localField": 'id',
                        "foreignField": 'movie_id',
                        "pipeline": [
                            {
                            "$match": {
                                "$and": [
                                { "$expr": { "$eq": ['$movie_type', 'movie'] } },
                                { "$expr": { "$eq": ['$user_id', jwtUser["id"]] } },
                                ],
                            },
                            },
                        ],
                        "as": 'in_list',
                        },
                    },
                    {
                        "$unwind": {
                            "path": '$rated_value',
                            "preserveNullAndEmptyArrays": True,
                        },
                    },
                    {
                        "$addFields": {
                            "rated_value": '$rated_value.rate_value',
                        },
                    },
                ]   
                
                # return cvtJson(movie[0] | extraValue2)
                

            movie = cvtJson(self.__db["movies"].aggregate([
                {
                    "$match": {"id": id},
                },
                *extraValue["images"],
                *extraValue["videos"],
                *extraValue["credits"],
                *extraValue2["list"],
                *extraValue2["history"],
                *extraValue2["rate"],
            ]))

            if len(movie) == 0:
                return {"not_found": True, "result": "Can not find the movie"}
            
            return cvtJson(movie[0]) 
                    # | extraValue

        except jwt.ExpiredSignatureError as e:
            make_response().delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            make_response().delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
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
