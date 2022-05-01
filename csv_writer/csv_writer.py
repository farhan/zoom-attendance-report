import csv


def write_meeting_report_into_csv(project_properties, meeting_report_dict):
    csv_file_name = 'meeting_report_{}_{}_{}.xls'.format(
        project_properties.MEETING_ID,
        project_properties.START_DATE,
        project_properties.END_DATE,
    )
    # TODO: MAKE A PROPER CSV FORMAT
    with open(csv_file_name, 'w') as csvfile:
        field_names = list(meeting_report_dict.keys())
        field_names.extend(['id', 'name', 'user_email', 'duration', 'entry_exit'])
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='excel')
        writer.writeheader()
        for meeting_key in meeting_report_dict:
            for user_key in meeting_report_dict[meeting_key]:
                user_record = meeting_report_dict[meeting_key][user_key]
                user_record[meeting_key] = user_record['duration']
                writer.writerow(user_record)
