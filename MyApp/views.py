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
                fs = FileSystemStorage(location='media/avatars')
                fs.save(request.FILES['avatar'].name, request.FILES['avatar'])
                cursor.execute("INSERT INTO MyApp_person (login, password, avatar) VALUES (%s, %s, %s)", [request.POST.get("login"), password, request.FILES['avatar'].name])
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
        if request.POST.get("title"):
            fs = FileSystemStorage(location='media/images')
            filename = fs.save(request.FILES['image'].name, request.FILES['image'])
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO MyApp_images (name, user, title, likes, dislikes) VALUES(%s, %s, %s, %s, %s)", [request.FILES['image'].name, user, request.POST.get('title'), 0, 0])
        elif request.POST.get("like"):
            with connection.cursor() as cursor:
                cursor.execute("UPDATE MyApp_images SET likes = likes + 1 WHERE name=%s", [request.POST.get("name")])
        elif request.POST.get('dislike'):
            with connection.cursor() as cursor:
                cursor.execute("UPDATE MyApp_images SET dislikes = dislikes + 1 WHERE name=%s", [request.POST.get("name")])
        else:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO MyApp_comments (comment, image, user) VALUES (%s, %s, %s)", [request.POST.get("comment"), request.POST.get("image"), user])
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT name, title, user, likes, dislikes from MyApp_images ORDER BY (likes - dislikes) DESC")
        files = cursor.fetchall()
        cursor.execute('SELECT avatar, user FROM MyApp_person INNER JOIN MyApp_images ON MyApp_person.login = MyApp_images.user')
        avatar = cursor.fetchall()
        all_comments = []
        for image in list(map(lambda x: x[0], files)):
            cursor.execute('SELECT comment, user FROM MyApp_comments WHERE image=%s', [image])
            comments = cursor.fetchall()
            all_comments.append(zip(list(map(lambda x: x[0], comments)), list(map(lambda x: x[1], comments))))
        data['files_users'] = zip(list(map(lambda x: 'images/' + x[0], files)), list(map(lambda x: x[1], files)), list(map(lambda x: x[2], files)), list(map(lambda x: x[3], files)), list(map(lambda x: x[4], files)), list(map(lambda x: 'avatars/' + x[0], avatar)), all_comments)
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
            cursor.execute('SELECT DISTINCT name FROM MyApp_images WHERE title=%s', [img])
            name = cursor.fetchone()
            cursor.execute("DELETE FROM MyApp_images WHERE title=%s", [img])
            cursor.execute("DELETE FROM MyApp_comments WHERE image=%s", [name[0]])
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT name, title FROM MyApp_images WHERE user=%s", [user])
        images = cursor.fetchall()
        data['files'] = zip(list(map(lambda x: 'images/' + x[0], images)), list(map(lambda x: x[1], images)))
    return render(request, 'your_images.html', context=data)
