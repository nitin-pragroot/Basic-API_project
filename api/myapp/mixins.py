import json
from django.core.serializers import serialize
from django.http import HttpResponse


class SerializerMixin:
    def render_to_http_response(self,jsondata,status=200):
        return HttpResponse(jsondata, content_type='application/json')

    def serialize(self,obj):
        jsondata = serialize('json', obj)
        p_data=json.loads(jsondata) #json to dictionay
        final_list=[]
        for obj in p_data:
            empdata=obj['fields']
            final_list.append(empdata)
        jsondata=json.dumps(final_list)
        return jsondata