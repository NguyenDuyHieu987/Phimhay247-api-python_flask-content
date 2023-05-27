import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage
from flask import *
from pymongo import ReturnDocument
import os
import jwt

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
            exceptValue = {"images": 0, "credits": 0, "videos": 0}

            if append_to_response != "":
                if "images" in append_to_response.split(","):
                    exceptValue.pop("images")
                if "credits" in append_to_response.split(","):
                    exceptValue.pop("credits")
                if "videos" in append_to_response.split(","):
                    exceptValue.pop("videos")

            movie = self.__db["movies"].find_one({"id": int(id)}, exceptValue)

            headers = request.headers

            if "Authorization" not in headers:
                if movie != None:
                    return cvtJson(movie)
                else:
                    return {"not_found": True, "result": "Can not find the movie"}
            else:
                user_token = request.headers["Authorization"].replace("Bearer ", "")

                jwtUser = jwt.decode(
                    user_token,
                    str(os.getenv("JWT_TOKEN_SECRET")),
                    algorithms=["HS256"],
                )
                item_lists = self.__db["lists"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$elemMatch": {"id": int(id)}}}
                )

                if "items" in item_lists:
                    movie = movie | {"in_list": True}
                else:
                    movie = movie | {"in_list": False}

                item_watchlists = self.__db["watchlists"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$elemMatch": {"id": int(id)}}}
                )

                if "items" in item_watchlists:
                    movie = movie | {
                        "in_history": True,
                        "history_progress": {
                            "duration": item_watchlists["items"][0]["duration"],
                            "percent": item_watchlists["items"][0]["percent"],
                            "seconds": item_watchlists["items"][0]["seconds"],
                        },
                    }
                else:
                    movie = movie | {"in_history": False}

                return cvtJson(movie)

        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {"not_found": True, "result": "Can not find the movie"}

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

        except:
            return {"success": False, "result": "Add movie failed"}

    def edit_movie(self, id):
        try:
            formMovie = request.form

            movie = self.__db["tans"].find_one_and_update(
                {"id": int(id)},
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
        except:
            return {"success": False, "message": "Edit movie failed"}

    def update_view_movie(self, id):
        try:
            movie_dumps = self.__db["movies"].find_one({"id": int(id)})
            new_views = int(movie_dumps["views"]) + 1

            self.__db["movies"].update_one(
                {"id": int(id)},
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
        except:
            return {"success": False, "result": "Update views of movie failed"}
