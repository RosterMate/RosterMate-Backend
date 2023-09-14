#from django.db import models

# Create your models here.
from djongo import models

class WardDetails(models.Model):
    _id = models.ObjectIdField()
    wardName = models.CharField(max_length=255)
    wardNumber = models.CharField(max_length=10)
    Shifts = models.IntegerField()
    ConsecutiveShifts = models.IntegerField()
    NoOfDoctors = models.IntegerField()

    meta = {
        'collection': 'WardDetails',  # Specify the MongoDB collection name
    }
    