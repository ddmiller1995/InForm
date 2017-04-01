from django.contrib import admin

from .models import User, Youth, YouthVisit, FormType, Form, FormYouthVisit, Task, TaskYouthVisit

models = [
    User, Youth, YouthVisit,
    FormType, Form, FormYouthVisit,
    Task, TaskYouthVisit
]

for model in models:
    admin.site.register(model)
