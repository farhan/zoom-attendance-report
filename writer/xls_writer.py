import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

# TODO:
# 4. Add the Check In & Check Out Times
# 5. Remove the outbound joins and their durations
# 6. Clean garbage code
from zoom_utils.constants import MIN_MINUTES_FOR_ATTENDANCE


class XlsWriter:
    user_header_fields = ['id', 'name', 'user_email']
    result_header_fields = ['Attendance %', 'No. of working days', 'No. of presents', 'No. of absents', ]
    meetings_data_start_col = len(user_header_fields) + len(result_header_fields)
    attendance_percentage_col = len(user_header_fields)
    no_of_working_days_col = attendance_percentage_col + 1
    no_of_presents_col = no_of_working_days_col + 1
    no_of_absents_col = no_of_presents_col + 1

    def __init__(self, project_properties):
        self.xlsx_file = xlsxwriter.Workbook('_temp_meeting_report_{}_{}_{}.xlsx'.format(
            project_properties.MEETING_ID,
            project_properties.START_DATE,
            project_properties.END_DATE,
        ))
        self.format_bold = self.xlsx_file.add_format({'bold': True})
        self.format_percentage = self.xlsx_file.add_format({'num_format': '0.0%'})
        self.format_align_center_bold = self.xlsx_file.add_format()
        self.format_align_center_bold.set_bold()
        self.format_align_center_bold.set_align('center')
        self.format_align_center_bold.set_align('vcenter')

    def write_meeting_report_into_xls(self, meetings, report):
        xlsx_sheet = self.xlsx_file.add_worksheet()
        self.write_headers(xlsx_sheet, meetings)
        self.write_user_data(xlsx_sheet, meetings, report)
        self.xlsx_file.close()

    def write_user_data(self, worksheet, meetings, report):
        row = 1
        for user_record in report:
            user_data = [report[user_record][key] for key in self.user_header_fields]
            worksheet.write_row(row, 0, user_data)
            for meeting_report in report[user_record]['meetings_report']:
                duration_mins = round(report[user_record]['meetings_report'][meeting_report]['duration'] / 60, 1)
                col = self.meetings_data_start_col + meetings.index(meeting_report)
                worksheet.write(row, col, duration_mins)
            self.write_results_formulas(worksheet, row, meetings)
            row += 1

    def write_results_formulas(self, worksheet, row, meetings):
        meetings_start_cell = xl_rowcol_to_cell(row, self.meetings_data_start_col)
        meetings_end_cell = xl_rowcol_to_cell(row, self.meetings_data_start_col + len(meetings) - 1)
        # Attendance percentage formula
        no_of_presents_cell = xl_rowcol_to_cell(row, self.no_of_presents_col)
        no_of_working_days_cell = xl_rowcol_to_cell(row, self.no_of_working_days_col)
        formula = '={}/{}'.format(no_of_presents_cell, no_of_working_days_cell)
        worksheet.write(row, self.attendance_percentage_col, formula, self.format_percentage)
        # No. of working days formula
        formula = '=COUNTIF({}:{},"<>*")'.format(meetings_start_cell, meetings_end_cell)
        worksheet.write(row, self.no_of_working_days_col, formula)
        # No. of presents formula
        formula = '=COUNTIF({}:{},">{}")'.format(meetings_start_cell, meetings_end_cell, MIN_MINUTES_FOR_ATTENDANCE)
        worksheet.write(row, self.no_of_presents_col, formula)
        # No. of absents formula
        formula = '=COUNTBLANK({}:{})'.format(meetings_start_cell, meetings_end_cell)
        worksheet.write(row, self.no_of_absents_col, formula)

    def write_headers(self, worksheet, meetings):
        worksheet.write_row(0, 0, self.user_header_fields, self.format_align_center_bold)
        worksheet.write_row(0, len(self.user_header_fields), self.result_header_fields, self.format_align_center_bold)
        worksheet.write_row(0, self.meetings_data_start_col, meetings, self.format_align_center_bold)
