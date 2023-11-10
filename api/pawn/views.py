from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Pawn, PawnBody
from .serializers import PawnBodySerializer, PawnSerializer


# Pawn views
@api_view(["GET"])
def list_pawns(request):
    pawn = Pawn.objects.all()
    serializer = PawnSerializer(pawn, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_pawn(request, id):
    try:
        pawn = Pawn.objects.get(id=id)
        body = PawnBody.objects.get(pawn_id=id)
    except Pawn.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    body_serializer = PawnBodySerializer(body)
    serializer = PawnSerializer(pawn)
    data = serializer.data
    data["body"] = body_serializer.data
    return Response(data)


@api_view(["POST"])
def set_pawn(request):
    pawn_serializer = PawnSerializer(data=request.data)
    if pawn_serializer.is_valid():
        pawn_serializer.save()

    body = PawnBody(pawn_id=pawn_serializer.data["id"])
    body.save()

    return Response(pawn_serializer.data)


@api_view(["DELETE"])
def delete_pawn(request, id):
    pawn = Pawn.objects.get(id=id)
    pawn.delete()
    return Response()


@api_view(["PUT"])
def update_pawn(request, id):
    pawn = Pawn.objects.get(id=id)
    serializer = PawnSerializer(pawn, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_pawn_body(request, pawn_id):
    body = PawnBody.objects.get(pawn_id=pawn_id)
    serializer = PawnBodySerializer(body, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
