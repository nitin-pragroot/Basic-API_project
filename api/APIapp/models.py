from django.db import models

# Create your models here.
class Student(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    rollno = models.IntegerField(max_length=50)
    addr = models.CharField(max_length=50)

    def __str__(self):
        return self.fname