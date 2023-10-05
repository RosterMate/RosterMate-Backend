import pymongo

uri = "mongodb+srv://sithumv:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

client = pymongo.MongoClient(uri)

db = client['RosterMateDB']

collection = db['WardDetails']

new_field_name = 'MaxLeaves'
new_field_value= 5

for document in collection.find({}):
    document[new_field_name] = new_field_value
    collection.update_one({"_id": document["_id"]}, {"$set": {new_field_name:new_field_value}})

client.close()