from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "myres/base.html", {'title':"Главная страница"})



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1 style="text-align: center; color: blue; font-family: sans-serif;">Page not found</h1>')