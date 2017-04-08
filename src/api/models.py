from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.http import Http404

import logging
logger = logging.getLogger(__name__)


class PlacementType(models.Model):
    '''PlacementType model'''
    placement_type_name = models.CharField(max_length=64, null=False, blank=False)
    default_stay_length = models.IntegerField() # expressed as days

    def __str__(self):
        return self.placement_type_name


class School(models.Model):
    '''School model'''
    school_name = models.CharField(max_length=64, null=False, blank=False)
    school_district = models.CharField(max_length=64, null=True, blank=True)
    school_phone = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.school_name


class Youth(models.Model):
    '''Youth model'''
    youth_name = models.CharField(max_length=256)
    date_of_birth = models.DateField('date born')
    ethnicity = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.youth_name

    def latest_youth_visit(self):
        '''Return the latest youth_visit for this Youth

        Raise YouthVisit.DoesNotExist if this Youth does not have any YouthVisits'''
        # filter by all YouthVisit rows that have FKs to this particular youth
        youth_visit = YouthVisit.objects.filter(youth_id=self)

        # if no results found, skip this youth. This happens if a youth has no youth_visit
        if not youth_visit:
            raise YouthVisit.DoesNotExist

        # now youth_visit is the specific youth_visit in the
        # queryset with the latest 'placement_date'
        youth_visit = youth_visit.latest('placement_date')
        return youth_visit

    @staticmethod
    def get_active_youth():
        '''Return an iterable of activate youth objects

        * Estimated exit date = placement date + CURRENT placement type default stay duration
        * Definition of active youth: "Youth whose current estimated exit date hasn't happened yet"
        * Once a youth's estimated exit date has passed, we mark that youth different
        (maybe highlight in light red or something), but DON'T remove it from the
        list of active youth by default
        * We add a mechanism for them to mark exit date
        * If a youth has a exit date marked, only then do we remove them from the
        computed list of active youth
        '''
        active_youth = []
        today = date.today()

        for youth in Youth.objects.all():
            try:
                youth_visit = youth.latest_youth_visit()
            except YouthVisit.DoesNotExist:
                continue
            if today <= youth_visit.estimated_exit_date():
                active_youth.append(youth)

        return active_youth


class YouthVisit(models.Model):
    '''YouthVisit model'''
    youth_id = models.ForeignKey(Youth, on_delete=models.CASCADE)
    placement_date = models.DateField('placement date')
    city_of_origin = models.CharField(max_length=256, null=True, blank=True)
    guardian_name = models.CharField(max_length=256, null=True, blank=True)
    placement_type = models.ForeignKey(
        PlacementType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    referred_by = models.CharField(max_length=256, null=True, blank=True)
    permanent_housing = models.NullBooleanField(null=True, blank=True)
    exited_to = models.CharField(max_length=256, null=True, blank=True)
    case_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    personal_counselor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    # School tracker fields - Not required fields
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    school_am_transport = models.CharField(max_length=256, null=True, blank=True)
    school_am_pickup_time = models.TimeField(null=True, blank=True)
    school_am_phone = models.CharField(max_length=64, null=True, blank=True)
    school_pm_transport = models.CharField(max_length=256, null=True, blank=True)
    school_pm_dropoff_time = models.TimeField(null=True, blank=True)
    school_pm_phone = models.CharField(max_length=64, null=True, blank=True)
    # POSSIBLE COMPUTED FIELDS
    # YF enroll - Youthforce Enrollment Form submitted
    # YF exit - Youthforce Exit Form submitted
    # >= 50% Case Goal Plan
    # total bed nights in program
    # Pay rate - supposedly redundant with bed

    def __str__(self):
        return f'Youth: {self.youth_id.youth_name} - Placement date: {str(self.placement_date)}'

    def estimated_exit_date(self):
        '''Compute the current estimated exit date for this youth's visit
        Estimated exit date = placement date + CURRENT placement type default stay duration
        Returns a datetime.date object
        '''
        return self.placement_date + timedelta(days=self.placement_type.default_stay_length)
        

class FormType(models.Model):
    '''FormType model'''
    form_type_name = models.CharField(max_length=256)

    def __str__(self):
        return self.form_type_name


class Form(models.Model):
    '''Form model'''
    form_name = models.CharField(max_length=256)
    form_description = models.CharField(max_length=2048, null=True, blank=True)
    form_type_id = models.ForeignKey(FormType, on_delete=models.CASCADE)
    # due date in days relative to entry date
    # forms without due dates are allowed
    default_due_date = models.IntegerField(null=True, blank=True)
    # Form location - file location in static files?

    def __str__(self):
        return self.form_name


class FormYouthVisit(models.Model):
    '''FormYouthVisit model'''

    PENDING = 'pending'
    IN_PROGRESS = 'in progress'
    DONE = 'done'

    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # expected values: pending, in_progess, done
    status = models.CharField(max_length=32, default=PENDING, 
        choices=(
            (PENDING, PENDING),
            (IN_PROGRESS, IN_PROGRESS),
            (DONE, DONE)
        )
    )

    def __str__(self):
        return 'Youth Visit ID: ' + str(self.youth_visit_id.id) + ' - Form Name: ' + self.form_id.form_name
