from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection
def index(request):
    return render(request, "index.html")
def registration(request):
    data = {"state": True}
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM MyApp_person WHERE login=%s", [request.POST.get("login")])
            if cursor.fetchall() != []:
                data['state'] = False
                return render(request, "registration.html", context=data)
            else:
                state = True
                cursor.execute("INSERT INTO MyApp_person (login, password) VALUES (%s, %s)", [request.POST.get("login"), request.POST.get("password")])
                return HttpResponseRedirect('/image/')
    return render(request, "registration.html")
def login(request):
    data = {"state": True}
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM MyApp_person WHERE login=%s AND password=%s", [request.POST.get("login"), request.POST.get("password")])
            if cursor.fetchall() == []:
                data['state'] = False
                return render(request, "login.html", context=data)
            else:
                state = True
                return HttpResponseRedirect('/image/')
    return render(request, "login.html")
def image(request):
    return render(request, "image.html")
# Create your views here.
