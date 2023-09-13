from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient

uri = "mongodb+srv://thejanbweerasekara:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

@api_view(['POST'])
def user_login(request):

    #print("Data from frontend -", request.data['email'], request.data['password'])

    client = MongoClient(uri)
    db = client.RosterMateDB
    rmusers_collection = db['RMusers']
    rmusers_data = list(rmusers_collection.find({}))
    client.close()
    for user in rmusers_data:
        #print("TEST ",user['email'],request.data['email'],)
        if user['email'] == request.data['email']:
            if user['password'] != request.data['password']:
                break
            data = {
                'isAuthenticated': True,
                'USERTYPE': user['type'],
                'NAME': user['name'],
            }
            return Response(data)

    #print(rmusers_data)
    data = {
        'isAuthenticated': False,
        'USERTYPE': 'Public',
    }

    return Response(data)