import pymongo
import pandas as pd
import json


class MongoDBManagement:

    def __init__(self, username, password):
        """
        This function sets the required url
        """
        try:
            self.username = username
            self.password = password
            self.url = "mongodb+srv://{}:{}@videosecondarydata.n1adhls.mongodb.net/?retryWrites=true&w=majority".format(
                self.username, self.password)
            # self.url = 'localhost:27017'
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n" + str(e))

    def getMongoDBClientObject(self):
        """
        This function creates the client object for connection purpose
        """
        try:
            mongo_client = pymongo.MongoClient(self.url)
            return mongo_client
        except Exception as e:
            raise Exception("(getMongoDBClientObject): Something went wrong on creation of client object\n" + str(e))

    def closeMongoDBconnection(self, mongo_client):
        """
        This function closes the connection of client
        :return:
        """
        try:
            mongo_client.close()
        except Exception as e:
            raise Exception(f"Something went wrong on closing connection\n" + str(e))

    def isDatabasePresent(self, db_name):
        """
        This function checks if the database is present or not.
        :param db_name:
        :return:
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.close()
                return True
            else:
                mongo_client.close()
                return False
        except Exception as e:
            raise Exception("(isDatabasePresent): Failed on checking if the database is present or not \n" + str(e))

    def createDatabase(self, db_name):
        """
        This function creates database.
        :param db_name:
        :return:
        """
        try:
            database_check_status = self.isDatabasePresent(db_name=db_name)
            if not database_check_status:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
            else:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
        except Exception as e:
            raise Exception(f"(createDatabase): Failed on creating database\n" + str(e))

    def getDatabase(self, db_name):
        """
        This returns databases.
        """
        try:
            mongo_client = self.getMongoDBClientObject()
           
            return mongo_client[db_name]
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")

    def getCollection(self, collection_name, db_name):
        """
        This returns collection.
        :return:
        """
        try:
            database = self.getDatabase(db_name)
            return database[collection_name]
        except Exception as e:
            raise Exception(f"(getCollection): Failed to get the database list.")

    def isCollectionPresent(self, collection_name, db_name):
        """
        This checks if collection is present or not.
        :param collection_name:
        :param db_name:
        :return:
        """
        try:
            database_status = self.isDatabasePresent(db_name=db_name)
            if database_status:
                database = self.getDatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"(isCollectionPresent): Failed to check collection\n" + str(e))

    def createCollection(self, collection_name, db_name):
        """
        This function creates the collection in the database given.
        :param collection_name:
        :param db_name:
        :return:
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, db_name=db_name)
            if not collection_check_status:
                database = self.getDatabase(db_name=db_name)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"(createCollection): Failed to create collection {collection_name}\n" + str(e))

    def freeCollection(self, collection_name, db_name):
        """
        This function drops the collection
        :param collection_name:
        :param db_name:
        :return:
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, db_name=db_name)
                collection.delete_many({})
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(freeCollection): Failed to free collection {collection_name}")

    def insertRecord(self, db_name, collection_name, record):
        """
        This inserts a record.
        :param db_name:
        :param collection_name:
        :param record:
        :return:
        """
        try:
            # collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(collection_name=collection_name, db_name=db_name)
            collection.insert_one(record)
            sum = 0
            return f"rows inserted "
        except Exception as e:
            raise Exception(f"(insertRecord): Something went wrong on inserting record\n" + str(e))

    

    def findAllRecords(self, db_name, collection_name):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, db_name=db_name)
                findAllRecords = collection.find()
                return findAllRecords
        except Exception as e:
            raise Exception(f"(findAllRecords): Failed to find record for the given collection and database\n" + str(e))

   
