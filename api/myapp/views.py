import json

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from myapp.forms import employeeform
import requests
import bs4
from bs4 import BeautifulSoup as bs
from .models import employee
from myapp.mixins import SerializerMixin
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def news(request):
    from newsapi import NewsApiClient
    newsapi = NewsApiClient(api_key='6381055e63cf4bac97aead362e4e8ba3')
    top_headlines = newsapi.get_top_headlines(language='en',country='in')
    articles=top_headlines['articles']
    desc=[]
    title=[]
    article_img=[]
    url=[]
    for i in range(len(articles)):
        title.append(articles[i]['title'])
        desc.append(articles[i]['description'])
        article_img.append(articles[i]['urlToImage'])
        url.append(articles[i]['url'])
    news=zip(title,desc,article_img,url)

    return render(request,'news.html',{'news':news})


def covidstats(request):
    url = "https://api.covid19api.com/summary"
    #response = requests.request("GET", url)
    response = requests.get(url)
    #jsondata=response.text
    jsondata=response.json()
    #print(jsondata['Countries'])
    data=jsondata['Countries']
    country = []
    total = []
    confirmed = []
    deaths = []
    cdate = []
    recovered = []
    nrecovered = []
    for i in range(len(data)):
        country.append(data[i]['Country'])
        confirmed.append(data[i]['NewConfirmed'])
        total.append(data[i]['TotalConfirmed'])
        deaths.append(data[i]['NewDeaths'])
        nrecovered.append(data[i]['NewRecovered'])
        recovered.append(data[i]['TotalRecovered'])
        cdate.append(data[i]['Date'])

    cdata = zip(country, confirmed, total, deaths,nrecovered,recovered,cdate)
    return render(request,'stats.html',{'cdata':cdata})


def flipkartdata(request):
    #url = "https://www.flipkart.com/search?q=samsung&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    #url = "https://www.flipkart.com/search?q=samsung&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=2"
    url = "https://www.flipkart.com/search?q=samsung+mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&as-pos=1&as-type=RECENT&suggestionId=samsung+mobiles%7CMobiles&requestId=4039723b-bdc7-40e2-9607-c69a41da4a4b&as-backfill=on&page=3"
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
   # print(soup.prettify())
    results = soup.find_all("div", {"class": "_13oc-S"})
    print(len(results))
    """    
    name = results[0].find('div', class_="_4rR01T").text
    rating = soup.find('div', class_="_3LWZlK").text
    price = soup.find('div', class_="_30jeq3 _1_WHN1").text
    content = soup.find('div', class_="fMghEO").text

    print(name)
    print(rating)
    print(price)
    print(content)
    """

    filename = "fipkartdata.csv"
    f = open(filename, "a")
    headers = "Product name,Price,Rating \n"
    f.write(headers)
    for x in results:
        name = x.find('div', class_="_4rR01T").text
        name = name.replace(",", " ")
        rating = x.find('div', class_="_3LWZlK").text
        price = x.find('div', class_="_30jeq3 _1_WHN1").text
        price = price.replace("₹", "Rs.")
        price = price.replace(",", "")
        f.write(name + "," + price + "," + rating + "\n")
    f.close()
    return render(request, 'flipkartdata.html')

def emp_data_view(request):
    data={
        'eno':100,
        'ename':'Mohan',
        'esal':12000,
        'eaddr':'Panchkula'
    }
    resp='eno:'+str(data['eno'])+'<br/> ename:'+data['ename']+'<br/> esal:'+str(data['esal'])+'<br/> eddr'+data['eaddr']
    return HttpResponse(resp)

def emp_data_view2(request):
    data={
        'eno':100,
        'ename':'Mohan',
        'esal':12000,
        'eaddr':'Panchkula'
    }
    jsondata=json.dumps(data)
    return HttpResponse(jsondata,content_type='application/json')

def emp_data_view3(request):
    data={
        'eno':100,
        'ename':'Mohan',
        'esal':12000,
        'eaddr':'Panchkula'
    }
    return JsonResponse(data)


@method_decorator(csrf_exempt,name='dispatch')
class jsonCBV(View):
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

"""
@method_decorator(csrf_exempt,name='dispatch')
class employeedetailCBV(View,SerializerMixin):
   
    def get(self,request,id):
        try:
            emp=employee.objects.get(eno=id)
        except employee.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
           jsondata=serialize('json',[emp,])
           return HttpResponse(jsondata, content_type='application/json')

    def get(self, request, id):
        try:
            emp = employee.objects.all()
        except employee.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
            jsondata = serialize('json', emp)
            return HttpResponse(jsondata, content_type='application/json')
    def get(self, request, id):
        try:
            emp = employee.objects.all()
        except employee.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
            jsondata = serialize('json', emp)
            p_data=json.loads(jsondata) #json to dictionay
            final_list=[]
            for obj in p_data:
                empdata=obj['fields']
                final_list.append(empdata)
            jsondata=json.dumps(final_list) #convert python format to json
            # jsondata=serialize('json',[emp,])
            return HttpResponse(jsondata, content_type='application/json')
    def get(self, request):
        try:
            emp = employee.objects.all()
        except employee.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
           jsondata=self.serialize(emp)
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
"""
@method_decorator(csrf_exempt,name='dispatch')
class employeedetailCBV(View,SerializerMixin):
    def get_object_by_id(self,id):
        try:
             emp=employee.objects.get(eno=id)
        except employee.DoesNotExist:
             emp=None
        return emp
    def get(self, request):
        try:
            emp = employee.objects.all()
        except employee.DoesNotExist:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return HttpResponse(jsondata, content_type='application/json')
        else:
           jsondata=self.serialize(emp)
           return self.render_to_http_response(jsondata)

    def delete(self, request, id):
        emp=self.get_object_by_id(id)
        if emp is None:
            jsondata=json.dumps({'msg':'No such resource found'})
            return self.render_to_http_response(jsondata)
        status,delitme=emp.delete()
        if status==1:
            jsondata=json.dumps({'msg':'Record Deleted sucessfully'})
            return self.render_to_http_response(jsondata)
        jsondata = json.dumps({'msg': 'Error while deletong data'})
        return self.render_to_http_response(jsondata)

    def put(self,request,id):
        emp=self.get_object_by_id(id)
        if emp is None:
            jsondata = json.dumps({'msg': 'The required resource is not available'})
            return self.render_to_http_response(jsondata, status=400)
        data = request.body
        try:
            pempdata = json.loads(data)
        except ValueError as err:
            jsondata = json.dumps({'msg': 'Please send valid json'})
            return self.render_to_http_response(jsondata, status=400)
        orignaldata={'eno':emp.eno,'ename':emp.ename,'esal':emp.esal,'eaddr':emp.eaddr}
        orignaldata.update(pempdata)
        form = employeeform(orignaldata,instance=emp)
        if form.is_valid():
            form.save(commit=True)
            jsondata = json.dumps({'msg': 'Resource updated successfully'})
            return self.render_to_http_response(jsondata)
        if form.errors:
            jsondata = json.dumps(form.errors)
            return self.render_to_http_response(jsondata, status=400)

    def post(self,request):
        data=request.body
        try:
            empdata=json.loads(data)
        except ValueError as err:
            jsondata=json.dumps({'msg':'Please send valid json'})
            return self.render_to_http_response(jsondata,status=400)
        form=employeeform(empdata)
        if form.is_valid():
            form.save(commit=True)
            jsondata=json.dumps({'msg':'Resource created successfully'})
            return self.render_to_http_response(jsondata)
        if form.errors:
            jsondata=json.dumps(form.errors)
            return self.render_to_http_response(jsondata,status=400)
