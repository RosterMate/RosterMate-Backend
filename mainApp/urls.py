from django.urls import path
from . import views


urlpatterns = [
    path('wardDetails', views.wardDetails, name='wardDetails'),
    path('doctorDetails', views.doctorDetails, name='doctorDetails'),
    path('consultantDetails', views.consultantDetails, name='consultantDetails'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('addWard', views.addWard, name='addWard'),
    path('leaveReqDetails', views.leaveRequests, name='leaveReqDetails'),
    path('view_All_Users', views.view_all_users, name='view_All_Users'),
    path('addWard', views.addWard, name='addWard'),

]