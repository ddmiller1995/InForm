from ajax_select import make_ajax_form
from ajax_select.admin import (AjaxSelectAdmin, AjaxSelectAdminStackedInline,
                               AjaxSelectAdminTabularInline)
from django.contrib import admin

from .models import (Form, FormType, FormYouthVisit, PlacementType, School,
                     Youth, YouthVisit, YouthTrackerField)


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

class YouthVisitAdmin(AjaxSelectAdmin):
    list_display = ('youth_id', 'current_placement_start_date', 'city_of_origin', 'estimated_exit_date', 'is_active')
    search_fields = ['youth_id__youth_name']
    list_filter = ('current_placement_start_date', 'city_of_origin',
                    'case_manager', 'personal_counselor')

    form = make_ajax_form(YouthVisit, {
        # fieldname: channel_name
        'youth_id': 'youth'
    })

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
                'guardian_phone_number'
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
    list_display = [
        'get_form_name',
        'get_youth_name',
        'get_youth_visit_start_date',
        'status'
    ]

    def get_youth_name(self, obj):
        return obj.youth_visit_id.youth_id.youth_name
    get_youth_name.admin_order_field = 'youth_visit_id__youth_id__youth_name'
    get_youth_name.short_description = 'Youth Name'

    def get_youth_visit_start_date(self, obj):
        return obj.youth_visit_id.visit_start_date
    get_youth_visit_start_date.admin_order_field = 'youth_visit_id__visit_start_date'
    get_youth_visit_start_date.short_description = 'Youth Visit Start Date'

    def get_form_name(self, obj):
        return obj.form_id.form_name
    get_form_name.admin_order_field = 'form_id__form_name'
    get_form_name.short_description = 'Form Name'

    list_filter = (
        'form_id__form_name',
        'youth_visit_id__visit_start_date',
        'status',
        'youth_visit_id__youth_id__youth_name'        
    )

    search_fields = [
        'youth_visit_id__youth_id__youth_name',
        'form_id__form_name',
        'form_id__form_description'
    ]

class YouthTrackerFieldAdmin(admin.ModelAdmin):
    #exclude = ('field_path',)
    ordering = ('-displayed', 'order',)

    list_display = [
        'field_name',
        'order',
        'displayed'
    ]

    list_filter = [
        'displayed'
    ]

    search_fields = [
        'field_name'
    ]

    def get_actions(self, request):
        #Disable delete
        actions = super(YouthTrackerFieldAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

    def has_add_permission(self, request):
        #Disable add
        return False

admin.site.register(Youth, YouthAdmin)
admin.site.register(YouthVisit, YouthVisitAdmin)
admin.site.register(PlacementType, PlacementTypeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(FormType, FormTypeAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(FormYouthVisit, FormYouthVisitAdmin)
admin.site.register(YouthTrackerField, YouthTrackerFieldAdmin)
