from django.core.files.storage import FileSystemStorage
import hashlib
import os
from django.conf import settings
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.db import connection
def index(request):
    global state
    state = None
    user = None
    return render(request, "index.html")
def registration(request):
    global user
    global state
    data = {"state": True}
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM MyApp_person WHERE login=%s", [request.POST.get("login")])
            if cursor.fetchall() != []:
                data['state'] = False
                return render(request, "registration.html", context=data)
            else:
                user = request.POST.get("login")
                state = True
                password = hashlib.sha256(request.POST.get("password").encode()).hexdigest()
                cursor.execute("INSERT INTO MyApp_person (login, password) VALUES (%s, %s)", [request.POST.get("login"), password])
                return HttpResponseRedirect('/image/')
    return render(request, "registration.html")
def login(request):
    global user
    global state
    data = {"state": True}
    if request.method == "POST":
        with connection.cursor() as cursor:
            password = hashlib.sha256(request.POST.get("password").encode()).hexdigest()
            cursor.execute("SELECT * FROM MyApp_person WHERE login=%s AND password=%s", [request.POST.get("login"), password])
            if cursor.fetchall() == []:
                data['state'] = False
                return render(request, "login.html", context=data)
            else:
                user = request.POST.get("login")
                state = True
                return HttpResponseRedirect('/image/')
    return render(request, "login.html")
def image(request):
    global state
    global user
    if not state:
        return HttpResponseForbidden("Вы не авторизованы")
    data = {"files_users": []}
    if request.method == "POST":
        fs = FileSystemStorage(location='MyApp/static/images')
        filename = fs.save(request.FILES['image'].name, request.FILES['image'])
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO MyApp_images (name, user, title) VALUES(%s, %s, %s)", [request.FILES['image'].name, user, request.POST.get('title')])
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT name, title, user from MyApp_images")
        files = cursor.fetchall()
        data['files_users'] = zip(list(map(lambda x: x[0], files)), list(map(lambda x: x[1], files)), list(map(lambda x: x[2], files)))
    return render(request, "image.html", context=data)
# Create your views here.
def your_images(request):
    global user
    global state
    if not state:
        return HttpResponseForbidden("Вы не авторизованы")
    data = {"files": []}
    if request.method == "POST":
        with connection.cursor() as cursor:
            img = request.POST.get("image")
            cursor.execute("DELETE FROM MyApp_images WHERE title=%s", [img])
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT name, title FROM MyApp_images WHERE user=%s", [user])
        images = cursor.fetchall()
        data['files'] = zip(list(map(lambda x: x[0], images)), list(map(lambda x: x[1], images)))
    return render(request, 'your_images.html', context=data)
