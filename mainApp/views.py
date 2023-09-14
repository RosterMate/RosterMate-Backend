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
    
@api_view(['POST'])
def view_profile(request):

    #print("Data from frontend -",request.data)
    client = MongoClient(uri)
    db = client.RosterMateDB
    if request.data['type'] == "Admin":
        profile_details_collection = db['User-Admin']
    elif request.data['type'] == "Doctor":
        profile_details_collection = db['User-Doctor']
    elif request.data['type'] == "Consultant":
        profile_details_collection = db['User-Consultant']

    projection = {'img': 1,
    'name': 1,
    'position': 1,
    'address': 1,
    'information': 1,
    'mobile': 1,}
    profile_details = [{'name': i['name'], 'position': i['position'],'img':i['img'],'address':i['address'],'information':i['information'],'mobile':i['mobile']} for i in profile_details_collection.find({'email':request.data['email']}, projection)][0]

    client.close()
    #print(profile_details)
    if profile_details:
        return Response(profile_details)
    else:
        return JsonResponse(None)
    

@api_view(['POST'])
def addWard(request):

    print("Data from frontend -",request.data)

    return Response(None)