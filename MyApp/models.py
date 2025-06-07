from django.db import models
class Person(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=1000)
# Create your models here.
class Images(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=20)
    title = models.CharField(max_length=100)