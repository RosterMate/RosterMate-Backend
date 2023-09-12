from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def user_login(request):
    data = {
        'USERTYPE': 'admin',
        'NAME': 'Dr.Kamal',
    }
    return Response(data)