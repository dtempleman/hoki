from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list_pawns),
    path("get/<int:id>", views.get_pawn),
    path("set/", views.set_pawn),
    path("update/<int:id>", views.update_pawn),
    path("delete/<int:id>", views.delete_pawn),
    path("body/update/<int:pawn_id>", views.update_pawn_body),
]
