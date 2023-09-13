from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient

@api_view(['POST'])
def user_login(request):

    #print("Data from frontend -", request.data['email'], request.data['password'])

    client = MongoClient('localhost', 27017)
    db = client['rosterMateDB']
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