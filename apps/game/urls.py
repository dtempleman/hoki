from django.urls import path
from apps.game import views


urlpatterns = [
    path("", views.game),
    path("hello/", views.hello_world),
]
