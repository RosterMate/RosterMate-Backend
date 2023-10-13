from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import HttpResponse

uri = "mongodb+srv://sithumv:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

@api_view(['POST'])
def user_login(request):

    print("Data from frontend -", request.data['email'], request.data['password'])

    client = MongoClient(uri)
    db = client.RosterMateDB
    collection = db['UserAuth']
    user = list(collection.find({"email": request.data['email']}))
    user = user[0]
    client.close()

    if user['password'] == request.data['password'] and user['email'] == request.data['email']:
        data = {
            'isAuthenticated': True,
            'USERTYPE': user['type'],
            'NAME': user['name'],
        }
        return Response(data)
    else:
        data = {
            'isAuthenticated': False,
            'USERTYPE': 'Public',
        }
        return Response(data)

# def add(request):
#     name = "Example"
#     description = "This is an example document."

#     my_doc = MyCollection(name=name, description=description)
#     my_doc.save()

#     return HttpResponse("Data added to the collection.")

