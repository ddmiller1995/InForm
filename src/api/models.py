import logging
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


def timezone_date():
    '''Returns just the date portion of the timezone.now() function
    Used as a callable to evaluate the current date as a default field value'''
    return timezone.localtime(timezone.now()).date()

class PlacementType(models.Model):
    '''PlacementType model
    Should be prepopulated with the 6 current types:
    - Interim(1A) - 30 days - 1:3
    - Interim(1B) - 30 days - 1:4
    - Assessment - 30 days - 1:5
    - RHY - 21 days - 1:8
    - HOPE(Self) - 30 days - 1:8
    - HOPE(State) - 30 days - 1:8
    '''
    placement_type_name = models.CharField(max_length=64)
    default_stay_length = models.IntegerField() # expressed as days
    supervision_ratio = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.placement_type_name


class School(models.Model):
    '''School model'''
    school_name = models.CharField(max_length=64, null=False, blank=False)
    school_district = models.CharField(max_length=64, null=True, blank=True)
    school_phone = models.CharField(max_length=64, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.school_name

class Youth(models.Model):
    '''Youth model'''
    youth_name = models.CharField(max_length=256, help_text="Full name")
    date_of_birth = models.DateField('date born')
    ethnicity = models.CharField(max_length=256, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

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
        # queryset with the latest 'current_placement_start_date'
        youth_visit = youth_visit.latest('current_placement_start_date')
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
        today = timezone_date()

        for youth in Youth.objects.all():
            try:
                youth_visit = youth.latest_youth_visit()
            except YouthVisit.DoesNotExist:
                continue
            if youth_visit.is_active():
                active_youth.append(youth)

        return active_youth


USER_WARNING_DONT_EDIT_FIELD = "Don't edit this field directly in this admin page. Instead edit it through the main UI."

class YouthVisit(models.Model):
    '''YouthVisit model'''

    MET_GOALS_YES = 'Yes'
    MET_GOALS_NO = 'No'
    MET_GOALS_NA = 'N/A'

    youth_id = models.ForeignKey(Youth, on_delete=models.CASCADE,
        verbose_name='Youth',
        help_text="If the Youth isn't in this dropdown already, you can add them with the green plus icon")

    # Required fields
    visit_start_date = models.DateField('initial start date for the visit', default=timezone_date,
        help_text=USER_WARNING_DONT_EDIT_FIELD)
    current_placement_type = models.ForeignKey(PlacementType, on_delete=models.PROTECT)
    current_placement_start_date = models.DateField('placement start date', default=timezone_date)  

    # Non-required fields
    current_placement_extension_days = models.IntegerField(default=0, blank=True,
        help_text="Don't edit this field")
    city_of_origin = models.CharField(max_length=256, null=True, blank=True)
    state_of_origin = models.CharField(max_length=64, default='Washington', null=True, blank=True)
    guardian_name = models.CharField(max_length=256, null=True, blank=True)
    guardian_relationship = models.CharField(max_length=256, null=True, blank=True)
    referred_by = models.CharField(max_length=256, null=True, blank=True)
    social_worker = models.CharField(max_length=256, null=True, blank=True)
    visit_exit_date = models.DateField(null=True, blank=True)
    permanent_housing = models.NullBooleanField(null=True, blank=True)
    exited_to = models.CharField(max_length=256, null=True, blank=True)

    csec_referral = models.BooleanField(default=False)
    family_engagement_referral = models.BooleanField(default=False)
    met_greater_than_50_percent_goals = models.CharField(max_length=32, default=MET_GOALS_NA,
                              choices=(
                                  (MET_GOALS_YES, MET_GOALS_YES),
                                  (MET_GOALS_NO, MET_GOALS_NO),
                                  (MET_GOALS_NA, MET_GOALS_NA)
                              ),
                              blank=True
                             )

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
    school_date_requested = models.DateField('date information is requested from school', null=True, blank=True)
    school_mkv_complete = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Youth: ' + self.youth_id.youth_name + ' - Placement date: ' + str(self.current_placement_start_date)

    def is_active(self):
        '''Return True if the Youth for this visit is still active'''
        today = timezone_date()
        return self.visit_exit_date is None
    is_active.boolean = True
    is_active.short_description = 'Is Active?'

    def is_before_estimated_exited_date(self):
        '''Return True if the today is before the youth's estimated exit date'''
        today = timezone_date()
        return today <= self.estimated_exit_date()


    def estimated_exit_date(self):
        '''Compute the current estimated exit date for this youth's visit
        Estimated exit date = placement date + CURRENT placement type default stay duration
        Returns a datetime.date object
        '''
        return self.current_placement_start_date + (
            timedelta(days=self.current_placement_type.default_stay_length) +
            timedelta(days=self.current_placement_extension_days)
        )

    def total_days_stayed(self):
        '''Sums and returns the days in this visit, which can include multiple placements and extensions'''
        end_date = self.visit_exit_date if self.visit_exit_date != None else timezone_date()
        return (end_date - self.visit_start_date).days

    def form_type_progress(self):
        '''Computes the ratio of forms marked as completed for this youth's visit
        Forms are grouped into their type and a dictionary is returned with 
        type/ratio pairs
        '''
        result = {}

        # Builds a QuerySet of each FormType and the total count of forms with that type
        form_type_counts = FormType.objects.annotate(form_count=Count('form'))

        # Returns a QuerySet of forms completed for this visit
        youth_visit_done_forms = FormYouthVisit.objects.filter(youth_visit_id=self, status='done')
        for form_type in form_type_counts:
            # Counts the forms marked as done with each form type
            done_count = youth_visit_done_forms.filter(form_id__form_type_id=form_type).count()
            # Calculate the ratio, store with the key as the form type name
            if form_type.form_count == 0:
                result[form_type.form_type_name] = 0.0
            else:
                result[form_type.form_type_name] = done_count / form_type.form_count
        
        return result

    def overall_form_progress(self):
        '''Return the percentage of forms completed out of possible forms as a ratio
        '''
        # Count the total number of forms in the database
        youth_visit_total_forms = FormYouthVisit.objects.filter(youth_visit_id=self).count()
        # Count the number of forms maked as completed for this youth's visit
        youth_visit_done_form_count = FormYouthVisit.objects.filter(youth_visit_id=self, status='done').count()

        if youth_visit_total_forms == 0:
            return 0.0

        return youth_visit_done_form_count / youth_visit_total_forms

    def get_absolute_url(self):
        return reverse('youth-detail', args=[str(self.id)])


class FormType(models.Model):
    '''FormType model'''
    form_type_name = models.CharField(max_length=256)

    def __str__(self):
        return self.form_type_name


class Form(models.Model):
    '''Form model'''
    form_name = models.CharField(max_length=256)
    form_description = models.CharField(max_length=2048, null=True, blank=True)
    form_type_id = models.ForeignKey(FormType, on_delete=models.CASCADE, verbose_name='Form Type')
    # due date in days relative to entry date
    # forms without due dates are allowed
    default_due_date = models.IntegerField(null=True, blank=True, verbose_name='Due in _ days')
    # Form location - file location in static files?
    assign_by_default = models.BooleanField(default=False,
                                            help_text='Check this box if you want this form to be assigned\
                                            to new youth visits by default')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.form_name


class FormYouthVisit(models.Model):
    '''FormYouthVisit model'''

    PENDING = 'pending'
    IN_PROGRESS = 'in progress'
    DONE = 'done'

    form_id = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name='Form')
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE, verbose_name='Youth Visit')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Completed by')
    # expected values: pending, in progess, done
    status = models.CharField(max_length=32, default=PENDING,
                              choices=(
                                  (PENDING, PENDING),
                                  (IN_PROGRESS, IN_PROGRESS),
                                  (DONE, DONE)
                              )
                             )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Youth Visit ID: ' + str(self.youth_visit_id.youth_id.youth_name) + ' - Form Name: ' + self.form_id.form_name

    def days_remaining(self):
        if self.form_id.default_due_date is None:
            return None
        result = self.form_id.default_due_date - (timezone_date() - self.youth_visit_id.visit_start_date).days
        return result


class YouthTrackerField(models.Model):
    '''YouthTrackerField model'''

    # Formatted name for the field to be displayed
    field_name = models.CharField(max_length=256)
    # Computer readable path in the Youth object to lookup. Expected format:
    #   - | (pipe) character indicates the next level of an array or object
    #   - + (plus) character indicates to combine the two fields into one column
    field_path = models.CharField(max_length=256)
    displayed = models.BooleanField(default=False)
    order = models.IntegerField(default=0, blank=True, null=True)

    @staticmethod
    def get_youth_tracker_fields():
        return YouthTrackerField.objects.filter(displayed=True).order_by('order', 'field_name')

    def __str__(self):
        return self.field_name


@receiver(post_save, sender=YouthVisit)
def AddDefaultForms(sender, **kwargs):
    if kwargs['created']:
        for form in Form.objects.filter(assign_by_default=True):
            form_youth_visit = FormYouthVisit.objects.create(
                form_id=form,
                youth_visit_id=kwargs['instance'],
                status=FormYouthVisit.PENDING
            )

