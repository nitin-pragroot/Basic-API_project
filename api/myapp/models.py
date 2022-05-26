from django.db import models

# Create your models here.
class employee(models.Model):
    eno=models.IntegerField()
    ename=models.CharField(max_length=100)
    eaddr=models.CharField(max_length=100)
    esal=models.FloatField()

    def __str__(self):
        return self.ename