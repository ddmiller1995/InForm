from django.db import models

# Create your models here.


class Youth(models.Model):
    youth_name = models.CharField(max_length=256)
    date_of_birth = models.DateTimeField('date born')
    # more youth constant attributes here


class YouthVisit(models.Models):
    youth_id = models.ForeignKey(Youth, on_delete=models.CASCADE)
    city_of_origin = models.CharField(max_length=256)
    # more visit specific attributes here


class Form(models.Model):
    form_name = models.CharField(max_length=256)
    form_type_id = models.ForeignKey(FormType, on_delete=models.CASCADE)


class FormType(models.Models):
    form_type_name = models.CharField(max_length=256)


class FormYouthVisit(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_deleted=models.SET_NULL)
    completed = models.BooleanField(default=False)


class Task(models.Models):
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


class TaskYouthVisit(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    youth_visit_id = models.ForeignKey(YouthVisit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_deleted=models.SET_NULL)
    completed = models.BooleanField(default=False)


class User(models.Model):
    user_name = models.CharField(max_length=64)
