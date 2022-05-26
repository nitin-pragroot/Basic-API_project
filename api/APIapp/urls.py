from django.urls import path
from .import views
urlpatterns = [
    path('stu_view', views.stu_view, name="stu_view"),
    path('stu_view2', views.stu_view2, name="stu_view2"),
    path('stu_view3', views.stu_view3, name="stu_view3"),
    path('jsondata',views.jsonData.as_view()),
   # path('studentdetail/<int:id>',views.studentdetail.as_view()),
    path('studentdetail',views.studentdetail.as_view()),
]