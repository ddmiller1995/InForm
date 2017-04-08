from django.db import models
from django.contrib.auth.models import User


class PlacementType(models.Model):
    placement_type_name = models.CharField(max_length=64, null=False, blank=False)
    default_stay_length = models.IntegerField()

    def __str__(self):
        return self.placement_type_name


class School(models.Model):
    school_name = models.CharField(max_length=64, null=False, blank=False)
    school_district = models.CharField(max_length=64, null=True, blank=True)
    school_phone = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.school_name


class Youth(models.Model):
    youth_name = models.CharField(max_length=256)
    date_of_birth = models.DateField('date born')
    ethnicity = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.youth_name

    @staticmethod
    def GetActiveYouth():
        '''Return an iterable of activate youth objects'''
        return Youth.objects.all() # TODO: Replace placeholder code


class YouthVisit(models.Model):
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
        return 'Youth: ' + self.youth_id.youth_name + ' - Placement date: ' + str(self.placement_date)


class FormType(models.Model):
    form_type_name = models.CharField(max_length=256)

    def __str__(self):
        return self.form_type_name


class Form(models.Model):
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
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # expected values: pending, in_progess, done
    status = models.CharField(max_length=32, default='pending')

    def __str__(self):
        return 'Youth Visit ID: ' + str(self.youth_visit_id.id) + ' - Form Name: ' + self.form_id.form_name
