from django.contrib import admin
from .models import Youth, YouthVisit, PlacementType, School, FormType, Form, FormYouthVisit

# class QuestionInline(admin.TabularInline):
#     model = Question
#     extra = 2

# class SurveyAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline]

class YouthAdmin(admin.ModelAdmin):
    list_display = (
        'youth_name',
        'date_of_birth',
        'ethnicity'
    )

class YouthVisitAdmin(admin.ModelAdmin):
    list_display = ('youth_id', 'current_placement_start_date', 'city_of_origin', 'estimated_exit_date', 'is_active')
    search_fields = ['youth_id__youth_name']
    list_filter = ('youth_id', 'current_placement_start_date', 'city_of_origin',
                    'case_manager', 'personal_counselor')

    fieldsets = [
        (None, {'fields': [
            'youth_id',
            'visit_start_date',
            'city_of_origin',
            'state_of_origin',
            'notes'

         ]}
        ),
        ('People', {
            'fields': [
                'social_worker',
                'case_manager',
                'personal_counselor',
                'guardian_name',
                'guardian_relationship',
            ]
        }),
        ('Placement', {
            'fields': [
                'current_placement_type',
                'current_placement_start_date',
                'current_placement_extension_days'
            ]
        }),
        ('School', {
            'classes': ('wide', 'extrapretty',), 
            'description': 'School information',
            'fields': [
                'school',
                ('school_am_transport', 'school_pm_transport'),
                ('school_am_pickup_time', 'school_pm_dropoff_time'),
                ('school_am_phone', 'school_pm_phone'),
                'school_date_requested',
                'school_mkv_complete'
            ]
        }),
        ('Misc', {
            # 'classes': ('collapse',),
            'fields': [
                'referred_by',
                'visit_exit_date',
                'exited_to',
                'permanent_housing',
                'csec_referral',
                'family_engagement_referral',
                'met_greater_than_50_percent_goals'
            ]
        })
    ]



class PlacementTypeAdmin(admin.ModelAdmin):
    list_display = ('placement_type_name', 'default_stay_length', 'supervision_ratio')

class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'school_name',
        'school_district',
        'school_phone'
    )

    list_filter = (
        'school_district',
    )

    search_fields = [
        'school_name',
        'school_district',
        'notes'
    ]

class FormTypeAdmin(admin.ModelAdmin):
    pass

class FormAdmin(admin.ModelAdmin):
    list_display = (
        'form_name',
        'form_type_id',
        'default_due_date',
        'assign_by_default'
    )
    
    list_filter = (
        'form_type_id__form_type_name',
    )

    search_fields = [
        'form_name',
        'form_description',
        'form_type_id__form_type_name'
    ]
class FormYouthVisitAdmin(admin.ModelAdmin):
    pass

admin.site.register(Youth, YouthAdmin)
admin.site.register(YouthVisit, YouthVisitAdmin)
admin.site.register(PlacementType, PlacementTypeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(FormType, FormTypeAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(FormYouthVisit, FormYouthVisitAdmin)