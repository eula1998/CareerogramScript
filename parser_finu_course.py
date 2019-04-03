from xlrd import open_workbook
from dbparser import DBParser
from ru_course_translation import translate, categorize

def change(i):
    if i == ',' or i == ';':# or i == '.':
        return '|'
    if i == '|':
        return '/'
    return i

class FinUCourseParser(DBParser):
    def __init__(self, filename):
        super().__init__(filename)
        self.courses = []
        # self.courses_lookup = {}

    def parse(self):
        wb = open_workbook(self.filename)
        # skipping the header row
        sheet = wb.sheet_by_index(0)
        for row_idx in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(row_idx)]
            # row index, course name, topics/skills
            self.parseRow(str(row_idx), row[2], row[4])
        # TODO deal with subjects and disciplines
        # del self.tags[""]

    def parseRow(self, key, course_name, skills):
        skills = self.parseTags(skills, change, translate)
        self.courses.append(("FinU", key, course_name, skills))
        # self.courses_lookup[course_number] = ("FinU", course_number, course_name, skills)
