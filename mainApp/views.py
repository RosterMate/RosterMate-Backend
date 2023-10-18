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

##### Admin views #####

@api_view(['POST'])
def adminViwAllDocDetails(request):
    user_type = request.data.get('type')

    if user_type == "Admin":
        doctors_in_wards = list(UserDoctor_collection.find({},{'_id':0}))
        if doctors_in_wards:
            return Response(doctors_in_wards)
        else:
            return JsonResponse({'message': 'No doctors found in this ward'})
    
    return JsonResponse({'message': 'Invalid user type'})   

@api_view(['POST'])
def adminViwAllConDetails(request):
    user_type = request.data.get('type')

    if user_type == "Admin":
        con_in_wards = list(UserConsultant_collection.find({},{'_id':0}))
        if con_in_wards:
            return Response(con_in_wards)
        else:
            return JsonResponse({'message': 'No consultants found in this ward'})
    
    return JsonResponse({'message': 'Invalid user type'})   

@api_view(['POST'])
def wardDetails(request):

    projection = {'wardName': 1, 'NoOfDoctors': 1}
    ward_details = [{'wardName': i['wardName'], 'NoOfDoctors': i['NoOfDoctors']} for i in WardDetail_collection.find({}, projection)]

    if ward_details:
        return Response(ward_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def doctorDetails(request):
    
    projection = {'name': 1, 'position': 1,'img':1}
    doctor_details = [{'name': i['name'], 'position': i['position'],'img':i['img']} for i in UserDoctor_collection.find({}, projection)]

    if doctor_details:
        return Response(doctor_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def consultantDetails(request):

    projection = {'name': 1, 'position': 1,'img':1}
    consultant_details = [{'name': i['name'], 'position': i['position'],'img':i['img']} for i in UserConsultant_collection.find({}, projection)]

    if consultant_details:
        return Response(consultant_details)
    else:
        return JsonResponse(None) 
  
@api_view(['POST'])
def addWard(request):
    wardName = request.data.get('wardname')
    wardNumber = request.data.get('wardnumber')
    Shifts = int(request.data.get('shifts'))
    MaxLeaves = int(request.data.get('maxleaves'))
    ConsecutiveShifts = int(request.data.get('consecutiveshifts'))
    NoOfDoctors = int(request.data.get('maxnumberdoctors'))

    ### Ward ID already exists
    query = {"wardNumber": wardNumber}
    result = WardDetail_collection.find_one(query)
    if result:
        return Response({'error': 'Ward ID'})
    
    ### Ward name already exists
    query = {"wardName": wardName}
    result = WardDetail_collection.find_one(query)
    if result:
        return Response({'error': 'Ward Name'})
    
    ### Add ward data to WardDetails Collection
    ward_data = {
        'wardName': wardName,
        'wardNumber': wardNumber,
        'Shifts': Shifts,
        'ConsecutiveShifts': ConsecutiveShifts,
        'NoOfDoctors': 0,
        'MaxLeaves': MaxLeaves,
        'Doctors': []
    }

    WardDetail_collection.insert_one(ward_data)

    return Response({'message': 'Ward added successfully'})

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

    ### Email already exists
    query = {"email": email}
    result = UserAuth_collection.find_one(query)
    if result:
        return Response({'error': 'Email'})
    
    ### Add doctor to 'User-Doctor' Collection
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
    UserDoctor_collection.insert_one(doctor_data)

    ### Add doctor to 'UserAuth' Collection
    UserAuth_Doctor = {
        'email':email,
        'password': password,
        'type': 'Doctor',
        'name': fullName,
    }
    UserAuth_collection.insert_one(UserAuth_Doctor)

    ### Update 'WardDetails' Collection
    query = {
        "wardNumber": wardNumber
    }
    document = WardDetail_collection.find_one(query)

    if document:
        document['Doctors'].append(email)
        document['NoOfDoctors'] += 1
        
        WardDetail_collection.update_one(query, {"$set": document})

        print("Updated Document:", document)
    else:
        print("Document not found")
        return Response({'message': 'WardDetails Collection Cannot find.'})

    return Response({'message': 'Doctor cadded successfully'})

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

    ### Email already exists
    query = {"email": email}
    result = UserAuth_collection.find_one(query)
    if result:
        return Response({'error': 'Email'})
    
    ### Add doctor to 'User-Consultant' Collection
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
    UserConsultant_collection.insert_one(consultant_data)

    ### Add doctor to 'UserAuth' Collection
    UserAuth_Consultant = {
        'email':email,
        'password': password,
        'type': 'Consultant',
        'name': fullName,
    }
    UserAuth_collection.insert_one(UserAuth_Consultant)

    return Response({'message': 'Consultant added successfully'})

@api_view(['POST'])
def changeData(request):
    ##### Not Completed Yet #####
    mobileNo = request.data.get('Mobile')
    email = (request.data.get('Email'))
    address = (request.data.get('Address'))
    info = (request.data.get('Information'))

    if request.data['Position'] == "Admin":
        print('add data to admin collection')
    elif request.data['Position'] == "Doctor":
        print('add data to doctor collection')
    elif request.data['Position'] == "Consultant":
        print('add data to consultant collection')
    
    return Response({'message': 'Data changed successfully'})

##### Doctor views #####

@api_view(['POST'])
def getShiftOptions(request):

    if request.data['type'] != "Doctor":
        return JsonResponse({'message': 'Invalid user type', 'status': 'error'})

    # find ward number of the doctor
    projection = {'wardNumber': 1,'_id':0}
    ward = UserDoctor_collection.find_one({'email':request.data['email']}, projection)

    # find number of shifts of the ward
    projection = {'Shifts': 1,'_id':0}
    shifts = WardDetail_collection.find_one(ward, projection)

    if shifts['Shifts'] == 2:
        return JsonResponse({'shifts': ['morning','night']})
    elif shifts['Shifts'] == 3:
        return JsonResponse({'shifts': ['morning','evening','night']})
    else:
        return JsonResponse({'message': 'Invalid number of shifts', 'status': 'error'})

@api_view(['POST'])
def sendWardDetails(request):
    projection = {'wardName': 1, 'wardNumber': 1}
    ward_details = [{'wardName': i['wardName'], 'wardNumber': i['wardNumber']} for i in WardDetail_collection.find({}, projection)]
    if ward_details:
        return Response(ward_details)
    else:
        return JsonResponse(None)

@api_view(['POST'])
def getScheduleForDoctor(request):

    #print(request.data)
    Schedule_collection = db['TimeTable-Doctor']
    projection = {'shifts': 1, '_id':0, 'wardID':1,'wardName':1,'numOfShifts':1}
    Schedule_details = Schedule_collection.find_one({'email':request.data['email'], 'y-m': request.data['ym']}, projection)

    if Schedule_details:
        pass
    else:
        print('Doctor schedule not found in database')
        return JsonResponse({'message': 'No schedule found'})

    result = dict()
    result['topic'] = Schedule_details['wardID']+' | '+Schedule_details['wardName']
    result['schedule'] = []
    
    for i in Schedule_details['shifts']:
        for time in i['time']:
            new = dict()
            new['Subject'] = Schedule_details['wardID']+' | '+Schedule_details['wardName']+" | "+time

            if Schedule_details['numOfShifts'] == 3:
                if time == 'morning':
                    new['StartTime'] = request.data['ym']+'-'+i['date']+'T07:00'
                    new['EndTime'] = request.data['ym']+'-'+i['date']+'T13:30'
                elif time == 'evening':
                    new['StartTime'] = request.data['ym']+'-'+i['date']+'T13:30'
                    new['EndTime'] = request.data['ym']+'-'+i['date']+'T20:00'
                elif time == 'night':
                    new['StartTime'] = request.data['ym']+'-'+i['date']+'T20:00'
                    new['EndTime'] = request.data['ym']+'-'+str(int(i['date'])+1)+'T07:00'

            elif Schedule_details['numOfShifts'] == 2:
                if time == 'morning':
                    new['StartTime'] = request.data['ym']+'-'+i['date']+'T08:00'
                    new['EndTime'] = request.data['ym']+'-'+i['date']+'T16:30'
                elif time == 'night':
                    new['StartTime'] = request.data['ym']+'-'+i['date']+'T16:30'
                    new['EndTime'] = request.data['ym']+'-'+str(int(i['date'])+1)+'T08:00'
            
            result['schedule'].append(new)        

    print("num of shifts = ",len(result['schedule']))
    if result:
        print('Doctor schedule found')
        return JsonResponse(result)
    else:
        print('Doctor schedule not found')
        return JsonResponse({'message': 'No schedule found'}, status=404)

@api_view(['POST'])
def docLeaveReq(request):
    
    if request.data['type'] != "Doctor":
        return JsonResponse({'message': 'Invalid user type', 'status': 'error'})
    
    # find doctor name and wardnumber of the doctor
    projection = {'wardNumber': 1,'name':1,'_id':0}
    docDetails = UserDoctor_collection.find_one({'email':request.data['email']}, projection)

    leave_req_document = {
    'email': request.data['email'], 
    "Name": docDetails['name'],
    'FromDate': request.data['fromDate'],
    'FromShift': request.data['fromShift'],
    'ToDate': request.data['toDate'],
    'ToShift': request.data['toShift'],
    'Reason': request.data['reason'],
    "Status": "NoResponse",
    "wardNumber": docDetails['wardNumber'],

    "Date": "temp",
    "FromTime": "temp",
    "ToTime": "temp",
    }
    

    # Insert the document into the collection
    LeaveRequests_collection.insert_one(leave_req_document)

    return JsonResponse({'message': 'Leave request sent successfully',  'status': 'success'})


@api_view(['POST'])
def docLeaveReqHistory(request):

    query_conditions = [
        {'Status': "Accepted", 'email': request.data['email']},
        {'Status': "Rejected", 'email': request.data['email']},
    ]
    if request.data['type'] != "Doctor":
        return JsonResponse(None, safe=False)
    
    result = dict()
    result['historyDetails'] = []
    
    for condition in query_conditions:

        documents = [{'email': i['email'], 
                        'Name': i['Name'],
                        "FromDate":i["FromDate"], 
                        "FromShift":i["FromShift"], 
                        "ToDate":i["ToDate"], 
                        "ToShift":i["ToShift"], 
                        "Reason": i["Reason"],
                        "Status": i["Status"],
                        "wardNumber": i["Status"],
                        } for i in LeaveRequests_collection.find(condition, {'_id':0})]



        result['historyDetails'].append(documents)
        result['historyDetails'] = [item for sublist in result['historyDetails'] for item in (sublist if isinstance(sublist, list) else [sublist])]
    
    return JsonResponse(result)

##### Consultant views #####
@api_view(['POST'])
def consViewDoctors(request):
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
                return JsonResponse({'message': 'No doctors found in the same ward'})
        else:
            return JsonResponse({'message': 'Consultant not found'}, status=404)
    
    return JsonResponse({'message': 'Invalid user type'}, status=400)

@api_view(['POST'])
def conViwAllDocDetails(request):
    user_type = request.data.get('type')
    email = request.data.get('email')

    if user_type == "Consultant":
        consultant = UserConsultant_collection.find_one({'email': email},{'wardNumber':1})

        if consultant:
            ward_number = consultant['wardNumber']
            doctors_in_wards = list(UserDoctor_collection.find({'wardNumber': ward_number},{'_id':0}))
            
            if doctors_in_wards:
                return Response(doctors_in_wards)
            else:
                return JsonResponse({'message': 'No doctors found in this ward'})
        else:
            return JsonResponse({'message': 'Consultant not found'})
    
    return JsonResponse({'message': 'Invalid user type'})   


@api_view(['POST'])
def conViwAllConDetails(request):
    user_type = request.data.get('type')
    email = request.data.get('email')

    if user_type == "Consultant":
        consultant = UserConsultant_collection.find_one({'email': email},{'wardNumber':1})

        if consultant:
            ward_number = consultant['wardNumber']
            con_in_wards = list(UserConsultant_collection.find({'wardNumber': ward_number},{'_id':0}))
            
            if con_in_wards:
                return Response(con_in_wards)
            else:
                return JsonResponse({'message': 'No consultants found in this ward'})
        else:
            return JsonResponse({'message': 'Consultant not found'})
    
    return JsonResponse({'message': 'Invalid user type'})   

@api_view(['POST'])
def consViewConsultants(request):
    user_type = request.data.get('type')
    email = request.data.get('email')

    if user_type == "Consultant":
        consultant = UserConsultant_collection.find_one({'email': email})
        
        if consultant:
            ward_number = consultant.get('wardNumber')
            doctors_in_wards = list(UserConsultant_collection.find({'wardNumber': ward_number}, projection={'_id': 0, 'img': 1, 'name': 1, 'position': 1}))
            
            if doctors_in_wards:
                return Response(doctors_in_wards)
            else:
                return JsonResponse({'message': 'No doctors found in the same ward'})
        else:
            return JsonResponse({'message': 'Consultant not found'}, status=404)
    
    return JsonResponse({'message': 'Invalid user type'}, status=400)

@api_view(['POST'])
def getScheduleForWard(request):
    
    Ward = db['User-Consultant']
    projection = {'wardNumber': 1, '_id':0}
    Ward = Ward.find_one({'email':request.data['email']}, projection)


    doctor_details = db['WardDetails']
    projection = {'_id':0, 'Doctors':1,'wardName':1}
    doctor_details = doctor_details.find_one({'wardNumber':Ward['wardNumber']}, projection)

    result = dict()
    result['wardName'] = doctor_details['wardName']
    result['schedule'] = []
    schedule_details = db['TimeTable-Doctor']
    projection = {'_id':0, 'shifts':1,'name':1,'numOfShifts':1}
    for doctor in doctor_details['Doctors']:
        schedule_detail = schedule_details.find_one({'email':doctor, 'y-m': request.data['ym']}, projection)

        if schedule_detail:
            new = dict()
            
            for i in schedule_detail['shifts']:
                for time in i['time']:
                    new = dict()
                    new['Subject'] = schedule_detail['name']+" | "+time


                    if schedule_detail['numOfShifts'] == 3:
                        if time == 'morning':
                            new['StartTime'] = request.data['ym']+'-'+i['date']+'T07:00'
                            new['EndTime'] = request.data['ym']+'-'+i['date']+'T13:30'
                        elif time == 'evening':
                            new['StartTime'] = request.data['ym']+'-'+i['date']+'T13:30'
                            new['EndTime'] = request.data['ym']+'-'+i['date']+'T20:00'
                        elif time == 'night':
                            new['StartTime'] = request.data['ym']+'-'+i['date']+'T20:00'
                            new['EndTime'] = request.data['ym']+'-'+str(int(i['date'])+1)+'T07:00'

                    elif schedule_detail['numOfShifts'] == 2:
                        if time == 'morning':
                            new['StartTime'] = request.data['ym']+'-'+i['date']+'T08:00'
                            new['EndTime'] = request.data['ym']+'-'+i['date']+'T16:30'
                        elif time == 'night':
                            new['StartTime'] = request.data['ym']+'-'+i['date']+'T16:30'
                            new['EndTime'] = request.data['ym']+'-'+str(int(i['date'])+1)+'T08:00'
                    
                    result['schedule'].append(new)
    
    if result:
        print('Doctor schedule found')
        return JsonResponse(result)
    else:
        print('Doctor schedule not found')
        return JsonResponse({'message': 'No schedule found'}, status=404)

@api_view(['POST'])
def leaveResponse(request):

    ### Update 'LeaveRequests' Collection
    query = {
        "Status": "NoResponse",
        "Name": request.data["name"],
        "FromDate": request.data["fromDate"],
        "FromShift": request.data["fromShift"],
        "ToDate": request.data["toDate"],
        "ToShift": request.data["toShift"],
    }
    document = LeaveRequests_collection.find_one(query)

    if document:
        document['Status'] = request.data["status"]
        LeaveRequests_collection.update_one(query, {"$set": document})
        #print("Updated Document:", document)
    else:
        print("Document not found")
        return Response({'message': 'LeaveRequests Collection Cannot find.'})

    return JsonResponse({'message': 'Leave response saved successfully'})

@api_view(['POST'])
def leaveRequests(request):

    query_conditions = [
        {'Status': "Accepted"},
        {'Status': "Rejected"},
    ]
    if request.data['type'] == "Consultant":
        consultant_collection = UserConsultant_collection

    current_consultant = consultant_collection.find_one({'email': request.data['email']})
    if current_consultant:
        ward_numbers = [current_consultant.get('wardNumber', [])]
    
    result = dict()
    result['historyDetails'] = []
    result['reqDetails'] = []
    
    for condition in query_conditions:
        # Use list comprehension to convert ObjectId to string
        documents = list(LeaveRequests_collection.find({'wardNumber': {'$in': ward_numbers}, **condition}))
        converted_documents = [
            {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()} 
            for doc in documents
        ]
        result['historyDetails'].append(converted_documents)
        result['historyDetails'] = [item for sublist in result['historyDetails'] for item in (sublist if isinstance(sublist, list) else [sublist])]

    # pending leave requests
    condition = {'Status': "NoResponse"}
    documents = list(LeaveRequests_collection.find({'wardNumber': {'$in': ward_numbers}, **condition}))
    converted_documents = [
        {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()} 
        for doc in documents
    ]
    result['reqDetails'].append(converted_documents)
    result['reqDetails'] = [item for sublist in result['reqDetails'] for item in (sublist if isinstance(sublist, list) else [sublist])]

    if any(result):
        return JsonResponse(result)
    else:
        return JsonResponse(None, safe=False)
   
##### All users views #####

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
    
    