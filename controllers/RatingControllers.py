import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]

# db["seasons"].find_one_and_delete({"id": 182643})

# db["tvs"].update_many(
#     {"genres": {"$elemMatch": {"id": 10762}}},
#     {"$set": {"genres.$[element].name": "Trẻ em"}},
#     upsert=False,
#     array_filters=[
#         {"element.id": 10762},
#     ],
# )

# db["accounts"].update_many({}, {"$set": {"role": "normal"}})

# db["hieus"].update_many({}, {"$rename": {"popularity": "views"}})


def rating_movie_tv(type, id):
    try:
        rateValue = float(request.form["value"])
        if type == "movie":
            movie_dumps = db["movies"].find_one({"id": int(id)})
            new_vote_average = (
                movie_dumps["vote_count"] * movie_dumps["vote_average"] + rateValue
            ) / (movie_dumps["vote_count"] + 1)

            new_movie = db["movies"].find_one_and_update(
                {"id": int(id)},
                {
                    "$set": {
                        "vote_average": new_vote_average,
                        "vote_count": movie_dumps["vote_count"] + 1,
                    },
                },
                return_document=ReturnDocument.AFTER,
            )

            return {
                "success": True,
                "vote_average": new_movie["vote_average"],
                "vote_count": new_movie["vote_count"],
            }

        elif type == "tv":
            tv_dumps = db["tvs"].find_one({"id": int(id)})
            new_vote_average = (
                tv_dumps["vote_count"] * tv_dumps["vote_average"] + rateValue
            ) / (tv_dumps["vote_count"] + 1)

            new_tv = db["tvs"].find_one_and_update(
                {"id": int(id)},
                {
                    "$set": {
                        "vote_average": new_vote_average,
                        "vote_count": tv_dumps["vote_count"] + 1,
                    },
                },
                return_document=ReturnDocument.AFTER,
            )

            return {
                "success": True,
                "vote_average": new_tv["vote_average"],
                "vote_count": new_tv["vote_count"],
            }
    except PyMongoError as e:
        return {"success": e._message}
