from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from bson import ObjectId

from .models import *
from Scheduler import Scheduler


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
    ward_details = []
    projection = {'wardName': 1, 'NoOfDoctors': 1, 'wardNumber': 1, 'Doctors': 1}
    wards = WardDetail_collection.find({}, projection)
    
    for ward in wards:
        ward_data = {
            'wardName': ward['wardName'],
            'NoOfDoctors': ward['NoOfDoctors'],
            'wardNumber': ward['wardNumber'],
            'Doctors': []
        }

        if 'Doctors' in ward and isinstance(ward['Doctors'], list):
            for doctor_email in ward['Doctors']:
                # Query your userDoctor collection to find the doctor name by email
                doctor = UserDoctor_collection.find_one({'email': doctor_email})
                if doctor:
                    ward_data['Doctors'].append(doctor['name'])

        ward_details.append(ward_data)
    if ward_details:
        return Response(ward_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def doctorDetails(request):
    
    projection = {'name': 1, 'position': 1,'img':1,'email':1,'address':1,'wardNumber':1,'Degree':1,'mobile':1}
    doctor_details = [{'name': i['name'], 'position': i['position'],'img':i['img'],'email':i['email'],'address':i['address'],'wardNumber':i['wardNumber'],'Degree':i['Degree'],'mobile':i['mobile']} for i in UserDoctor_collection.find({}, projection)]

    if doctor_details:
        return Response(doctor_details)
    else:
        return JsonResponse(None)
    
@api_view(['POST'])
def consultantDetails(request):

    projection = {'name': 1, 'position': 1,'img':1,'email':1,'address':1,'wardNumber':1,'Degree':1,'mobile':1}
    consultant_details = [{'name': i['name'], 'position': i['position'],'img':i['img'],'email':i['email'],'address':i['address'],'wardNumber':i['wardNumber'],'Degree':i['Degree'],'mobile':i['mobile']} for i in UserConsultant_collection.find({}, projection)]

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

    result = dict()
    result['schedule'] = []

    yearMonth = request.data['ym'].split('-')
    month = str(int(yearMonth[1])-1)
    if len(month) == 1:
        month = '0'+month
    yearMonth = yearMonth[0]+'-'+ month

    #print(request.data)
    for _ in range(2):
        yearMonth = request.data['ym'].split('-')
        yearMonth = yearMonth[0]+'-'+ month
        yearMonth = yearMonth.split('-')
        month = str(int(yearMonth[1])+1)
        if len(month) == 1:
            month = '0'+month
        yearMonth = yearMonth[0]+'-'+ month
        
        projection = {'shifts': 1, '_id':0, 'wardID':1,'wardName':1,'numOfShifts':1}
        Schedule_details = TimeTable_collection.find_one({'email':request.data['email'], 'y-m': yearMonth}, projection)

        if Schedule_details:
            pass
        else:
            continue
        
        result['topic'] = Schedule_details['wardID']+' | '+Schedule_details['wardName']

        for i in Schedule_details['shifts']:
            for time in i['time']:
                new = dict()
                new['Subject'] = Schedule_details['wardID']+' | '+Schedule_details['wardName']+" | "+time

                if Schedule_details['numOfShifts'] == 3:
                    if time == 'morning':
                        new['StartTime'] = yearMonth+'-'+i['date']+'T07:00'
                        new['EndTime'] = yearMonth+'-'+i['date']+'T13:30'
                    elif time == 'evening':
                        new['StartTime'] = yearMonth+'-'+i['date']+'T13:30'
                        new['EndTime'] = yearMonth+'-'+i['date']+'T20:00'
                    elif time == 'night':
                        new['StartTime'] = yearMonth+'-'+i['date']+'T20:00'
                        new['EndTime'] = yearMonth+'-'+str(int(i['date'])+1)+'T07:00'

                elif Schedule_details['numOfShifts'] == 2:
                    if time == 'morning':
                        new['StartTime'] = yearMonth+'-'+i['date']+'T08:00'
                        new['EndTime'] = yearMonth+'-'+i['date']+'T16:30'
                    elif time == 'night':
                        new['StartTime'] = yearMonth+'-'+i['date']+'T16:30'
                        new['EndTime'] = yearMonth+'-'+str(int(i['date'])+1)+'T08:00'
                
                result['schedule'].append(new)   
         
    if result:
        print('Doctor schedule found')
        return JsonResponse(result)
    else:
        print('Doctor schedule not found')
        return JsonResponse({'message': 'No schedule found','status':'error'}, )

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
            doctors_in_wards = list(UserDoctor_collection.find({'wardNumber': ward_number}, {'_id': 0, 'img': 1, 'name': 1, 'position': 1,'email':1,'address':1,'wardNumber':1,'Degree':1,'mobile':1}))
            
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
            doctors_in_wards = list(UserConsultant_collection.find({'wardNumber': ward_number}, projection={'_id': 0, 'img': 1, 'name': 1, 'position': 1,'email':1,'address':1,'wardNumber':1,'Degree':1,'mobile':1}))

            if doctors_in_wards:
                return Response(doctors_in_wards)
            else:
                return JsonResponse({'message': 'No doctors found in the same ward'})
        else:
            return JsonResponse({'message': 'Consultant not found'}, status=404)
    
    return JsonResponse({'message': 'Invalid user type'}, status=400)

@api_view(['POST'])
def getScheduleForWard(request):
    
    projection = {'wardNumber': 1, '_id':0}
    Ward = UserConsultant_collection.find_one({'email':request.data['email']}, projection)

    projection = {'_id':0, 'Doctors':1,'wardName':1}
    doctor_details = WardDetail_collection.find_one({'wardNumber':Ward['wardNumber']}, projection)

    result = dict()
    result['wardName'] = doctor_details['wardName']
    result['schedule'] = []
    projection = {'_id':0, 'shifts':1,'name':1,'numOfShifts':1}

    yearMonth = request.data['ym'].split('-')
    month = str(int(yearMonth[1])-1)
    if len(month) == 1:
        month = '0'+month
    yearMonth = yearMonth[0]+'-'+ month
    for _ in range(2):
        yearMonth = yearMonth.split('-')
        month = str(int(yearMonth[1])+1)
        if len(month) == 1:
            month = '0'+month
        yearMonth = yearMonth[0]+'-'+ month

        for doctor in doctor_details['Doctors']:
            schedule_detail = TimeTable_collection.find_one({'email':doctor, 'y-m': yearMonth}, projection)

            if schedule_detail:
                new = dict()
                
                for i in schedule_detail['shifts']:
                    for time in i['time']:
                        new = dict()
                        new['Subject'] = schedule_detail['name']+" | "+time


                        if schedule_detail['numOfShifts'] == 3:
                            if time == 'morning':
                                new['StartTime'] = yearMonth+'-'+i['date']+'T07:00'
                                new['EndTime'] = yearMonth+'-'+i['date']+'T13:30'
                            elif time == 'evening':
                                new['StartTime'] = yearMonth+'-'+i['date']+'T13:30'
                                new['EndTime'] = yearMonth+'-'+i['date']+'T20:00'
                            elif time == 'night':
                                new['StartTime'] = yearMonth+'-'+i['date']+'T20:00'
                                new['EndTime'] = yearMonth+'-'+str(int(i['date'])+1)+'T07:00'

                        elif schedule_detail['numOfShifts'] == 2:
                            if time == 'morning':
                                new['StartTime'] = yearMonth+'-'+i['date']+'T08:00'
                                new['EndTime'] = yearMonth+'-'+i['date']+'T16:30'
                            elif time == 'night':
                                new['StartTime'] = yearMonth+'-'+i['date']+'T16:30'
                                new['EndTime'] = yearMonth+'-'+str(int(i['date'])+1)+'T08:00'
                        
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

@api_view(['POST'])
def getScheduleConstraints(request):
    
    email = request.data.get('email')
    wardNumber = UserConsultant_collection.find_one({'email': email},{'wardNumber':1})['wardNumber']
    ward = WardDetail_collection.find_one({'wardNumber': wardNumber},{'NoOfDoctors':1,'wardName':1,'_id':0})

    if ward:
        return JsonResponse(ward)
    
    return JsonResponse(None, safe=False)

@api_view(['POST'])
def createSchedule(request):

    user_type = request.data.get('type')
    email = request.data.get('email')

    # get doctors IDs and names in the same ward
    if user_type == "Consultant":
        consultant = UserConsultant_collection.find_one({'email': email})
        
        if consultant:
            ward_number = consultant.get('wardNumber')
            doctors_in_ward = {i['email']:i['name'] for i in  list(UserDoctor_collection.find({'wardNumber': ward_number},{'_id': 0, 'name': 1,'email':1}))}
        else:
            return JsonResponse({'message': 'Consultant not found', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid user type', 'status': 'error'})



    if request.data['form']['shifts'] == '2':
        shift_types = ["morning", "night"]
        num_doctors = {"morning": int(request.data['form']['number1']), "night": int(request.data['form']['number3'])}
    elif request.data['form']['shifts'] == '3':
        shift_types = ["morning", "evening", "night"]
        num_doctors = {"morning": int(request.data['form']['number1']), "evening": int(request.data['form']['number2']), "night": int(request.data['form']['number3'])}
    else:
        return JsonResponse({'message': 'shift_types error'  , 'status': 'error'})
    
    consecutive_shifts = int(request.data['form']['consecutiveShifts'])
    year = int(request.data['month'][:4])
    month = int(request.data['month'][5:7])+1

    leaves = list(LeaveRequests_collection.find({'wardNumber': ward_number,'Status':"Accepted"},{'_id': 0, 'name': 1,'email':1,"FromDate":1,"FromShift":1,"ToDate":1,"ToShift":1}))
    ward_name = WardDetail_collection.find_one({'wardNumber': ward_number},{'_id':0,'wardName':1})['wardName']

    doctors_details = [[i] for i in doctors_in_ward]

    #print(doctors_details)
    #print(leaves)

    str_month = str(month)
    if len(str_month) == 1:
        str_month = '0'+str_month

    ##### check if schedule already created #####
    isScheduled = ScheduledMonths_collection.find_one({'wardID': ward_number,"y-m": str(year)+"-"+str_month},{})
    if isScheduled:
        print('Schedule already created. Deleting old schedule...')
        TimeTable_collection.delete_many({'wardID': ward_number,"y-m": str(year)+"-"+str_month})
        ScheduledMonths_collection.delete_one({'wardID': ward_number,"y-m": str(year)+"-"+str_month})
        #return JsonResponse({'message': 'Schedule already created.',  'status': 'error'})
    
    for leave in leaves:
        date1 = leave['FromDate'].split('-')
        date2 = leave['ToDate'].split('-')

        if date1[1] != str_month:
            continue
        
        if request.data['form']['shifts'] == '2':
            if leave['FromShift'] == 'evening':
                leave['FromShift'] = 'morning'
            if leave['ToShift'] == 'evening':
                leave['ToShift'] = 'morning'
        for i in doctors_details:
            if i[0] == leave['email']:
                i.append([date1[0]+'-'+date1[1]+"-"+date1[2],leave['FromShift']])
                while date1[2] != date2[2] or leave['FromShift'] != leave['ToShift']:

                    if request.data['form']['shifts'] == '3':
                        if leave['FromShift'] == "morning":
                            leave['FromShift'] = "evening"
                        elif leave['FromShift'] == "evening":
                            leave['FromShift'] = "night"
                        else:
                            leave['FromShift'] = "morning"
                            date1[2] = str(int(date1[2])+1)
                            if len(date1[2]) == 1:
                                date1[2] = '0'+date1[2]
                    else:
                        if leave['FromShift'] == "morning":
                            leave['FromShift'] = "night"
                        else:
                            leave['FromShift'] = "morning"
                            date1[2] = str(int(date1[2])+1)
                            if len(date1[2]) == 1:
                                date1[2] = '0'+date1[2]

                    i.append([date1[0]+'-'+date1[1]+"-"+date1[2],leave['FromShift']])
                break
    
    scheduler = Scheduler(doctors_details, shift_types, num_doctors,consecutive_shifts, year, month)
    schedule = scheduler.get_schedule_with_equal_shifts()

    #print(schedule)

    ##### insert schedule to database #####
    for doc in doctors_in_ward:

        document = {
            "email": doc,
            "wardID": ward_number,
            "wardName": ward_name,
            "name": doctors_in_ward[doc],
            "y-m": str(year)+"-"+str_month,
            "shifts": [],
            "numOfShifts": int(request.data['form']['shifts'])
        }

        for temp in schedule[doc]:
            d = temp[0].split('-')[-1]
            if len(d) == 1:
                d = '0'+d
            document['shifts'].append({"date":d,"time":[temp[1]]})
        
        TimeTable_collection.insert_one(document)
    
    ##### insert scheduled month to database #####
    document = {
        "wardID": ward_number,
        "y-m": str(year)+"-"+str_month
    }
    ScheduledMonths_collection.insert_one(document)
    print('Schedule created successfully')
    return JsonResponse({'message': 'Schedule created successfully',  'status': 'success'})

##### All users views #####

@api_view(['POST'])
def view_profile(request):

    if request.data['type'] == "Admin":
        profile_details_collection = UserAdmin_collection
    elif request.data['type'] == "Doctor":
        profile_details_collection = UserDoctor_collection
    elif request.data['type'] == "Consultant":
        profile_details_collection = UserConsultant_collection

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
    
    