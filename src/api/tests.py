import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *

class YouthModelTests(TestCase):
    '''Main test class for all Youth and YouthVisit model methods'''

    def setUp(self):
        '''Runs before all of the actual tests, so these entities can be referenced by test'''
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
        placement = PlacementType.objects.create(
            placement_type_name="Testing",
            default_stay_length=3
        )
        visit1 = YouthVisit.objects.create(
            youth_id=youth1,
            current_placement_start_date=datetime.date(2010, 1, 1),
            city_of_origin="Bellingham",
            current_placement_type=placement,
        )
        visit2 = YouthVisit.objects.create(
            youth_id=youth1,
            current_placement_start_date=timezone.localtime(timezone.now()).date(),
            city_of_origin="Seattle",
            current_placement_type=placement,
        )
        visit3 = YouthVisit.objects.create(
            youth_id=youth2,
            current_placement_start_date=timezone.localtime(timezone.now()).date() - timedelta(days=3),
            city_of_origin="Seattle",
            current_placement_type=placement,
        )
        form_type1 = FormType.objects.create(form_type_name="Intake")
        form_type2 = FormType.objects.create(form_type_name="Outtake")
        form1 = Form.objects.create(form_name="Form 1", form_type_id=form_type1)
        form2 = Form.objects.create(form_name="Form 2", form_type_id=form_type1)
        form3 = Form.objects.create(form_name="Form 3", form_type_id=form_type2)
        form4 = Form.objects.create(form_name="Form 4", form_type_id=form_type2)
        form_youth_visit1 = FormYouthVisit.objects.create(form_id=form1, youth_visit_id=visit2, status='done')
        form_youth_visit2 = FormYouthVisit.objects.create(form_id=form2, youth_visit_id=visit2, status='done')
        form_youth_visit3 = FormYouthVisit.objects.create(form_id=form3, youth_visit_id=visit2, status='done')

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

    def test_get_active_youth_multiple_active(self):    
        self.assertEqual(Youth.get_active_youth(), 
            [
                Youth.objects.get(youth_name="John"),
                Youth.objects.get(youth_name="Bob")        
            ]
        )
   
    def test_get_active_youth_none_active(self):
        YouthVisit.objects.all().delete()
        self.assertEqual(Youth.get_active_youth(), []) 
        # Recreate YouthVisits
        YouthVisit.objects.create(
            youth_id=Youth.objects.get(pk=1),
            current_placement_start_date=datetime.date(2010, 1, 1),
            city_of_origin="Bellingham",
            current_placement_type=PlacementType.objects.get(pk=1),
        )
        YouthVisit.objects.create(
            youth_id=Youth.objects.get(pk=1),
            current_placement_start_date=timezone.localtime(timezone.now()).date(),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(pk=1),
        )
        YouthVisit.objects.create(
            youth_id=Youth.objects.get(pk=2),
            current_placement_start_date=timezone.localtime(timezone.now()).date() - timedelta(days=3),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(pk=1),
        )  

    def test_estimated_exit_date_upcoming(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            current_placement_start_date=datetime.date(2017, 1, 1),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.estimated_exit_date(), datetime.date(2017, 1, 4))

    def test_estimated_exit_date_today(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            current_placement_start_date=datetime.date.today() - timedelta(days=3),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.estimated_exit_date(), datetime.date.today())

    def test_estimated_exit_date_past(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            current_placement_start_date=datetime.date(1805, 12, 31),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.estimated_exit_date(), datetime.date(1806, 1, 3))

    def test_total_days_stayed_visit_started_today(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            visit_start_date=timezone.now().date(),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.total_days_stayed(), 0)

    def test_total_days_stayed_visit_ongoing(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            visit_start_date=timezone.now().date() - timedelta(days=10),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.total_days_stayed(), 10)

    def test_total_days_stayed_visit_ended(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            visit_start_date=timezone.now().date() - timedelta(days=10),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing"),
            visit_exit_date=timezone.now().date() - timedelta(days=7)
        )
        self.assertEqual(visit.total_days_stayed(), 3)

    def test_form_type_progress_method_no_forms(self):
        visit = YouthVisit.objects.get(pk=1)
        progress = visit.form_type_progress()
        self.assertIsNotNone(progress)
        self.assertEqual(progress["Intake"], 0.0)
        self.assertEqual(progress["Outtake"], 0.0)
    
    def test_form_type_progress_method_some_forms(self):
        visit = YouthVisit.objects.get(pk=2)
        progress = visit.form_type_progress()
        self.assertIsNotNone(progress)
        self.assertEqual(progress["Intake"], 1.0)
        self.assertEqual(progress["Outtake"], 0.5)

    def test_overall_form_progress_in_progress(self):
        visit = YouthVisit.objects.get(pk=2)
        self.assertEqual(visit.overall_form_progress(), 0.75) 
        form_youth_visit = FormYouthVisit.objects.create(
            form_id=Form.objects.get(form_name='Form 3'), 
            youth_visit_id=visit, 
            status='in progress'
        )
        self.assertEqual(visit.overall_form_progress(), 0.75)  

    def test_overall_form_progress_done(self):
        visit = YouthVisit.objects.get(pk=2)
        form_youth_visit = FormYouthVisit.objects.create(
            form_id=Form.objects.get(form_name='Form 3'), 
            youth_visit_id=visit, 
            status='done'
        )        
        self.assertEqual(visit.overall_form_progress(), 1.0)

    def test_overall_form_progress_in_progress_no_forms(self):
        visit = YouthVisit.objects.get(pk=3)
        self.assertEqual(visit.overall_form_progress(), 0.0)