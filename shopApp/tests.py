from django.test import TestCase
from .models import *

class ItemTestCase(TestCase):
    def setUp(self):
        cat1 = Category.objects.get(id=6)
        cat2 = Category.objects.get(id=7)
        Item.objects.create(make="Sony", name="PS8", desc="NAIIS", properties="miau|hau", category=cat1, image="shopApp/static/img/pylly.png", price="30", quantityAvailable=5, date_added="2018-09-09", objects="")
        Item.objects.create(make="pierutv", name="ruma telkkari", desc="HYI", properties="lollero", category=cat2, image="shopApp/static/img/pieru.png", price="3", quantityAvailable=2, date_added="2070-10-02", objects="")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        sony = Item.objects.get(name="PS8")
        pierutv = Item.objects.get(name="pierutv")

        self.assertEqual(sony.date_added(), "2018-09-09")
        self.assertEqual(pierutv.date_added(), "2070-10-02")
