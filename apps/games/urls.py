from django.urls import path
from apps.games import views


urlpatterns = [
    path("", views.hello_world),
    path("hello/", views.hello_world),
]
