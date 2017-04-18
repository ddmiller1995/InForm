from django.contrib import admin
from .models import Youth, YouthVisit, PlacementType, School, FormType, Form, FormYouthVisit

# class QuestionInline(admin.TabularInline):
#     model = Question
#     extra = 2

# class SurveyAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline]

class YouthAdmin(admin.ModelAdmin):
    list_display = ('youth_name', 'date_of_birth')

class YouthVisitAdmin(admin.ModelAdmin):
    list_display = ('youth_id', 'current_placement_start_date', 'city_of_origin')
    search_fields = ['youth_id']
    list_filter = list_display

class PlacementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'placement_type_name', 'default_stay_length')

class SchoolAdmin(admin.ModelAdmin):
    pass

class FormTypeAdmin(admin.ModelAdmin):
    pass

class FormAdmin(admin.ModelAdmin):
    pass

class FormYouthVisitAdmin(admin.ModelAdmin):
    pass

admin.site.register(Youth, YouthAdmin)
admin.site.register(YouthVisit, YouthVisitAdmin)
admin.site.register(PlacementType, PlacementTypeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(FormType, FormTypeAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(FormYouthVisit, FormYouthVisitAdmin)