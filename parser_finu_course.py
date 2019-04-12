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
        self.courses_lookup = {}
        self.degree_requirement_lookup = {}

    def parse(self):
        wb = open_workbook(self.filename)
        # skipping the header row
        sheet = wb.sheet_by_index(0)
        for row_idx in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(row_idx)]

            if row[0] != "":
                current_degree = row[0]
                self.degree_requirement_lookup[current_degree] = set()

            if row[2] != "":
                # row index, course name, topics/skills
                self.parseRow(str(row_idx), row[2], row[4])
                self.degree_requirement_lookup[current_degree].add(str(row_idx))

    def parseRow(self, key, course_name, skills):
        skills = self.parseTags(skills, change, translate)
        self.courses.append(("finu", key, course_name, skills))
        self.courses_lookup[key] = ("finu", key, course_name, skills)
