from django.urls import path
from . import views

urlpatterns = [
    
    path('view_profile', views.view_profile, name='view_profile') ,
    path('changeData', views.changeData, name='changeData') ,

    # Admin
    path('wardDetails', views.wardDetails, name='wardDetails') ,
    path('doctorDetails', views.doctorDetails, name='doctorDetails') ,
    path('consultantDetails', views.consultantDetails, name='consultantDetails') ,
    path('addWard', views.addWard, name='addWard') ,
    path('addDoctor', views.addDoctor, name='addDoctor') ,
    path('addConsultant', views.addConsultant, name='addConsultant') ,

    path('sendWardDetails', views.sendWardDetails, name='sendWardDetails') ,
    # Doctor
    path('getScheduleForDoctor', views.getScheduleForDoctor, name='getScheduleForDoctor') ,


    # Consultant
    path('consViewDoctors', views.consViewDoctors, name='consViewDoctors') ,
    path('consViewConsultants', views.consViewConsultants, name='consViewConsultants') ,
    path('getScheduleForWard', views.getScheduleForWard, name='getScheduleForWard') ,
    path('leaveReqDetails', views.leaveRequests, name='leaveReqDetails') ,
    path('leaveResponse', views.leaveResponse, name='leaveResponse') ,
]