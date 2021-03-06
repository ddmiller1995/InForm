import datetime

from django.test import TestCase
from django.utils import timezone

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from .models import *
from .views import DATE_STRING_FORMAT

class YouthModelTests(TestCase):
    '''Main test class for all Youth and YouthVisit model methods'''

    def timezone_date():
        '''Returns just the date portion of the timezone.now() function
        Used as a callable to evaluate the current date as a default field value'''
        return timezone.localtime(timezone.now()).date()

    def setUp(self):
        '''Runs before all of the actual tests, so these entities can be referenced by tests'''

        self.user = User.objects.create(username='test')

        youth1 = Youth.objects.create(
            youth_name="John",
            date_of_birth=datetime.date(1995, 12, 25),
        )
        youth2 = Youth.objects.create(
            youth_name="Bob",
            date_of_birth=datetime.date(1999, 3, 7),
        )

        youth3 = Youth.objects.create(
            youth_name="Sarah",
            date_of_birth=datetime.date(1995, 4, 20)
        )

        youth4 = Youth.objects.create(
            youth_name="Neville",
            date_of_birth=datetime.date(1996, 3, 22)
        )

        placement = PlacementType.objects.create(
            placement_type_name="Testing",
            default_stay_length=3
        )

        placement2 = PlacementType.objects.create(
            placement_type_name="RHY",
            default_stay_length=21
        )

        visit1 = YouthVisit.objects.create(
            youth_id=youth1,
            current_placement_start_date=datetime.date(2010, 1, 1),
            city_of_origin="Bellingham",
            current_placement_type=placement,
        )
        visit2 = YouthVisit.objects.create(
            youth_id=youth1,
            current_placement_start_date=timezone_date(),
            city_of_origin="Seattle",
            current_placement_type=placement,
        )
        visit3 = YouthVisit.objects.create(
            youth_id=youth2,
            current_placement_start_date=timezone_date() - timedelta(days=3),# Visit started 3 days ago
            city_of_origin="Seattle",
            current_placement_type=placement,
        )

        visit4_exited_before_deadline = YouthVisit.objects.create(
            youth_id=youth3,
            current_placement_start_date=timezone_date() - timedelta(days=2), # placement deadline is 3 days
            city_of_origin="Everett",
            current_placement_type=placement,
            visit_exit_date=timezone_date() # this youth should not be active b/c they have exit date
        )

        
        visit5_exited_after_deadline = YouthVisit.objects.create(
            youth_id=youth3,
            current_placement_start_date=timezone_date() - timedelta(days=5), # placement deadline is 3 days
            city_of_origin="Everett",
            current_placement_type=placement,
            visit_exit_date=timezone_date() # this youth should not be active b/c they have exit date
        )

        visit6_deadline_extended = YouthVisit.objects.create(
            youth_id=youth4,
            current_placement_start_date=timezone_date() - timedelta(days=22), # placed 22 days ago
            city_of_origin="Mountlake Terrace",
            current_placement_type=placement2, # 21 day deadline
            current_placement_extension_days=15 # given 15 day extension
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

    
    def test_duplicate_form_youth_visit(self):
        form1 = Form.objects.get(form_name="Form 1")
        visit2 = YouthVisit.objects.get(pk=2)

        query = FormYouthVisit.objects.filter(form_id=form1, youth_visit_id=visit2)
        self.assertEqual(query.count(), 1)
        form_youth_visit1 = FormYouthVisit.objects.create(form_id=form1, youth_visit_id=visit2, status='in progress')
        query = FormYouthVisit.objects.filter(form_id=form1, youth_visit_id=visit2, status='done')
        self.assertEqual(query.count(), 1)

    def test_create_youth_succeeds(self):
        self.assertIsNotNone(Youth.objects.all()[0].pk)

    def test_create_visit_succeeds(self):
        self.assertIsNotNone(YouthVisit.objects.all()[0].pk)

    def test_latest_youth_visit_with_no_visits(self):
        youth = Youth.objects.create(
            youth_name="Sam",
            date_of_birth=datetime.date(2000, 10, 7),
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
                Youth.objects.get(youth_name="Bob"),
                Youth.objects.get(youth_name="Neville")        
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
            current_placement_start_date=timezone_date(),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(pk=1),
        )
        YouthVisit.objects.create(
            youth_id=Youth.objects.get(pk=2),
            current_placement_start_date=timezone_date() - timedelta(days=3),
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
            visit_start_date=timezone_date(),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.total_days_stayed(), 0)

    def test_total_days_stayed_visit_ongoing(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            visit_start_date=timezone_date() - timedelta(days=10),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing")
        )
        self.assertEqual(visit.total_days_stayed(), 10)

    def test_total_days_stayed_visit_ended(self):
        visit = YouthVisit.objects.create(
            youth_id=Youth.objects.get(youth_name="Bob"),
            visit_start_date=timezone_date() - timedelta(days=10),
            city_of_origin="Seattle",
            current_placement_type=PlacementType.objects.get(placement_type_name="Testing"),
            visit_exit_date=timezone_date() - timedelta(days=7)
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
        self.assertEqual(visit.overall_form_progress(), 1.0) 
        form_youth_visit = FormYouthVisit.objects.create(
            form_id=Form.objects.get(form_name='Form 4'), 
            youth_visit_id=visit, 
            status='in progress'
        ) 
        self.assertEqual(visit.overall_form_progress(), 0.75)  

    def test_overall_form_progress_done(self):
        visit = YouthVisit.objects.get(pk=2)
        form_youth_visit = FormYouthVisit.objects.get(
            form_id=Form.objects.get(form_name='Form 3'), 
            youth_visit_id=visit
        )
        form_youth_visit.status = 'done'
        form_youth_visit.save()
        self.assertEqual(visit.overall_form_progress(), 1.0)

    def test_overall_form_progress_in_progress_no_forms(self):
        visit = YouthVisit.objects.get(pk=3)
        self.assertEqual(visit.overall_form_progress(), 0.0)

    def test_youth_visit_is_active_false(self):
        visit = YouthVisit.objects.get(pk=1)
        self.assertEqual(visit.is_active(), True)
        # this youth was placed years ago, but his exit was never marked,
        # so he should technically still be active
        
    def test_youth_visit_is_active_true(self):
        visit = YouthVisit.objects.get(pk=2)
        self.assertEqual(visit.is_active(), True)

    def test_youth_visit_is_active_exited_before(self):
        visit = YouthVisit.objects.get(pk=4)
        self.assertEqual(visit.is_active(), False)

    def test_youth_visit_is_active_exited_after(self):
        visit = YouthVisit.objects.get(pk=5)
        self.assertEqual(visit.is_active(), False)
        
        
    def test_change_placement_type_success(self):
        client = APIClient()
        client.force_authenticate(self.user)

        # client.login(username='youthhaven', password='youthforce')

        youth_visit_id = 1
        new_placement_type_id = 2
        new_placement_start_date = '2017-04-20'

        url = reverse('youth-change-placement', args=[youth_visit_id])

        response = client.post(url, {
            'new_placement_type_id': new_placement_type_id,
            'new_placement_start_date': new_placement_start_date
        })

        self.assertEqual(response.status_code, 202)

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)
        self.assertEqual(youth_visit.current_placement_type.id, new_placement_type_id)
        self.assertEqual(youth_visit.current_placement_start_date, datetime.date(2017, 4, 20))
        self.assertEqual(youth_visit.current_placement_extension_days, 0)

    def test_mark_exited_success(self):
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 1
        
        exit_date = datetime.date(2017, 4, 20)
        where_exited = 'ROOTS'
        permanent_housing = 'false'

        url = reverse('youth-mark-exited', args=[youth_visit_id])

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)
        self.assertEqual(youth_visit.visit_exit_date, None)

        response = client.post(url, {
            'exit_date_string': exit_date.strftime(DATE_STRING_FORMAT), # convert to correct date string format,
            'where_exited': where_exited,
            'permanent_housing': permanent_housing
        })

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(youth_visit.visit_exit_date, exit_date)
        self.assertEqual(youth_visit.exited_to, where_exited)
        self.assertEqual(youth_visit.permanent_housing, False)

    def test_mark_exited_success_2(self):
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 1
        
        exit_date = datetime.date(2017, 4, 20)
        where_exited = 'ROOTS'
        permanent_housing = 'true'

        url = reverse('youth-mark-exited', args=[youth_visit_id])

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)
        self.assertEqual(youth_visit.visit_exit_date, None)

        response = client.post(url, {
            'exit_date_string': exit_date.strftime(DATE_STRING_FORMAT), # convert to correct date string format,
            'where_exited': where_exited,
            'permanent_housing': permanent_housing
        })

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(youth_visit.visit_exit_date, exit_date)
        self.assertEqual(youth_visit.exited_to, where_exited)
        self.assertEqual(youth_visit.permanent_housing, True)

    def test_mark_exited_success_3(self):
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 1
        
        exit_date = datetime.date(2017, 4, 20)
        where_exited = 'ROOTS'
        permanent_housing = 'unknown'

        url = reverse('youth-mark-exited', args=[youth_visit_id])

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)
        self.assertEqual(youth_visit.visit_exit_date, None)

        response = client.post(url, {
            'exit_date_string': exit_date.strftime(DATE_STRING_FORMAT), # convert to correct date string format,
            'where_exited': where_exited,
            'permanent_housing': permanent_housing
        })

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(youth_visit.visit_exit_date, exit_date)
        self.assertEqual(youth_visit.exited_to, where_exited)
        self.assertEqual(youth_visit.permanent_housing, None)

    def test_youth_add_extension_success(self):
        '''Test that the add extension endpoint works as expected
        Testing with a youth visit that was
            * Placed 22 days ago
            * Is given a 21 day deadline
            * Was manually given a 15 day extension before this test

        This test gives him a 15 day extension via the add extension endpoint
        and tests that the youth visit's computed values are as expected afterwards
        '''
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 6
        
        extension = '15'

        url = reverse('youth-add-extension', args=[youth_visit_id])

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)
        self.assertEqual(youth_visit.current_placement_extension_days, 15)
        self.assertEqual(youth_visit.is_active(), True)
        self.assertEqual(youth_visit.is_before_estimated_exited_date(), True)
        self.assertEqual(youth_visit.estimated_exit_date(), 
            youth_visit.current_placement_start_date + 
            timedelta(days=youth_visit.current_placement_type.default_stay_length) +
            timedelta(days=youth_visit.current_placement_extension_days))

        response = client.post(url, {
            'extension': extension
        })

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(youth_visit.current_placement_extension_days, 30)
        self.assertEqual(youth_visit.is_active(), True)
        self.assertEqual(youth_visit.is_before_estimated_exited_date(), True)
        self.assertEqual(youth_visit.estimated_exit_date(), 
            youth_visit.current_placement_start_date + 
            timedelta(days=youth_visit.current_placement_type.default_stay_length) +
            timedelta(days=youth_visit.current_placement_extension_days))

    def test_youth_visit_edit_note_success(self):
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 1

        note = '''
        blah blah
        lorem ipsum notes
        yay'''

        url = reverse('youth-edit-note', args=[youth_visit_id])

        response = client.post(url, {
            'note': note
        })

        youth_visit = YouthVisit.objects.get(id=youth_visit_id)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(youth_visit.notes, note)

    def test_form_edit_note_success(self):
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 2
        form_id = 1

        note = '''
        blah blah
        lorem ipsum notes
        yay'''

        url = reverse('form-edit-note', args=[youth_visit_id])

        response = client.post(url, {
            'form_id': form_id,
            'note': note
        })

        form_youth_visit = FormYouthVisit.objects.get(youth_visit_id=youth_visit_id, form_id=form_id)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(form_youth_visit.notes, note)

    def test_form_youth_visit_days_remaining_with_days_remaining(self):
        visit = YouthVisit.objects.get(pk=3) # Visit started 3 days ago
        visit.visit_start_date = timezone_date() - timedelta(days=3)
        form = Form.objects.get(form_name='Form 3')
        form.default_due_date = 5
        form_youth_visit = FormYouthVisit.objects.create(
            form_id=form,
            youth_visit_id=visit, 
            status='done'
        )
        self.assertEqual(form_youth_visit.days_remaining(), 2)

    def test_form_youth_visit_days_remaining_with_deadline_passed(self):
        visit = YouthVisit.objects.get(pk=3) # Visit started 3 days ago
        visit.visit_start_date = timezone_date() - timedelta(days=3)
        form = Form.objects.get(form_name='Form 3')
        form.default_due_date = 0
        form_youth_visit = FormYouthVisit.objects.create(
            form_id=form,
            youth_visit_id=visit, 
            status='done'
        )
        self.assertEqual(form_youth_visit.days_remaining(), -3)

    def test_change_form_status(self):
        client = APIClient()
        client.force_authenticate(self.user)

        youth_visit_id = 2
        form_id = 1

        url = reverse('change-form-status', args=[youth_visit_id])

        form_youth_visit = FormYouthVisit.objects.get(youth_visit_id=youth_visit_id, form_id=form_id)
        self.assertEqual(form_youth_visit.status, "done")

        response = client.post(url, {
            'form_id': form_id,
            'status': 'in progress'
        })

        form_youth_visit = FormYouthVisit.objects.get(youth_visit_id=youth_visit_id, form_id=form_id)
        

        self.assertEqual(response.status_code, 202)
        self.assertEqual(form_youth_visit.status, "in progress")

class YouthTrackerFieldModelTests(TestCase):
    '''Main test class for all YouthTrackerField model methods'''

    def setUp(self):
        '''Runs before all of the actual tests, so these entities can be referenced by tests'''

        YouthTrackerField.objects.create(
            field_name='Youth Name',
            field_path='name',
            displayed=True,
            order=0
        )
        YouthTrackerField.objects.create(
            field_name='Youth Z',
            field_path='z',
            displayed=True,
        )
        YouthTrackerField.objects.create(
            field_name='Origin City',
            field_path='origin_city',
            displayed=True,
            order=3
        )
        YouthTrackerField.objects.create(
            field_name='Date of Birth',
            field_path='dob',
            displayed=True,
            order=3
        )
        YouthTrackerField.objects.create(
            field_name='Not Displayed',
            field_path='null',
            displayed=False,
            order=0
        )
        YouthTrackerField.objects.create(
            field_name='Not Everything provided',
            field_path='null'
        )

    def test_get_youth_tracker_fields_returns_only_displayed(self):
        self.assertEqual(YouthTrackerField.get_youth_tracker_fields().count(), 4)

    def test_get_youth_tracker_fields_returns_correct_order(self):
        self.assertQuerysetEqual(
            YouthTrackerField.get_youth_tracker_fields(),
            [
                '<YouthTrackerField: Youth Name>', 
                '<YouthTrackerField: Youth Z>', 
                '<YouthTrackerField: Date of Birth>', 
                '<YouthTrackerField: Origin City>'
            ]
        )