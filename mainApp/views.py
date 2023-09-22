from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import JsonResponse
from .models import LeaveRequests_collection
from bson import ObjectId

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


@api_view(['POST'])
def leaveRequests(request):
    # Define the query conditions for each Status
    query_conditions = [
        {'Status': "NoResponse"},
        {'Status': "Accepted"},
        {'Status': "Rejected"},
    ]

    leaveReq_details = []

    for condition in query_conditions:
        # Use list comprehension to convert ObjectId to string
        documents = list(LeaveRequests_collection.find(condition))
        converted_documents = [
            {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()} 
            for doc in documents
        ]
        leaveReq_details.append(converted_documents)
        leaveReq_flattened_list = [item for sublist in leaveReq_details for item in (sublist if isinstance(sublist, list) else [sublist])]

    if any(leaveReq_flattened_list):
        return Response(leaveReq_flattened_list)
    else:
        return JsonResponse(None)