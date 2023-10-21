from django.db import models
from database_Connection import db

# Create your models here.

##### All Users #####
LeaveRequests_collection = db['LeaveRequests']
WardDetail_collection = db['WardDetails']
UserAuth_collection = db['UserAuth']
TimeTable_collection = db['TimeTable-Doctor']
ScheduledMonths_collection = db['Scheduled-months']

##### Doctor #####
UserDoctor_collection =db['User-Doctor']

##### Consultant #####
UserConsultant_collection =db['User-Consultant']

##### Admin #####
UserAdmin_collection = db['User-Admin']
