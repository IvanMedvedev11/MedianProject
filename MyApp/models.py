from django.db import models
class Person(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
# Create your models here.
