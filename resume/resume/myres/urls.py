from django.urls import path
from .views import *
urlpatterns = [
    path("", index, name = 'home'),
    path("/register", Registration, name = 'registration' ),
    path("/auth", autentification, name = "autentification")
]