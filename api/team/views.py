from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Team, TeamContract
from .serializers import TeamContractSerializer, TeamSerializer


# Team views
@api_view(["GET"])
def list_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_team(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team)
    data = serializer.data
    return Response(data)


@api_view(["POST"])
def set_team(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_team(request, id):
    team = Team.objects.get(id=id)
    team.delete()
    return Response()


@api_view(["PUT"])
def update_team(request, id):
    team = Team.objects.get(id=id)
    serializer = TeamSerializer(team, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Contracts views
@api_view(["POST"])
def set_contract(request):
    serializer = TeamContractSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_contract(request, id):
    contract = TeamContract.objects.get(id=id)
    contract.delete()
    return Response()


@api_view(["PUT"])
def update_contract(request, id):
    contract = TeamContract.objects.get(id=id)
    serializer = TeamContractSerializer(contract, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_team_contracts(request, team_id):
    contracts = TeamContract.objects.filter(team_id=team_id)
    serializer = TeamContractSerializer(contracts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_player_contract(request, pawn_id):
    try:
        contract = TeamContract.objects.get(player_id=pawn_id)
    except TeamContract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeamContractSerializer(contract)
    data = serializer.data
    return Response(data)
