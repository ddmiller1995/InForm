from rest_framework import serializers
from api.models import PlacementType, FormType
import logging
logger = logging.getLogger(__name__)

def serialize_youth(youth):
    'Serialize the youth object'
    obj = {}

    obj['youth_id'] = youth.pk
    obj['name'] = youth.youth_name
    obj['dob'] = youth.date_of_birth
    obj['ethnicity'] = youth.ethnicity
    obj['dcfs_id'] = youth.dcfs_id
    obj['notes'] = youth.notes

    return obj


def serialize_user(user):
    'Serialize the user object'
    obj = {}
    if user is not None:
        obj['username'] = user.username
        obj['full_name'] = user.get_full_name()
    else:
        obj['username'] = None
        obj['full_name'] = None
        
    return obj

def serialize_youth_visit(youth_visit):
    'Serialize the youth_visit object'

    obj = {}

    obj['youth_visit_id'] = youth_visit.id
    obj['visit_start_date'] = youth_visit.visit_start_date
    obj['city_of_origin'] = youth_visit.city_of_origin
    obj['guardian_name'] = youth_visit.guardian_name
    obj['guardian_relationship'] = youth_visit.guardian_relationship
    obj['guardian_phone_number'] = youth_visit.guardian_phone_number
    obj['referred_by'] = youth_visit.referred_by
    obj['social_worker'] = youth_visit.social_worker
    obj['permanent_housing'] = youth_visit.permanent_housing
    obj['exited_to'] = youth_visit.exited_to
    obj['visit_exit_date'] = youth_visit.visit_exit_date
    obj['case_manager'] = serialize_user(youth_visit.case_manager)
    obj['personal_counselor'] = serialize_user(youth_visit.personal_counselor)
    obj['current_placement_type'] = {
        'name': youth_visit.current_placement_type.placement_type_name,
        'default_stay_length': youth_visit.current_placement_type.default_stay_length,
        'current_placement_start_date': youth_visit.current_placement_start_date,
        'current_placement_extension_days': youth_visit.current_placement_extension_days
    }
    obj['estimated_exit_date'] = youth_visit.estimated_exit_date()
    if youth_visit.school is not None:
        obj['school'] = {
            'school_name': youth_visit.school.school_name,
            'school_district': youth_visit.school.school_district,
            'school_phone': youth_visit.school.school_phone,
        }
    else:
        obj['school'] = {
            'school_name': None,
            'school_district': None,
            'school_phone': None,
        } 
    obj['school_am_transport'] = youth_visit.school_am_transport
    obj['school_am_pickup_time'] = youth_visit.school_am_pickup_time
    obj['school_am_phone'] = youth_visit.school_am_phone
    obj['school_pm_transport'] = youth_visit.school_pm_transport
    obj['school_pm_dropoff_time'] = youth_visit.school_pm_dropoff_time
    obj['school_pm_phone'] = youth_visit.school_pm_phone
    obj['school_date_requested'] = youth_visit.school_date_requested
    obj['school_mkv_complete'] = youth_visit.school_mkv_complete
    obj['visit_notes'] = youth_visit.notes
    obj['overall_form_progress'] = youth_visit.overall_form_progress()
    obj['total_bed_nights'] = youth_visit.total_days_stayed()

    return obj

def serialize_form_youth_visit(form_youth_visit):
    'Serialize the form_youth_visit object'

    obj = {}

    obj['form_id'] = form_youth_visit.form_id.id
    obj['form_name'] = form_youth_visit.form_id.form_name
    obj['form_type'] = form_youth_visit.form_id.form_type_id.form_type_name
    obj['form_description'] = form_youth_visit.form_id.form_description
    obj['default_due_date'] = form_youth_visit.form_id.default_due_date
    obj['assign_by_default'] = form_youth_visit.form_id.assign_by_default
    obj['status'] = form_youth_visit.status
    obj['completed_by'] = serialize_user(form_youth_visit.user_id)
    obj['days_remaining'] = form_youth_visit.days_remaining()
    obj['notes'] = form_youth_visit.notes

    return obj
    

def serialize_youth_tracker_field(field):
    'Serialize the youth_tracker_fields object'

    obj = {}

    obj['field_name'] = field.field_name
    obj['field_path'] = field.field_path
    obj['displayed'] = field.displayed
    obj['order'] = field.order

    return obj


class PlacementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementType
        fields = '__all__'

class FormTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormType
        fields = '__all__'
