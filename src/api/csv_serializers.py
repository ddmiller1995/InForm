from datetime import datetime

youth_field_names = ['youth_id', 'youth_name', 'date_of_birth', 'ethnicity', 'youth_notes']

youth_visit_field_names = ['youth_visit_id', 'visit_start_date',

                           'current_placement_type_id', 'current_placement_type_name',
                           'current_placement_type_default_stay_length',
                           'current_placement_type_supervision_ratio',

                           'current_placement_start_date', 'current_placement_extension_days',
                           'city_of_origin', 'state_of_origin',
                           'guardian_name', 'guardian_relationship', 'referred_by',
                           'social_worker', 'visit_exit_date', 'permanent_housing', 'exited_to',
                           'csec_referral', 'family_engagement_referral',
                           'met_greater_than_50_percent_goals',

                           'case_manager_id', 'case_manager_name', 'case_manager_username',
                           'personal_counselor_id', 'personal_counselor_name',
                           'personal_counselor_username',

                           'school_id', 'school_name', 'school_district',
                           'school_phone', 'school_notes',

                           'school_am_transport', 'school_am_pickup_time', 'school_am_phone',
                           'school_pm_transport', 'school_pm_dropoff_time', 'school_pm_phone',
                           'school_date_requested', 'school_mkv_complete', 'youth_visit_notes'
                          ]

class Error(Exception):
    pass

class CsvLineParseError(Error):
    pass

class CsvLineAccessError(Error):
    pass

class CsvLine(object):
    def __init__(self, line):
        self.line = line
        if not self.validate_line():
            raise CsvLineParseError()

        self.DATE_FORMAT = '%Y-%m-%d'

    def __getitem__(self, value):
        return self.line[value]

    def validate_line(self):
        return True

    def get_string_field(self, index, default):
        if index > len(self.line) - 1:
            raise CsvLineAccessError()

        return self.line[index] if self.line[index] else default

        
    def get_datetime_field(self, index, default=None):
        string_field = self.get_string_field(index, default)
        string_field = string_field.decode('ascii')
        date_field = datetime.strptime(string_field, self.DATE_FORMAT)
        return date_field