import csv

from pip._internal.utils.deprecation import deprecated


@deprecated
def write_meeting_report_into_csv(project_properties, meetings, report):
    csv_file_name = 'meeting_report_{}_{}_{}.xls'.format(
        project_properties.MEETING_ID,
        project_properties.START_DATE,
        project_properties.END_DATE,
    )
    with open(csv_file_name, 'w') as csvfile:
        user_field_names = ['id', 'name', 'user_email']
        field_names = user_field_names + list(meetings)
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='excel')
        writer.writeheader()
        for user_record in report:
            row = {key: report[user_record][key] for key in user_field_names}
            for meeting_report in report[user_record]['meetings_report']:
                duration_mins = round(report[user_record]['meetings_report'][meeting_report]['duration'] / 60, 1)
                row.update({
                    meeting_report: duration_mins
                })
            writer.writerow(row)
