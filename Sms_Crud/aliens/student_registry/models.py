from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Students(models.Model):
    fullname=models.CharField(max_length=60)
    role_no=models.IntegerField()
    email=models.EmailField()
    mobile=models.IntegerField()
    degree=models.CharField(max_length=30)
    dept=models.CharField(max_length=50)

    def __str__(self):
        return self.fullname
    
class Document(models.Model):
    myfile = models.FileField(upload_to='documents/')
