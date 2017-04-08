from django.db import models
from django.contrib.auth.models import User


class PlacementType(models.Model):
    placement_type_name = models.CharField(max_length=64, null=False, blank=False)
    default_stay_length = models.IntegerField()

    def __str__(self):
        return self.placement_type_name


class School(models.Model):
    school_name = models.CharField(max_length=64, null=False, blank=False)
    school_district = models.CharField(max_length=64)
    school_phone = models.CharField(max_length=64)

    def __str__(self):
        return self.school_name


class Youth(models.Model):
    youth_name = models.CharField(max_length=256, null=False, blank=False)
    date_of_birth = models.DateField('date born', null=False, blank=False)
    ethnicity = models.CharField(max_length=64)

    def __str__(self):
        return self.youth_name

    @staticmethod
    def GetActiveYouth():
        '''Return an iterable of activate youth objects'''
        return []
        return Youth.objects.all() # TODO: Replace placeholder code


class YouthVisit(models.Model):
    youth_id = models.ForeignKey(Youth, on_delete=models.CASCADE)
    placement_date = models.DateField(
        'placement date', null=False, blank=False)
    city_of_origin = models.CharField(max_length=256)
    guardian_name = models.CharField(max_length=256)
    placement_type = models.ForeignKey(PlacementType, on_delete=models.SET_NULL, null=True)
    referred_by = models.CharField(max_length=256)
    permanent_housing = models.CharField(max_length=256)
    exited_to = models.CharField(max_length=256)
    case_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
    personal_counselor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
    # School tracker fields
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    school_am_transport = models.CharField(max_length=256)
    school_am_pickup_time = models.TimeField(null=True)
    school_am_phone = models.CharField(max_length=64)
    school_pm_transport = models.CharField(max_length=256)
    school_pm_dropoff_time = models.TimeField(null=True)
    school_pm_phone = models.CharField(max_length=64)
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
    form_type_id = models.ForeignKey(FormType, on_delete=models.CASCADE)

    def __str__(self):
        return self.form_name


class FormYouthVisit(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return 'Youth Visit ID: ' + self.youth_visit_id.id + ' - Form ID: ' + self.form_id.id


class Task(models.Model):
    task_name = models.CharField(max_length=256)
    # due date in days relative to entry date
    default_due_date = models.IntegerField(null=True, blank=True)
    form_id = models.ForeignKey(
        Form,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    form_type_id = models.ForeignKey(
        FormType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.task_name


class TaskYouthVisit(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return 'Youth Visit ID: ' + self.youth_visit_id.id + ' - Task ID: ' + self.task_id.id
