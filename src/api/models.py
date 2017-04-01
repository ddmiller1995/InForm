from django.db import models

# Create your models here.


# Are we planning on restricting access based on role?
class User(models.Model):
    user_name = models.CharField(max_length=64)

    def __str__(self):
        return self.user_name


class Youth(models.Model):
    youth_name = models.CharField(max_length=256, null=False, blank=False)
    date_of_birth = models.DateTimeField('date born', null=False, blank=False)
    ethnicity = models.CharField(max_length=64)

    def __str__(self):
        return self.youth_name


# School tracker currently not included, possible new table?
class YouthVisit(models.Model):
    youth_id = models.ForeignKey(Youth, on_delete=models.CASCADE)
    placement_date = models.DateTimeField(
        'placement date', null=False, blank=False)
    city_of_origin = models.CharField(max_length=256)
    guardian_name = models.CharField(max_length=256)
    # should bed type be a table?
    bed_type = models.CharField(max_length=256)
    referred_by = models.CharField(max_length=256)
    permanent_housing = models.CharField(max_length=256)
    exited_to = models.CharField(max_length=256)
    case_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
    personal_counselor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
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


# Need to integrate Case Goal plan with Tasks
class Task(models.Model):
    task_name = models.CharField(max_length=256)
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
    # due date is relative to entry date, so should it be computed in business logic
    # or enforced by model?
    due_date = models.DateTimeField('due date')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return 'Youth Visit ID: ' + self.youth_visit_id.id + ' - Task ID: ' + self.task_id.id
