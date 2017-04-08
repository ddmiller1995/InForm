from django.contrib import admin
from .models import Youth, YouthVisit, PlacementType, School, FormType, Form, FormYouthVisit

models = [
    Youth, YouthVisit,
    PlacementType, School,
    FormType, Form, FormYouthVisit
]

for model in models:
    admin.site.register(model)
