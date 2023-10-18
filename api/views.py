from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import HttpResponse

from database_Connection import db
import jwt
import datetime

secret = 'Rostermate12@#'

@api_view(['POST'])
def user_login(request):

    collection = db['UserAuth']
    user = list(collection.find({"email": request.data['email']}))
    user = user[0]

    if user['password'] == request.data['password'] and user['email'] == request.data['email']:
        token_payload = {
            'id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days = 1)
        }
        jwt_token = jwt.encode(token_payload, "secret", algorithm='HS256')
        data = {
            'isAuthenticated': True,
            'USERTYPE': user['type'],
            'NAME': user['name'],
            'token': jwt_token
        }
        return Response(data)
    else:
        data = {
            'isAuthenticated': False,
            'USERTYPE': 'Public',
        }
        return Response(data)

