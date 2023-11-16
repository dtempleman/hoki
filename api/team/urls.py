from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list_teams),
    path("get/<int:id>", views.get_team),
    path("set/", views.set_team),
    path("update/<int:id>", views.update_team),
    path("delete/<int:id>", views.delete_team),
    path("contract/set", views.set_contract),
    path("contract/delete/<int:id>", views.delete_contract),
    path("contract/updat/<int:id>", views.update_contract),
    path("contract/list/<int:team_id>", views.list_team_contracts),
    path("contract/get/<int:pawn_id>", views.get_player_contract),
]
