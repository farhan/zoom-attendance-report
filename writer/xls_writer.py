import calendar

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

from zoom_utils import utils
from zoom_utils.constants import MIN_MINUTES_FOR_ATTENDANCE, DATE_TIME_FORMAT


class XlsWriter:
    user_header_fields = ['id', 'user_email', 'name']
    result_header_fields = ['Attendance\n%', 'No. of\nWorking days', 'No. of\nPresents', 'No. of\nAbsents', ]
    meetings_data_start_col = len(user_header_fields) + len(result_header_fields)
    attendance_percentage_col = len(user_header_fields)
    no_of_working_days_col = attendance_percentage_col + 1
    no_of_presents_col = no_of_working_days_col + 1
    no_of_absents_col = no_of_presents_col + 1

    def __init__(self, project_properties):
        self.xlsx_file = xlsxwriter.Workbook('meeting_report_{}_{}_{}.xlsx'.format(
            project_properties.MEETING_ID,
            project_properties.START_DATE,
            project_properties.END_DATE,
        ))
        self.format_bold = self.xlsx_file.add_format({'bold': True})
        self.format_percentage = self.xlsx_file.add_format({'num_format': '0.0%'})
        self.format_text_wrap = self.xlsx_file.add_format({'text_wrap': 'true'})
        self.format_align_center_bold = self.xlsx_file.add_format()
        self.format_align_center_bold.set_bold()
        self.format_align_center_bold.set_align('center')
        self.format_align_center_bold.set_align('vcenter')
        self.format_align_center_bold.set_text_wrap(True)

    def write_meeting_report_into_xls(self, meetings, report):
        xlsx_sheet = self.xlsx_file.add_worksheet()
        self.write_headers(xlsx_sheet, meetings)
        self.write_user_data(xlsx_sheet, meetings, report)
        self.hide_columns(xlsx_sheet)
        self.xlsx_file.close()

    def write_user_data(self, worksheet, meetings, report):
        row = 1
        for user_record in report:
            user_data = [report[user_record][key] for key in self.user_header_fields]
            worksheet.write_row(row, 0, user_data)
            self.write_results_formulas(worksheet, row, meetings)
            for meeting_report in report[user_record]['meetings_report']:
                duration_mins = round(report[user_record]['meetings_report'][meeting_report]['duration'] / 60, 1)
                col = self.meetings_data_start_col + meetings.index(meeting_report)
                worksheet.write(row, col, duration_mins)
                worksheet.write(
                    row + 1, col, report[user_record]['meetings_report'][meeting_report]['entry_exit'],
                    self.format_text_wrap
                )
                worksheet.set_column(row + 1, col, len(DATE_TIME_FORMAT) + 3)
            worksheet.set_row(row + 1, None, None, {'hidden': True})
            row += 2

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
        for idx, meeting in enumerate(meetings):
            meeting_date_obj = utils.to_date_time(meeting)
            day = calendar.day_name[meeting_date_obj.weekday()]
            data = '{}\n{}'.format(str(meeting_date_obj), day)
            worksheet.write(0, self.meetings_data_start_col + idx, data, self.format_align_center_bold)

    def hide_columns(self, worksheet):
        first_col = self.user_header_fields.index('id')
        last_col = self.user_header_fields.index('user_email')
        worksheet.set_column(first_col, last_col, None, None, {'hidden': True})
