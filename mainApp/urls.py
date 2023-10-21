from django.urls import path
from . import views

urlpatterns = [

    # All users
    path('view_profile', views.view_profile, name='view_profile') ,
    path('changeData', views.changeData, name='changeData') ,

    # Admin
    path('wardDetails', views.wardDetails, name='wardDetails') ,
    path('doctorDetails', views.doctorDetails, name='doctorDetails') ,
    path('consultantDetails', views.consultantDetails, name='consultantDetails') ,
    path('addWard', views.addWard, name='addWard') ,
    path('addDoctor', views.addDoctor, name='addDoctor') ,
    path('addConsultant', views.addConsultant, name='addConsultant') ,
    path('adminViwAllDocDetails', views.adminViwAllDocDetails, name='adminViwAllDocDetails') ,
    path('adminViwAllConDetails', views.adminViwAllConDetails, name='adminViwAllConDetails') ,

    # Doctor
    path('getScheduleForDoctor', views.getScheduleForDoctor, name='getScheduleForDoctor') ,
    path('docLeaveReqHistory', views.docLeaveReqHistory, name='docLeaveReqHistory') ,
    path('docLeaveReq', views.docLeaveReq, name='docLeaveReq') ,
    path('getShiftOptions', views.getShiftOptions, name='getShiftOptions') ,
    path('sendWardDetails', views.sendWardDetails, name='sendWardDetails') ,

    # Consultant
    path('consViewDoctors', views.consViewDoctors, name='consViewDoctors') ,
    path('consViewConsultants', views.consViewConsultants, name='consViewConsultants') ,
    path('getScheduleForWard', views.getScheduleForWard, name='getScheduleForWard') ,
    path('leaveReqDetails', views.leaveRequests, name='leaveReqDetails') ,
    path('leaveResponse', views.leaveResponse, name='leaveResponse') ,
    path('conViwAllDocDetails', views.conViwAllDocDetails, name='conViwAllDocDetails') ,
    path('conViwAllConDetails', views.conViwAllConDetails, name='conViwAllConDetails') ,
    path('createSchedule', views.createSchedule, name='createSchedule') ,
    path('getScheduleConstraints', views.getScheduleConstraints, name='getScheduleConstraints') ,
]