from xlrd import open_workbook
from dbparser import DBParser
from us_course_translation import translate, categorize

def change(i):
    if i == ',' or i == ';':# or i == '.':
        return '|'
    if i == '|':
        return '/'
    return i

class WpiCourseParser(DBParser):
    def __init__(self, filename):
        super().__init__(filename)
        self.courses = []
        self.courses_lookup = {}
        self.degree_requirement_lookup = {}

    def parse(self):
        wb = open_workbook(self.filename)
        # skipping the header row
        for i in range(0, 4):
            sheet = wb.sheet_by_index(i)
            for row_idx in range(1, sheet.nrows):
                row = [cell.value for cell in sheet.row(row_idx)]
                # course nummber, course name, topics/skills
                self.parseRow(row[1], row[2], row[4])

        first_page = []
        sheet = wb.sheet_by_index(0)
        for row_idx in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(row_idx)]
            if row[1] != "":
                first_page.append(row[1])

        sheet = wb.sheet_by_index(1)
        program = None
        for row_idx in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(row_idx)]
            if row[0] != "" and not row[0].endswith("(*)"):
                if program != None:
                    self.degree_requirement_lookup[program].update(first_page)
                program = row[0]
                self.degree_requirement_lookup[program] = set()
            if row[1] != "":
                self.degree_requirement_lookup[program].add(row[1])
        self.degree_requirement_lookup[program].update(first_page)

        for i in range(2, 4):
            sheet = wb.sheet_by_index(i)
            for row_idx in range(1, sheet.nrows):
                row = [cell.value for cell in sheet.row(row_idx)]
                if row[0] != "" and not row[0].endswith("(*)"):
                    program = row[0]
                    self.degree_requirement_lookup[program] = set()
                if row[1] != "":
                    self.degree_requirement_lookup[program].add(row[1])

    def parseRow(self, course_number, course_name, skills):
        skills = self.parseTags(skills, change, translate)
        self.courses.append(("wpi", course_number, course_name, skills))
        self.courses_lookup[course_number] = ("wpi", course_number, course_name, skills)
