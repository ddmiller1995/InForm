from django.contrib import admin
from .models import Youth, YouthVisit, PlacementType, School, FormType, Form, FormYouthVisit, Task, TaskYouthVisit

models = [
    Youth, YouthVisit,
    PlacementType, School,
    FormType, Form, FormYouthVisit,
    Task, TaskYouthVisit,
]

for model in models:
    admin.site.register(model)
