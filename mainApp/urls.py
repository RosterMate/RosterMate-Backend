from django.urls import path
from . import views


urlpatterns = [
    path('wardDetails', views.wardDetails, name='wardDetails'),
    path('doctorDetails', views.doctorDetails, name='doctorDetails'),
    path('consultantDetails', views.consultantDetails, name='consultantDetails'),
    path('view_profile', views.view_profile, name='view_profile'),
]