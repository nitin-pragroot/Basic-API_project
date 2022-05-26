from django.urls import path
from .import views
urlpatterns = [
    path("news/",views.news,name="news"),
    path('stats', views.covidstats, name="stats"),
    path('flipkartdata', views.flipkartdata, name="flipkartdata"),
    path('emp_data_view', views.emp_data_view, name="emp_data_view"),
    path('emp_data_view2', views.emp_data_view2, name="emp_data_view2"),
    path('emp_data_view3', views.emp_data_view3, name="emp_data_view3"),
    path('jsoncbv', views.jsonCBV.as_view()),
    #path('employeedetailCBV/<int:id>', views.employeedetailCBV.as_view()),
    path('employeedetailCBV', views.employeedetailCBV.as_view()),

]