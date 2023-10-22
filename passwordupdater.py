import pymongo
import hashing

uri = "mongodb+srv://sithumv:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

client = pymongo.MongoClient(uri)

db = client['RosterMateDB']

collection = db['UserAuth']

email = 'sithumv@gmail.com'
new_password = '123456'


hashed_password = hashing.hash_password(new_password)

# Update the password field of the specific user
collection.update_one({'email': email}, {"$set": {'password': hashed_password}})

client.close()