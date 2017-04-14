

def serialize_youth(youth):
    'Serialize the youth object'
    obj = {  # Youth fields
        'id': youth.pk,
        'name': youth.youth_name,
        'dob': youth.date_of_birth
    }
    return obj




def serialize_youth_visit(youth_visit):
    'Serialize the youth_visit object'

    obj = {
        'placement_date': youth_visit.placement_date,
        'placement_type': {
            'name': youth_visit.placement_type.placement_type_name,
            'default_stay_length': youth_visit.placement_type.default_stay_length
        },
        'estimated_exit_date': youth_visit.estimated_exit_date(),
        'school': {
            'school_name': youth_visit.school.school_name,
            'school_district': youth_visit.school.school_district,
            'school_phone': youth_visit.school.school_phone,
        },
        'school_am_transport': youth_visit.school_am_transport,
        'school_am_phone': youth_visit.school_am_phone,
        'school_pm_transport': youth_visit.school_pm_transport,
        'school_pm_dropoff_time': youth_visit.school_pm_dropoff_time,
        'school_pm_phone': youth_visit.school_pm_phone,
        'progress': youth_visit.overall_progress()
    }


    # TODO: Handling for empty fields, currently only works if all fields are not empty

    # TODO: serialize form progress fields - how do we determine which forms/form categories
    # to express as a % for each youth? All?
    # pseudocode
    # for form in Form.objects.all():
    #     obj[f'{form.name}-progess'] = str(form.getProgress())


    return obj
