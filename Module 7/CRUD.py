from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30737
        DB = 'aac'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
		insertSuccess = self.database.animals.insert(data)  # data should be dictionary
        #Check inserSuccess for operation
        if insertSuccess != 0:
            return False
        #default return
        return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Create method to implement the R in CRUD.
    def read(self, searchData):
        if searchData:
            data = self.database.animals.find(searchData, {"_id": False})
        else:
            data = self.database.animals.find( {}, {"_id": False})
            #Return the data else let error flow up
            return data

# Create method to implement the U in CRUD
    def update(self, searchData, updateData):
        if searchData in not None:
            result = self.database.animals.update_many(searchData, { "$set": upddateData})
        else:
            return "{}"
        #Return the dataset else let the error flow up
        return result.raw_result

# Create method to implemnt the D in CRUD
    def delete)self, deleteData):
        if deleteData in not None:
            result = self.database.animals.delete_many(deleteData)
        else:
            return "{}"
        #Return the dataset else let the error flow up
        return result.raw_result


