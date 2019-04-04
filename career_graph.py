import networkx as nx
import pandas as pd
import math

categories = ["data scientist", "artificial intelligence", "machine learning", "software engineer", "firmware engineering"]

def initialize_df_cell_and_incr(df, index, col):
    # the dataframe is initialized to nan
    if math.isnan(df.at[index, col]):
        df.at[index, col] = 0
    df.at[index, col] = df.at[index, col] + 1

class Node:
    def __init__(self, name):
        self.name = name

class JobNode(Node):
    def __init__(self, country, category, company, job_title):
        self.country = country
        self.category = category
        self.company = company
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

class CareerGraph():

    def __init__(self):
        self.job_nodes = {}
        self.skill_nodes = {}
        self.course_nodes = {}
        self.skill_df = None
        self.job_nodes_by_category = None


########################################################
# IMPORTS DATA
########################################################
    # import data structure
    # job_list: (country, category, company, job_title, list_of_responsibility, list_of_minimum, list_of_preferred, list_of_required)
    # course_list: (school, course number, course name, skills)

    def import_jobs(self, job_list):
        for j in job_list:
            jn = JobNode(j[0], j[1], j[2], j[3])
            # responsibilities
            for t in j[4]:
                self.add_skill_from_job(jn, jn.responsibility, t)
            # minimum
            for t in j[5]:
                self.add_skill_from_job(jn, jn.minimum, t)
            # preferred
            for t in j[6]:
                self.add_skill_from_job(jn, jn.preferred, t)
            # required
            for t in j[7]:
                self.add_skill_from_job(jn, jn.required, t)
            self.job_nodes[jn.name] = jn


    def import_courses(self, course_list):
        for c in course_list:
            cn = CourseNode(c[0], c[1], c[2])
            for t in c[3]:
                self.add_skill_from_course(cn, cn.skills, t)
            self.course_nodes[cn.name] = cn


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

    def set_up_skill_dataframe(self, make_csv=False):
        # if self.skill_df != None:
        #     print("WARNING: You are recalculating the dataframe." +
        #     "This may be wasted resources if the graph has not been changed")

        # order of the category variable
        # currently ds, ai, ml, se, fe
        self.job_nodes_by_category = {}
        job_count_by_category = {}
        for c in categories:
            self.job_nodes_by_category["us " + c] = [self.job_nodes[k] for k in self.job_nodes
                                if (self.job_nodes[k].country == "us" and self.job_nodes[k].category == c)]
            self.job_nodes_by_category["ru " + c] = [self.job_nodes[k] for k in self.job_nodes
                                if (self.job_nodes[k].country == "ru" and self.job_nodes[k].category == c)]
            job_count_by_category["us " + c] = [len(self.job_nodes_by_category["us " + c])]
            job_count_by_category["ru " + c] = [len(self.job_nodes_by_category["ru " + c])]

        # columns with raw data
        columns = []
        scat = ["minimum", "preferred", "required", "responsibility"]
        country = ["ru", "us"]

        for sc in scat:
            for cat in categories:
                for c in country:
                    columns.append(c + " " + cat + " " + sc)

        df = pd.DataFrame(index=self.skill_nodes.keys(), columns=columns, dtype=int)

        for c in categories:
            for j in self.job_nodes_by_category["ru " + c]:
                for s in j.minimum:
                    initialize_df_cell_and_incr(df, s.name, "ru " + c + " minimum")
                for s in j.preferred:
                    initialize_df_cell_and_incr(df, s.name, "ru " + c + " preferred")
                for s in j.responsibility:
                    initialize_df_cell_and_incr(df, s.name, "ru " + c + " responsibility")
                for s in j.required:
                    initialize_df_cell_and_incr(df, s.name, "ru " + c + " required")
            for j in self.job_nodes_by_category["us " + c]:
                for s in j.minimum:
                    initialize_df_cell_and_incr(df, s.name, "us " + c + " minimum")
                for s in j.preferred:
                    initialize_df_cell_and_incr(df, s.name, "us " + c + " preferred")
                for s in j.responsibility:
                    initialize_df_cell_and_incr(df, s.name, "us " + c + " responsibility")
                for s in j.required:
                    initialize_df_cell_and_incr(df, s.name, "us " + c + " required")

        # columns produced using the raw data
        combined = {
            "us data scientist": ["us data scientist minimum", "us data scientist preferred", "us data scientist required", "us data scientist responsibility"],
            "us artificial intelligence": ["us artificial intelligence minimum", "us artificial intelligence preferred", "us artificial intelligence required", "us artificial intelligence responsibility"],
            "us firmware engineering": ["us firmware engineering minimum", "us firmware engineering preferred", "us firmware engineering required", "us firmware engineering responsibility"],
            "us software engineer": ["us software engineer minimum", "us software engineer preferred", "us software engineer required", "us software engineer responsibility"],
            "us machine learning": ["us machine learning minimum", "us machine learning preferred", "us machine learning required", "us machine learning responsibility"],
            "ru data scientist": ["ru data scientist minimum", "ru data scientist preferred", "ru data scientist required", "ru data scientist responsibility"],
            "ru artificial intelligence": ["ru artificial intelligence minimum", "ru artificial intelligence preferred", "ru artificial intelligence required", "ru artificial intelligence responsibility"],
            "ru firmware engineering": ["ru firmware engineering minimum", "ru firmware engineering preferred", "ru firmware engineering required", "ru firmware engineering responsibility"],
            "ru software engineer": ["ru software engineer minimum", "ru software engineer preferred", "ru software engineer required", "ru software engineer responsibility"],
            "ru machine learning": ["ru machine learning minimum", "ru machine learning preferred", "ru machine learning required", "ru machine learning responsibility"],
            "artificial intelligence": ["us artificial intelligence", "ru artificial intelligence"],
            "data scientist": ["us data scientist", "ru data scientist"],
            "software engineer": ["us software engineer", "ru software engineer"],
            "machine learning": ["us machine learning", "ru machine learning"],
            "firmware engineering": ["ru firmware engineering", "us firmware engineering"],
            "ru": ["ru data scientist", "ru artificial intelligence", "ru firmware engineering", "ru software engineer", "ru machine learning"],
            "us": ["us data scientist", "us artificial intelligence", "us firmware engineering", "us software engineer", "us machine learning"],
            "all": ["us", "ru"],
        }
        for c in combined:
            df[c] = df[combined[c]].sum(axis=1)

        # sort the columns by name
        df = df.reindex(sorted(df.columns), axis=1)
        if make_csv:
            df.to_csv(path_or_buf="./combined_data/skill_count.csv", index=True)
            temp_df = pd.DataFrame(job_count_by_category)
            temp_df.to_csv(path_or_buf="./combined_data/job_count.csv", index=False)

        self.skill_df = df


    # outputs the top 20 skills for each category and each skill column
    # returns a dictionary of which the key = column heading, containing the 20
    # skills that occur in a column most frequently
    def top_20_skills(self, make_csv=False):
        # TODO ValueError:The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
        # if self.skill_df == None:
        #     self.set_up_skill_dataframe()

        top20 = {}
        # retrieves the list of columns
        for c in list(self.skill_df.columns.values):
            temp_df = self.skill_df.sort_values(c, axis=0, ascending=False, kind='quicksort', na_position='last')
            top20[c] = list(temp_df.head(20).index.values)
            # filter out the skills that do not exist in that category
            top20[c] = [s for s in top20[c] if not math.isnan(temp_df.at[s, c]) and temp_df.at[s, c] != 0 and s != "" and s != '']

        if make_csv:
            for c in top20:
                while len(top20[c]) < 20:
                    top20[c].append(None)
            temp_df = pd.DataFrame(top20)
            temp_df.to_csv(path_or_buf="./combined_data/top20.csv", index=False)
        return top20


    # percentage of jobs need the skill in each categories
    def top_20_distribution(self, make_csv=True, top20=None):
        if top20 == None:
            top20 = self.top_20_skills()
        for c in top20:
            while len(top20[c]) < 20:
                top20[c].append(None)

        temp_df = pd.DataFrame(top20)

        columns = {}
        # skill category
        scat = ["minimum", "preferred", "required", "responsibility"]
        country = ["ru", "us"]
        for sc in scat:
            for cat in categories:
                for c in country:
                    columns[c + " " + cat + " " + sc] = c + " " + cat + " " + sc + " distribution"

        for c in columns:
            temp_df[columns[c]] = 0.0

        for c in columns:
            for i in range(len(temp_df.index.values)):
                # temp_df.at[i, columns[c]] = 1
                if temp_df.at[i, c] != None:
                    # percentage = numberOfSkillsInThatCategory / number_of_jobs_in_that_job_category
                    temp_df.at[i, columns[c]] = self.skill_df.at[temp_df.at[i, c], c] / len(self.job_nodes_by_category[c.rsplit(' ', 1)[0]])

        for c in categories:
            temp_df[c + " distribution"] = 0.0
            for i in range(len(temp_df.index.values)):
                if temp_df.at[i, c] != None:
                    temp_df.at[i, c + " distribution"] = self.skill_df.at[temp_df.at[i, c], c] / (len(self.job_nodes_by_category["ru " + c]) + len(self.job_nodes_by_category["us " + c]))

        # sort the columns by name
        temp_df = temp_df.reindex(sorted(temp_df.columns), axis=1)

        if make_csv:
            temp_df.to_csv(path_or_buf="./combined_data/top20_percentage.csv", index=False)



    def drawNetworkXGraph(self):
        top20 = self.top_20_skills()
        G = nx.Graph()
        # skills = self.skill_nodes.keys()
        edges = []
        for c in categories:
            skills = top20[c]
            for s in skills:
                for c in self.skill_nodes[s].courses:
                    edges.append((s, c.name))
                for j in self.skill_nodes[s].jobs:
                    edges.append((s, j.name))
        G.add_edges_from(edges)
        # layout = nx.spring_layout(G,iterations=50)
        # print(nx.info(G))
        # nx.draw_networkx(G)





                # for index.html and graph.json
                # formatted according to this tutorial , credited to Konstya for finding it
                # https://bl.ocks.org/mbostock/ad70335eeef6d167bc36fd3c04378048
                # not sure how to format this thingy, interactive enough though
            # def output_json_3djs(self):
            #     file = []
            #     file.append("{")
            #     file.append("\t\"nodes\": [")
            #     for s in self.skill_nodes:
            #         file.append("\t\t{{\"id\": \"{}\", \"group\": 1}},".format(self.skill_nodes[s].name))
            #     for s in self.course_nodes:
            #         file.append("\t\t{{\"id\": \"{}\", \"group\": 2}},".format(self.course_nodes[s].name))
            #     for s in self.job_nodes:
            #         file.append("\t\t{{\"id\": \"{}\", \"group\": 3}},".format(self.job_nodes[s].name))
            #     file.append("],")
            #     file.append("\t\"links\": [")
            #     for s in self.skill_nodes:
            #         for j in self.skill_nodes[s].jobs:
            #             file.append("\t\t{{\"source\": \"{}\", \"target\": \"{}\", \"value\": 1}},".format(s, j.name))
            #         for c in self.skill_nodes[s].courses:
            #             file.append("\t\t{{\"source\": \"{}\", \"target\": \"{}\", \"value\": 1}},".format(s, c.name))
            #     file.append("\t]")
            #     file.append("}")
            #     return file

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
