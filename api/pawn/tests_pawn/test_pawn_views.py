import ast

from django.test import TestCase
from django.urls import reverse
from pawn import views
from pawn.models import Pawn, PawnBody
from pawn.serializers import PawnSerializer

# Create your tests here.


def decode_response_content(resp):
    return ast.literal_eval(resp.content.decode("UTF-8"))


class PawnViewTests(TestCase):
    def add_pawn(self):
        pawn = Pawn.objects.create(
            first_name="first",
            last_name="last",
            birthday="2000-01-01",
        )
        body = PawnBody.objects.create(pawn_id=pawn.id)
        return pawn, body

    def test_list_pawns(self):
        _, _ = self.add_pawn()
        resp = self.client.get(
            reverse(views.list_pawns),
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_pawn(self):
        pawn, _ = self.add_pawn()
        resp = self.client.get(
            reverse(views.get_pawn, args=[pawn.id]),
        )
        self.assertEqual(resp.status_code, 200)

    def test_set_pawn(self):
        resp = self.client.post(
            reverse(views.set_pawn),
            data={
                "first_name": "first",
                "last_name": "last",
                "birthday": "2000-01-01",
            },
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete_pawn(self):
        pawn, _ = self.add_pawn()
        resp = self.client.delete(
            reverse(views.delete_pawn, args=[pawn.id]),
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_pawn, args=[pawn.id]),
        )
        self.assertEqual(resp.status_code, 404)

    def test_update_pawn(self):
        pawn, _ = self.add_pawn()
        serializer = PawnSerializer(pawn)
        data = serializer.data
        data["first_name"] = "new first"

        resp = self.client.put(
            reverse(views.update_pawn, args=[pawn.id]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_pawn, args=[pawn.id]),
        )
        content = decode_response_content(resp)
        self.assertEqual(content["first_name"], "new first")

    def test_update_pawn_body(self):
        pawn, body = self.add_pawn()
        resp = self.client.get(
            reverse(views.get_pawn, args=[pawn.id]),
        )
        body_content = decode_response_content(resp)["body"]
        body_content["head"] = 0.5
        resp = self.client.put(
            reverse(views.update_pawn_body, args=[pawn.id]),
            data=body_content,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_pawn, args=[pawn.id]),
        )
        body_content = decode_response_content(resp)["body"]
        self.assertEqual(body_content["head"], 0.5)
