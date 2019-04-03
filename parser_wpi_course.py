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

    def parse(self):
        wb = open_workbook(self.filename)
        # skipping the header row
        for i in range(0, 4):
            sheet = wb.sheet_by_index(i)
            for row_idx in range(1, sheet.nrows):
                row = [cell.value for cell in sheet.row(row_idx)]
                # course nummber, course name, topics/skills
                self.parseRow(row[1], row[2], row[4])
        # TODO deal with subjects and disciplines
        # del self.tags[""]

    def parseRow(self, course_number, course_name, skills):
        skills = self.parseTags(skills, change, translate)
        self.courses.append(("WPI", course_number, course_name, skills))
        self.courses_lookup[course_number] = ("WPI", course_number, course_name, skills)
