import pymongo

uri = "mongodb+srv://sithumv:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

client = pymongo.MongoClient(uri)

db = client['RosterMateDB']

collection = db['User-Doctor']

field_to_delete = 'information'

# Use $unset operator to remove the field from all documents
collection.update_many({}, {"$unset": {field_to_delete: ""}})

client.close()