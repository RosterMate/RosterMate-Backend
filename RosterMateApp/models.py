from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=30)
    NIC = models.CharField(max_length=12)
    password = models.CharField(max_length=15)
    wardID = models.IntegerField()
    mobileNumber = models.IntegerField()
