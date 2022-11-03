from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    return render(request, "hello.html", context={"name": "daniel"})


def game(request):
    return HttpResponse("Hello world")
