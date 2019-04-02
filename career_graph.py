import csv
import networkx as nx
categories = ["data scientist", "artificial intelligence", "machine learning", "software engineer", "firmware engineering"]

class Node:
    def __init__(self, name):
        self.name = name

class JobNode(Node):
    def __init__(self, category, company, job_title):
        self.category = category
        self.company = company
        self.job_title = job_title
        key = category + ";" + company + ";" + job_title
        super().__init__(key)
        self.preferred = []
        self.minimum = []
        self.required = []
        self.responsibility = []

class SkillNode(Node):
    def __init__(self, name):
        super().__init__(name, category)
        self.jobs = []
        self.courses = []
        self.category = category

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

class CareerGraph():

    def __init__(self):
        self.job_nodes = {}
        self.skill_nodes = {}
        self.course_nodes = {}

########################################################
# IMPORTS DATA
########################################################
    # import data structure
    # job_list: (category, company, job_title, list_of_responsibility, list_of_minimum, list_of_preferred, list_of_required)
    # course_list: (school, course number, course name, skills)

    def import_job(self, job_list):
        for j in job_list:
            jn = JobNode(j[0], j[1], j[2])
            # responsibilities
            for t in j[3]:
                self.add_skill_from_job(jn, jn.responsibility, t)
            # minimum
            for t in j[4]:
                self.add_skill_from_job(jn, jn.minimum, t)
            # preferred
            for t in j[5]:
                self.add_skill_from_job(jn, jn.preferred, t)
            # required
            for t in j[6]:
                self.add_skill_from_job(jn, jn.required, t)
            self.job_nodes[jn.name] = jn

        if "" in self.skill_nodes:
            del self.skill_nodes[""]

    def import_courses(self, course_list):
        for c in course_list:
            cn = CourseNode(c[0], c[1], c[2])
            for t in c[3]:
                self.add_skill_from_course(cn, cn.skills, t)
            self.course_nodes[cn.name] = cn

        if "" in self.skill_nodes:
            del self.skill_nodes[""]

########################################################
# PRIVATE FUNCTIONS
########################################################

    def add_skill(self, list_to_be_added, skill):
        if skill not in self.skill_nodes:
            sn = SkillNode(skill)
            self.skill_nodes[skill] = sn
        else:
            sn = self.skill_nodes[skill]
        list_to_be_added.append(sn)
        return sn

    def add_skill_from_course(self, course, list_to_be_added, skill):
        sn = self.add_skill(list_to_be_added, skill)
        sn.courses.append(course)

    def add_skill_from_job(self, job, list_to_be_added, skill):
        sn = self.add_skill(list_to_be_added, skill)
        sn.jobs.append(job)


########################################################
# STATISTICS STUFFS
########################################################
    def calculate_skill_category_distribution_csv(self):
        l = []
        row = ["skill", "total"]
        row.extend(categories)
        l.append(row)

        keys = list(self.skill_nodes.keys())
        keys.sort()
        for t in keys:
            sn = self.skill_nodes[t]
            row = [sn.name]
            row.append(len(sn.jobs))
            for c in categories:
                row.append(sn.count_category(c))
            l.append(row)
        return l

        # for index.html and graph.json
        # formatted according to this tutorial , credited to Konstya for finding it
        # https://bl.ocks.org/mbostock/ad70335eeef6d167bc36fd3c04378048
        # not sure how to format this thingy, interactive enough though
    def output_json_3djs(self):
        file = []
        file.append("{")
        file.append("\t\"nodes\": [")
        for s in self.skill_nodes:
            file.append("\t\t{{\"id\": \"{}\", \"group\": 1}},".format(self.skill_nodes[s].name))
        for s in self.course_nodes:
            file.append("\t\t{{\"id\": \"{}\", \"group\": 2}},".format(self.course_nodes[s].name))
        for s in self.job_nodes:
            file.append("\t\t{{\"id\": \"{}\", \"group\": 3}},".format(self.job_nodes[s].name))
        file.append("],")
        file.append("\t\"links\": [")
        for s in self.skill_nodes:
            for j in self.skill_nodes[s].jobs:
                file.append("\t\t{{\"source\": \"{}\", \"target\": \"{}\", \"value\": 1}},".format(s, j.name))
            for c in self.skill_nodes[s].courses:
                file.append("\t\t{{\"source\": \"{}\", \"target\": \"{}\", \"value\": 1}},".format(s, c.name))
        file.append("\t]")
        file.append("}")
        return file

# formatted according to this tutorial:
# http://jonathansoma.com/lede/algorithms-2017/classes/networks/networkx-graphs-from-source-target-dataframe/
    # def output_csv_edges(self):
    #     file = []
    #     file.append(("skill", "entity"))
    #     for s in self.skill_nodes:
    #         for j in self.skill_nodes[s].jobs:
    #             file.append((s, j.name))
    #         for c in self.skill_nodes[s].courses:
    #             file.append((s, c.name))
    #     return file


    def drawNetworkXGraph(self):
        G = nx.Graph()
        coursenodes = self.course_nodes.keys()
        skillnodes = self.skill_nodes.keys()
        jobnodes = self.job_nodes.keys()
        pass
