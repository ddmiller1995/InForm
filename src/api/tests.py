import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *

# Create your tests here.

class YouthModelTests(TestCase):

    def setUp(self):
        youth1 = Youth.objects.create(
            youth_name="John",
            date_of_birth=datetime.date(1995, 12, 25),
            ethnicity="white"
        )
        youth2 = Youth.objects.create(
            youth_name="Bob",
            date_of_birth=datetime.date(1999, 3, 7),
            ethnicity="asian"
        )
        visit1 = YouthVisit.objects.create(
            youth_id=youth1,
            placement_date=datetime.date(2010, 1, 1),
            city_of_origin="Bellingham"
        )
        visit2 = YouthVisit.objects.create(
            youth_id=youth1,
            placement_date=timezone.localtime(timezone.now()).date(),
            city_of_origin="Seattle"
        )
        visit3 = YouthVisit.objects.create(
            youth_id=youth2,
            placement_date=timezone.localtime(timezone.now()).date() - timedelta(days=3),
            city_of_origin="Seattle"
        )
        form_type1 = FormType.objects.create(form_type_name="Intake")
        form_type2 = FormType.objects.create(form_type_name="Outtake")
        form1 = Form.objects.create(form_name="Form 1", form_type_id=form_type1)
        form2 = Form.objects.create(form_name="Form 2", form_type_id=form_type1)
        form3 = Form.objects.create(form_name="Form 3", form_type_id=form_type2)
        form_youth_visit1 = FormYouthVisit.objects.create(form_id=form1, youth_visit_id=visit2, status='done')
        #form_youth_visit2 = FormYouthVisit.objects.create(form_id=form1, youth_visit_id=visit2, status='done')
        #form_youth_visit3 = FormYouthVisit.objects.create(form_id=form1, youth_visit_id=visit2, status='done')



    def test_create_youth_succeeds(self):
        self.assertIsNotNone(Youth.objects.all()[0].pk)

    def test_create_visit_succeeds(self):
        self.assertIsNotNone(YouthVisit.objects.all()[0].pk)

    def test_latest_youth_visit_with_no_visits(self):
        youth = Youth.objects.create(
            youth_name="Sam",
            date_of_birth=datetime.date(2000, 10, 7),
            ethnicity="white"
        )
        self.assertRaises(YouthVisit.DoesNotExist, youth.latest_youth_visit)

    def test_latest_youth_visit_with_one_visit(self):
        youth = Youth.objects.get(youth_name="Bob")
        # Bob has one visit, with a primary key of '3'
        latest_visit = YouthVisit.objects.get(pk=3)
        self.assertEqual(youth.latest_youth_visit(), latest_visit)

    def test_latest_youth_visit_with_multiple_visits(self):
        youth = Youth.objects.get(youth_name="John")
        # John has two visits, the most recent one has a primary key of '2'
        latest_visit = YouthVisit.objects.get(pk=2)
        self.assertEqual(youth.latest_youth_visit(), latest_visit)

    # TODO: Expand testing for this method and for the other model methods
    def test_form_type_progress_method(self):
        visit = YouthVisit.objects.filter(pk=2)[0]
        progress = visit.form_type_progress()
        self.assertIsNotNone(progress)
        self.assertEqual(progress["Intake"], 0.5)
        self.assertEqual(progress["Outtake"], 0.0)

