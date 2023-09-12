from django.urls import path
from . import views

# Correct the variable name to "urlpatterns"
urlpatterns = [
    path('hello/', views.say_hello,name="index"),
    path('add/<int:a>/<int:b>', views.add,name="add"),
    path('intro/<str:a>/<int:b>', views.intro,name="intro"),
    path('myfirstpage', views.myfirstpage,name="myfirstpage"),
    path('mysecondpage', views.mysecondpage,name="mysecondpage")
]
