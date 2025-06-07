from django.db import models
class Person(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=1000)
    avatar = models.CharField(max_length=100, null=True)
# Create your models here.
class Images(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
class Comments(models.Model):
    comment = models.CharField(max_length=1000000)
    image = models.CharField(max_length=100)
    user = models.CharField(max_length=20)