import json

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .forms import studentform
from .mixs import SerializerMixs
from .models import Student
from django.views.decorators.csrf import csrf_exempt


def stu_view(request):
    data={
        'fname':'Sumit',
        'lname':'saini',
        'rollno':1011,
        'addr':'Panchkula'
    }
    resp='rollno:'+str(data['rollno'])+'<br/> fname:'+data['fname']+'<br/> lname:'+data['lname']+'<br/> addr:'+data['addr']
    return HttpResponse(resp)

def stu_view2(request):
    data={
        'fname':'Sumit',
        'lname':'saini',
        'rollno':1011,
        'addr':'Panchkula'
    }
    jsondata=json.dumps(data)
    return HttpResponse(jsondata,content_type='application/json')

def stu_view3(request):
    data={
        'fname': 'Sumit',
        'lname': 'saini',
        'rollno': 1011,
        'addr': 'Panchkula'
    }
    return JsonResponse(data)

@method_decorator(csrf_exempt,name='dispatch')
class jsonData(View):
    def get(self,request):
        jsondata=json.dumps({'msg':'this is get method'})
        return HttpResponse(jsondata, content_type='application/json')

    def put(self,request):
        jsondata=json.dumps({'msg':'this is put method'})
        return HttpResponse(jsondata, content_type='application/json')

    def post(self,request):
        jsondata=json.dumps({'msg':'this is post method'})
        return HttpResponse(jsondata, content_type='application/json')

    def delete(self,request):
        jsondata=json.dumps({'msg':'this is delete method'})
        return HttpResponse(jsondata, content_type='application/json')

@method_decorator(csrf_exempt,name='dispatch')
class studentdetail(View,SerializerMixs):
    """
    def get(self,request,id):
        try:
            stu=Student.objects.get(rollno=id)
        except Student.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
           jsondata=serialize('json',[stu,])
           return HttpResponse(jsondata, content_type='application/json')

    def get(self,request,id):
        try:
            stu = Student.objects.all()
        except Student.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
            jsondata = serialize('json',stu)
            return HttpResponse(jsondata,content_type='application/json')

    def get(self,request):
        try:
            stu = Student.objects.all()
        except Student.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata,content_type='application/json')
        else:
            jsondata = serialize('json',stu)
            p_data=json.loads(jsondata)
            final_list=[]
            for obj in p_data:
                studata = obj['fields']
                final_list.append(studata)
            jsondata=json.dumps(final_list)
            return HttpResponse(jsondata, content_type='application/json')

    def get(self,request):
        try:
            stu = Student.objects.all()
        except Student.DoesNotExist:
            jsondata=json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
            jsondata = self.serialize(stu)
            return HttpResponse(jsondata, content_type='application/json')
    """

@method_decorator(csrf_exempt,name='dispatch')
class studentdetail(View,SerializerMixs):
    def get_object_by_id(self,id):
        try:
            stu=Student.objects.get(rollno=id)
        except Student.DoesNotExist:
            stu=None
        return stu
    def get(self, request):
        try:
            stu = Student.objects.all()
        except Student.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
           jsondata=self.serialize(stu)
           return self.render_to_http_response(jsondata)

    def delete(self, request,id):
        stu = self.get_object_by_id(id)
        if stu is None:
            jsondata=json.dumps({'msg':'No such resource found'})
            return self.render_to_http_response(jsondata)
        status,deleteitem=stu.delete()
        if status==1:
            jsondata=json.dumps({'msg':'Record is successfully'})
            return self.render_to_http_response(jsondata)
        jsondata = json.dumps({'msg': 'Error while deletong data'})
        return self.render_to_http_response(jsondata)

    def put(self,request,id):
        stu = self.get_object_by_id(id)
        if stu is None:
            jsondata=json.dumps({'msg': 'The required resource is not available'})
            return self.render_to_http_response(jsondata,status=400)
        data = request.body
        try:
            provstudata=json.loads(data)
        except ValueError as err:
            jsondata = json.dumps({'msg': 'Please send valid json'})
            return self.render_to_http_response(jsondata, status=400)
        orignaldata={'fname':stu.fname,'lname':stu.lname,'rollno':stu.rollno,'addr':stu.addr}
        orignaldata.update(provstudata)
        form = studentform(orignaldata, instance=stu)
        if form.is_valid():
            form.save(commit=True)
            jsondata = json.dumps({'msg': 'Resource updated successfully'})
            return self.render_to_http_response(jsondata)
        if form.errors:
            jsondata = json.dumps(form.errors)
            return self.render_to_http_response(jsondata, status=400)





