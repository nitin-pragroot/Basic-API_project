from django.urls import path
from .import views
urlpatterns = [
    path('insertemp', views.insertemp, name="insertemp"),
    path('addemp', views.addemp, name="addemp"),

]