from arctic import Arctic
import pymongo

def get_localhost_mongo_client():

    client = pymongo.MongoClient('localhost', 27017)
    adb = Arctic(client)

    return adb

