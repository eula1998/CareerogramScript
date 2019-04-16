
class Node:
    def __init__(self, name):
        self.name = name

class JobNode(Node):
    def __init__(self, country, category, salary, company, job_title):
        self.country = country
        self.category = category
        self.company = company
        self.salary = salary
        self.job_title = job_title
        key = country + ";" + category + ";" + company + ";" + job_title
        super().__init__(key)
        # list of skills
        self.preferred = []
        self.minimum = []
        self.required = []
        self.responsibility = []

class SkillNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.jobs = []
        self.courses = []

    def count_category(self, category):
        count = 0
        for j in self.jobs:
            if j.category == category:
                count+=1
        return count #/ len(self.jobs) * 100

class CourseNode(Node):
    def __init__(self, school, course_number, course_name):
        self.school = school
        self.course_number = course_number
        self.course_name = course_name
        key = school + ";" + course_number + ";" + course_name
        super().__init__(key)
        self.skills = []

class CategoryNode(Node):
    def __init__(self, category):
        super().__init__(category)
        self.jobs = []
        self.skills = {}

class DegreeNode(Node):
    def __init__(self, school, degree_name):
        self.school = school
        self.degree_name = degree_name
        key = school + ";" + degree_name
        super().__init__(key)
        self.courses = []
        self.skills = {}
