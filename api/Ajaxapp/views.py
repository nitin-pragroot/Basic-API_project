from django.http import HttpResponse
from django.shortcuts import render
from .models import employee
# Create your views here.
def insertemp(request):
    return render(request,"ajaxdemo.html")

def addemp(request):
    print('hi')
    no=request.GET.get('eno')
    address=request.GET.get('address')
    name=request.GET.get('name')
    sal=request.GET.get('salary')
    obj=employee.objects.create( eno=no,eaddr=address,ename=name,esal=sal)
    obj.save()
    return HttpResponse("Record submitted successfully")