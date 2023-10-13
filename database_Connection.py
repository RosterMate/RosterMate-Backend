import pymongo

uri = "mongodb+srv://thejanbweerasekara:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

client = pymongo.MongoClient(uri)

db = client['RosterMateDB']