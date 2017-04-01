from django.contrib import admin

from .models import Youth, YouthVisit, FormType, Form, FormYouthVisit, Task, TaskYouthVisit

models = [
    Youth, YouthVisit,
    FormType, Form, FormYouthVisit,
    Task, TaskYouthVisit
]

for model in models:
    admin.site.register(model)
