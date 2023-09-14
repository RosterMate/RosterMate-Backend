from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import JsonResponse

uri = "mongodb+srv://thejanbweerasekara:atYiYnBqom0ZrQXt@rostermatedb.n9yfrig.mongodb.net/"

@api_view(['POST'])
def wardDetails(request):

    #print("Data from frontend -")
    client = MongoClient(uri)
    db = client.RosterMateDB
    ward_details_collection = db['WardDetails']

    projection = {'wardName': 1, 'NoOfDoctors': 1}
    ward_details = [{'wardName': i['wardName'], 'NoOfDoctors': i['NoOfDoctors']} for i in ward_details_collection.find({}, projection)]

    client.close()

    if ward_details:
        return Response(ward_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def doctorDetails(request):

    #print("Data from frontend -")
    client = MongoClient(uri)
    db = client.RosterMateDB
    doctor_details_collection = db['User-Doctor']

    projection = {'name': 1, 'position': 1,'img':1}
    doctor_details = [{'name': i['name'], 'position': i['position'],'img':i['img']} for i in doctor_details_collection.find({}, projection)]

    client.close()

    if doctor_details:
        return Response(doctor_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def consultantDetails(request):

    #print("Data from frontend -")
    client = MongoClient(uri)
    db = client.RosterMateDB
    consultant_details_collection = db['User-Consultant']

    projection = {'name': 1, 'position': 1,'img':1}
    consultant_details = [{'name': i['name'], 'position': i['position'],'img':i['img']} for i in consultant_details_collection.find({}, projection)]

    client.close()

    if consultant_details:
        return Response(consultant_details)
    else:
        return JsonResponse(None)