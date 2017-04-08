import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *

# Create your tests here.

class YouthModelTests(TestCase):

    def test_create_youth_succeeds(self):
        youth = Youth(
            youth_name="John",
            date_of_birth=datetime.date(1995, 12, 25),
            ethnicity="white"
        )
        youth.save()
        self.assertIsNotNone(youth.pk)

    def test_create_visit_succeeds(self):
        youth = Youth(
            youth_name="John",
            date_of_birth=datetime.date(1995, 12, 25),
            ethnicity="white"
        )
        youth.save()
        youth_visit = YouthVisit(
            youth_id=youth,
            placement_date=timezone.localtime(timezone.now()).date(),
            city_of_origin="Seattle"
        )
        youth_visit.save()
        self.assertIsNotNone(youth_visit.pk)
        youth.delete()
        self.assertIsNone(youth.pk)
        print(youth_visit.pk)
        print(youth_visit.youth_id)
