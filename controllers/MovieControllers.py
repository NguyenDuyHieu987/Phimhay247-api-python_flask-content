import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument

# import uuid

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def detail_movie(id):
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

        movie = cvtJson(db["movies"].find_one({"id": int(id)}, exceptValue))
        if movie != None:
            return movie
        else:
            return {"not_found": True}

    except:
        return {}


def add_movie():
    try:
        formMovie = request.form

        # id = uuid.uuid1().time_mid
        movie = db["phimles"].find_one({"id": int(formMovie["id"])})
        tv = db["phimbos"].find_one({"id": int(formMovie["id"])})
        # while movie != None and tv != None:
        #     id = uuid.uuid1().time_mid
        #     movie = db["phimles"].find_one({"id": int(id)})

        if movie == None and tv == None:
            db["phimles"].insert_one(
                {
                    "id": int(formMovie["id"]),
                    "title": formMovie["title"],
                    "original_title": formMovie["original_title"],
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


def edit_movie(id):
    try:
        formMovie = request.form

        movie = db["tans"].find_one_and_update(
            {"id": int(id)},
            {
                "$set": {
                    "title": formMovie["title"],
                    "original_title": formMovie["original_title"],
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


def update_view_movie(id):
    try:
        movie_dumps = db["movies"].find_one({"id": int(id)})
        new_views = int(movie_dumps["views"]) + 1

        db["movies"].update_one(
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
