from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import HttpResponse

from database_Connection import db

@api_view(['POST'])
def user_login(request):

    collection = db['UserAuth']
    user = list(collection.find({"email": request.data['email']}))
    user = user[0]

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

