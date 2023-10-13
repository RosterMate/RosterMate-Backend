from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import JsonResponse
from bson import ObjectId

from .models import LeaveRequests_collection
from .models import UserDoctor_collection
from .models import UserConsultant_collection
from .models import WardDetail_collection
from .models import UserAuth_collection

from database_Connection import db



@api_view(['POST'])
def wardDetails(request):

    #print("Data from frontend -")
    ward_details_collection = db['WardDetails']

    projection = {'wardName': 1, 'NoOfDoctors': 1}
    ward_details = [{'wardName': i['wardName'], 'NoOfDoctors': i['NoOfDoctors']} for i in ward_details_collection.find({}, projection)]


    if ward_details:
        return Response(ward_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def doctorDetails(request):
    
    doctor_details_collection = db['User-Doctor']
    projection = {'name': 1, 'position': 1,'img':1}
    doctor_details = [{'name': i['name'], 'position': i['position'],'img':i['img']} for i in doctor_details_collection.find({}, projection)]

    if doctor_details:
        return Response(doctor_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def consultantDetails(request):

    consultant_details_collection = db['User-Consultant']
    projection = {'name': 1, 'position': 1,'img':1}
    consultant_details = [{'name': i['name'], 'position': i['position'],'img':i['img']} for i in consultant_details_collection.find({}, projection)]

    if consultant_details:
        return Response(consultant_details)
    else:
        return JsonResponse(None) 
    

@api_view(['POST'])
def view_profile(request):

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
    profile_details = [{'name': i['name'], 'position': i['position'],'img':i['img'],'address':i['address'],'mobile':i['mobile']} for i in profile_details_collection.find({'email':request.data['email']}, projection)][0]
    #,'information':i['information'],
    
    if profile_details:
        return Response(profile_details)
    else:
        return JsonResponse(None)
    

@api_view(['POST'])
def leaveRequests(request):
    # Define the query conditions for each Status
    query_conditions = [
        {'Status': "NoResponse"},
        {'Status': "Accepted"},
        {'Status': "Rejected"},
    ]
    if request.data['type'] == "Consultant":
        consultant_collection = UserConsultant_collection

    current_consultant = consultant_collection.find_one({'email': request.data['email']})
    if current_consultant:
        ward_numbers = [current_consultant.get('wardNumber', [])]
    
    leaveReq_details = []
    
    for condition in query_conditions:
        # Use list comprehension to convert ObjectId to string
        documents = list(LeaveRequests_collection.find({'wardNumber': {'$in': ward_numbers}, **condition}))
        converted_documents = [
            {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()} 
            for doc in documents
        ]
        leaveReq_details.append(converted_documents)
        leaveReq_flattened_list = [item for sublist in leaveReq_details for item in (sublist if isinstance(sublist, list) else [sublist])]

    if any(leaveReq_flattened_list):
        return Response(leaveReq_flattened_list)
    else:
        return JsonResponse(None, safe=False)
    


@api_view(['POST'])
def view_all_users(request):
    user_type = request.data.get('type')
    email = request.data.get('email')

    if user_type == "Consultant":
        consultant = UserConsultant_collection.find_one({'email': email})
        
        if consultant:
            ward_number = consultant.get('wardNumber')
            doctors_in_wards = list(UserDoctor_collection.find({'wardNumber': ward_number}, projection={'_id': 0, 'img': 1, 'name': 1, 'position': 1}))
            
            if doctors_in_wards:
                return Response(doctors_in_wards)
            else:
                return JsonResponse({'message': 'No doctors found in the same ward'}, status=404)
        else:
            return JsonResponse({'message': 'Consultant not found'}, status=404)
    
    return JsonResponse({'message': 'Invalid user type'}, status=400)

@api_view(['POST'])
def addWard(request):
    wardName = request.data.get('wardname')
    wardNumber = request.data.get('wardnumber')
    Shifts = int(request.data.get('shifts'))
    MaxLeaves = int(request.data.get('maxleaves'))
    ConsecutiveShifts = int(request.data.get('consecutiveshifts'))
    NoOfDoctors = int(request.data.get('maxnumberdoctors'))

    ward_details_collection = db['WardDetails']
    query = {"wardNumber": wardNumber}
    result = ward_details_collection.find_one(query)

    if result:
        return Response({'error': 'true'})

    # print((wardName,wardNumber,Shifts,MaxLeaves,ConsecutiveShifts,NoOfDoctors))
    ward_data = {
        'wardName': wardName,
        'wardNumber': wardNumber,
        'Shifts': Shifts,
        'ConsecutiveShifts': ConsecutiveShifts,
        'NoOfDoctors': 0,
        'MaxLeaves': MaxLeaves
    }

    WardDetail_collection.insert_one(ward_data)
    return Response({'message': 'Ward added successfully'})

@api_view(['POST'])
def sendWardDetails(request):
    projection = {'wardName': 1, 'wardNumber': 1}
    ward_details = [{'wardName': i['wardName'], 'wardNumber': i['wardNumber']} for i in WardDetail_collection.find({}, projection)]
    if ward_details:
        return Response(ward_details)
    else:
        return JsonResponse(None)

@api_view(['POST'])
def addDoctor(request):
    fullName = request.data.get('fullname')
    mobileNo = request.data.get('mobileNo')
    email = (request.data.get('email'))
    password = (request.data.get('password'))
    address = (request.data.get('address'))
    position = (request.data.get('position'))
    degree = (request.data.get('degree'))
    specialization = (request.data.get('specialization'))
    wardNumber = (request.data.get('wardnumber'))

    # print((wardName,wardNumber,Shifts,MaxLeaves,ConsecutiveShifts,NoOfDoctors))
    doctor_data = {
        'email': email,
        'position': position,
        'name': fullName,
        'mobile': mobileNo,
        'address': address,
        'img':'',
        'wardNumber': wardNumber,
        'Degree':degree,
        'Specialization':specialization,
    }
    print(doctor_data)

    UserAuth_Doctor = {
        'email':email,
        'password': password,
        'type': 'Doctor',
        'name': fullName,
    }
    print(UserAuth_Doctor)

    UserDoctor_collection.insert_one(doctor_data)
    UserAuth_collection.insert_one(UserAuth_Doctor)
    return Response({'message': 'Doctor added successfully'})

@api_view(['POST'])
def addConsultant(request):
    fullName = request.data.get('fullname')
    mobileNo = request.data.get('mobileNo')
    email = (request.data.get('email'))
    password = (request.data.get('password'))
    address = (request.data.get('address'))
    position = (request.data.get('position'))
    degree = (request.data.get('degree'))
    specialization = (request.data.get('specialization'))
    wardNumber = (request.data.get('wardnumber'))

    # print((wardName,wardNumber,Shifts,MaxLeaves,ConsecutiveShifts,NoOfDoctors))
    consultant_data = {
        'email': email,
        'position': position,
        'name': fullName,
        'mobile': mobileNo,
        'address': address,
        'img':'',
        'wardNumber': wardNumber,
        'Degree':degree,
        'Specialization':specialization,
    }

    UserAuth_Consultant = {
        'email':email,
        'password': password,
        'type': 'Consultant',
        'name': fullName,
    }

    UserConsultant_collection.insert_one(consultant_data)
    UserAuth_collection.insert_one(UserAuth_Consultant)
    return Response({'message': 'Consultant added successfully'})