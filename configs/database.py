import pymongo


def ConnectMongoDB():
    try:
        myclient = pymongo.MongoClient(
            "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
        )

        db = myclient["Phimhay247_DB"]
        return db
    except:
        pass
