from django.db import models
from database_Connection import db

# Create your models here.

LeaveRequests_collection = db['LeaveRequests']
UserAdmin_collection = db['User-Admin']
UserDoctor_collection =db['User-Doctor']
UserConsultant_collection =db['User-Consultant']
WardDetail_collection = db['WardDetails']
UserAuth_collection = db['UserAuth']
TimeTable_collection = db['TimeTable-Doctor']
