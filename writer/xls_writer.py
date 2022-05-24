import calendar

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

from zoom_utils import utils
from zoom_utils.constants import DATE_TIME_FORMAT


class XlsWriter:

    def __init__(self, configuration):
        self.xlsx_file = xlsxwriter.Workbook('meeting_report_{}_{}_{}.xlsx'.format(
            configuration.MEETING_ID,
            configuration.START_DATE,
            configuration.END_DATE,
        ))
        self.configuration = configuration
        self.__init_formats__()
        self.__init_headers_and_constants__(self.configuration)

    def __init_headers_and_constants__(self, configuration):
        self.user_header_fields = ['id', 'user_email', 'name']
        presents_header = 'No. of\nPresents\nAttended > {} mins'.format(configuration.MIN_MINUTES_FOR_ATTENDANCE)
        self.result_header_fields = ['Attendance\n%', 'No. of\nWorking days', presents_header, 'No. of\nAbsents']
        self.meetings_data_start_col = len(self.user_header_fields) + len(self.result_header_fields)
        self.attendance_percentage_col = len(self.user_header_fields)
        self.no_of_working_days_col = self.attendance_percentage_col + 1
        self.no_of_presents_col = self.no_of_working_days_col + 1
        self.no_of_absents_col = self.no_of_presents_col + 1

    def __init_formats__(self):
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
        self.__write_headers(xlsx_sheet, meetings)
        self.__write_user_data(xlsx_sheet, meetings, report)
        self.__hide_columns(xlsx_sheet)
        self.xlsx_file.close()

    def __write_user_data(self, worksheet, meetings, report_list):
        row = 1
        for user_record_tuple in report_list:
            user_data = [user_record_tuple[1][key] for key in self.user_header_fields]
            worksheet.write_row(row, 0, user_data)
            self.__write_results_formulas(worksheet, row, meetings)
            for meeting_report in user_record_tuple[1]['meetings_report']:
                duration_mins = round(user_record_tuple[1]['meetings_report'][meeting_report]['duration'] / 60, 1)
                col = self.meetings_data_start_col + meetings.index(meeting_report)
                worksheet.write(row, col, duration_mins)
                worksheet.write(
                    row + 1, col, user_record_tuple[1]['meetings_report'][meeting_report]['entry_exit'],
                    self.format_text_wrap
                )
                worksheet.set_column(row + 1, col, len(DATE_TIME_FORMAT) + 3)
            worksheet.set_row(row + 1, None, None, {'hidden': True})
            row += 2

    def __write_results_formulas(self, worksheet, row, meetings):
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
        formula = '=COUNTIF({}:{},">{}")'.format(
            meetings_start_cell,
            meetings_end_cell,
            self.configuration.MIN_MINUTES_FOR_ATTENDANCE
        )
        worksheet.write(row, self.no_of_presents_col, formula)
        # No. of absents formula
        formula = '=COUNTBLANK({}:{})'.format(meetings_start_cell, meetings_end_cell)
        worksheet.write(row, self.no_of_absents_col, formula)

    def __write_headers(self, worksheet, meetings):
        for idx, user_header in enumerate(self.user_header_fields):
            get_header = {
                'id': "Zoom Id",
                'user_email': "Email Address",
                'name': "Name",
            }
            data = get_header.get(user_header, user_header)
            worksheet.write(0, idx, data, self.format_align_center_bold)
        worksheet.write_row(0, len(self.user_header_fields), self.result_header_fields, self.format_align_center_bold)
        for idx, meeting in enumerate(meetings):
            meeting_date_obj = utils.to_date_time(self.configuration.UTC_TIME_DIFFERENCE, meeting)
            day = calendar.day_name[meeting_date_obj.weekday()]
            data = 'Attended time (Mins)\n{}\n{}'.format(str(meeting_date_obj), day)
            worksheet.write(0, self.meetings_data_start_col + idx, data, self.format_align_center_bold)

    def __hide_columns(self, worksheet):
        first_col = self.user_header_fields.index('id')
        last_col = self.user_header_fields.index('user_email')
        worksheet.set_column(first_col, last_col, None, None, {'hidden': True})
