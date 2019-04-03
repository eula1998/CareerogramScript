from xlrd import open_workbook
from dbparser import DBParser
from us_job_tag_translation import translate, categorize

def change(i):
    if i == '(' or i == ')' or i == '[' or i == ']' or i == ',':
        return '|'
    if i == '|':
        return '/'
    return i

class UsJobParser(DBParser):
    def __init__(self, filename):
        super().__init__(filename)
        self.jobs = []

    def parse(self):
        wb = open_workbook(self.filename)
        # gets the first sheet
        sheet = wb.sheet_by_index(0)
        # skipping the header row
        for row_idx in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(row_idx)]
            # category, company, job_title, responsibility, minimum, preferred, required
            self.parseRow(row[0], row[1], row[2], row[8], row[9], row[10], row[11])

        # del self.tags[""]

    def parseRow(self, category, company, job_title, responsibility, minimum, preferred, required):
        # parse responsibility
        responsibility = self.parseTags(responsibility, change, translate)
        # parse minimum
        minimum = self.parseTags(minimum, change, translate)
        # parse preferred
        preferred = self.parseTags(preferred, change, translate)
        # parse required
        required = self.parseTags(required, change, translate)
        #(category, company, job_title, list_of_responsibility, list_of_minimum, list_of_preferred, list_of_required)
        self.jobs.append(("US", category.lower(), company.lower(), job_title.lower(), responsibility, minimum, preferred, required))
