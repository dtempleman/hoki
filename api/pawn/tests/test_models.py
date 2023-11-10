from django.test import TestCase
from pawn.models import Pawn, PawnBody


# Create your tests here.
class ModelTests(TestCase):
    def create_pawn(self):
        return Pawn.objects.create(
            first_name="first",
            last_name="last",
            birthday="2000-01-01",
        )

    def create_pawn_body(self, pawn_id):
        return PawnBody.objects.create(pawn_id=pawn_id)

    def test_pawn(self):
        pawn = self.create_pawn()
        self.assertTrue(isinstance(pawn, Pawn))

    def test_pawn_body(self):
        pawn = self.create_pawn()
        body = self.create_pawn_body(pawn.id)
        self.assertTrue(isinstance(body, PawnBody))
