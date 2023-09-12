from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
def say_hello(request):
    return HttpResponse('Hello World!')

def add(request,a,b):
    return HttpResponse(a+b)

def intro(request,a,b):
    data = {
        'name': a,
        'age': b
    }
    return JsonResponse(data)

def myfirstpage(request):
    return render(request,'index.html')

def mysecondpage(request):
    return render(request,'second.html')