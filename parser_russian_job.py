from xlrd import open_workbook
from dbparser import DBParser
from ru_job_tag_translation import translate, categorize

def change(i):
    if i == ',' or i == ';':# or i == '.':
        return '|'
    if i == '|':
        return '/'
    return i

class RussianJobParser(DBParser):
    def __init__(self, filename):
        super().__init__(filename)
        self.jobs = []

    def parse(self):
        wb = open_workbook(self.filename)
        # finds the second sheet
        sheet = wb.sheet_by_index(1)

        # skipping the header row
        for row_idx in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(row_idx)]
            # category, company, job_title, salary, responsibility, minimum, preferred, required
            self.parseRow(row[0], row[1], row[2], row[3], row[8], row[9], row[10], row[11])

        # del self.tags[""]

    def parseRow(self, category, company, job_title, salary, responsibility, minimum, preferred, required):
        # parse responsibility
        responsibility = self.parseTags(responsibility, change, translate)
        # parse minimum
        minimum = self.parseTags(minimum, change, translate)
        # parse preferred
        preferred = self.parseTags(preferred, change, translate)
        # parse required
        required = self.parseTags(required, change, translate)
        #(category, company, job_title, list_of_responsibility, list_of_minimum, list_of_preferred, list_of_required)
        self.jobs.append(("ru", category.lower(), company.lower(), job_title.lower(), salary.lower(), responsibility, minimum, preferred, required))
