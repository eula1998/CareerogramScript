import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import math
from node import CourseNode, CategoryNode, SkillNode, JobNode

categories = ["data scientist", "artificial intelligence", "machine learning", "software engineer", "firmware engineering"]

def initialize_df_cell_and_incr(df, index, col):
    # the dataframe is initialized to nan
    if math.isnan(df.at[index, col]):
        df.at[index, col] = 0
    df.at[index, col] = df.at[index, col] + 1

class CareerGraph():

    def __init__(self):
        self.job_nodes = {}
        self.skill_nodes = {}
        self.course_nodes = {}
        self.skill_df = None
        self.job_nodes_by_category = None
        self.category_nodes = {}

########################################################
# IMPORTS DATA
########################################################
    # import data structure
    # job_list: (country, category, company, job_title, list_of_responsibility, list_of_minimum, list_of_preferred, list_of_required)
    # course_list: (school, course number, course name, skills)

    def import_jobs(self, job_list):
        for j in job_list:
            jn = JobNode(country=j[0], category=j[1], company=j[2], job_title=j[3], salary=j[4])

            if j[1] not in self.category_nodes:
                self.category_nodes[j[1]] = CategoryNode(j[1])
            cn = self.category_nodes[j[1]]
            cn.jobs.append(jn)

            # responsibilities
            for t in j[5]:
                self.add_skill_from_job(jn, jn.responsibility, t, cn)
            # minimum
            for t in j[6]:
                self.add_skill_from_job(jn, jn.minimum, t, cn)
            # preferred
            for t in j[7]:
                self.add_skill_from_job(jn, jn.preferred, t, cn)
            # required
            for t in j[8]:
                self.add_skill_from_job(jn, jn.required, t, cn)
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

    def add_skill_from_job(self, job, list_to_be_added, skill, cn):
        sn = self.add_skill(list_to_be_added, skill)

        if skill not in cn.skills:
            cn.skills[skill] = 0
        cn.skills[skill] += 1

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
    def top_skills(self, count=20, make_csv=False, columns=None):
        # TODO ValueError:The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
        # if self.skill_df == None:
        #     self.set_up_skill_dataframe()
        if columns == None:
            columns = list(self.skill_df.columns.values)

        top = {}
        # retrieves the list of columns
        for c in [cl for cl in columns if cl in list(self.skill_df.columns.values)]:
            temp_df = self.skill_df.sort_values(c, axis=0, ascending=False, kind='quicksort', na_position='last')
            top[c] = list(temp_df.head(count).index.values)
            # filter out the skills that do not exist in that category
            top[c] = [s for s in top[c] if not math.isnan(temp_df.at[s, c]) and temp_df.at[s, c] != 0 and s != "" and s != '']

        if make_csv:
            for c in top:
                while len(top[c]) < count:
                    top[c].append(None)
            temp_df = pd.DataFrame(top)
            temp_df.to_csv(path_or_buf="./combined_data/top%s.csv" %(str(count)), index=False)
        return top


    # percentage of jobs need the skill in each categories
    def top_20_distribution(self, make_csv=True, top20=None):
        if top20 == None:
            top20 = self.top_skills(20)
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

        return top20

    def generate_sql_csv(self):
        files = {}
        # category: name
        files["category"] = []
        category_id_lookup = {}
        id = 0
        for c in categories:
            category_id_lookup[c] = id
            id += 1
        row = ["id", "name"]
        files["category"].append(row)
        for c in categories:
            row = [category_id_lookup[c], c]
            files["category"].append(row)

        # jobs: id, name, company, salary, category_id
        files["job"] = []
        job_id_lookup = {}
        id = 0
        for j in self.job_nodes:
            job_id_lookup[j] = id
            id+=1
        row = ["id", "name", "company", "salary", "category_id"]
        files["job"].append(row)

        for j in self.job_nodes:
            jn = self.job_nodes[j]
            row = [job_id_lookup[j], jn.job_title, jn.company, jn.salary, category_id_lookup[jn.category]]
            files["job"].append(row)

        # skill: name
        files["skill"] = []
        skill_id_lookup = {}
        id = 0
        for s in self.skill_nodes:
            skill_id_lookup[s] = id
            id += 1
        row = ["id", "name"]
        files["skill"].append(row)

        for s in self.skill_nodes:
            row = [skill_id_lookup[s], s]
            files["skill"].append(row)

        # course: name, school
        files["course"] = []
        course_id_lookup = {}
        id = 0
        for c in self.course_nodes:
            course_id_lookup[c] = id
            id += 1
        row = ["id", "name", "school"]
        files["course"].append(row)

        for c in self.course_nodes:
            cn = self.course_nodes[c]
            row = [course_id_lookup[c], cn.course_name, cn.school]
            files["course"].append(row)

        # job_minimum_requirement: id_job, id_skill
        files["job_minimum_requirement"] = []
        row = ["id_job", "id_skill"]
        files["job_minimum_requirement"].append(row)
        for j in self.job_nodes:
            jn = self.job_nodes[j]
            for s in jn.minimum:
                row = [job_id_lookup[j], skill_id_lookup[s.name]]
                files["job_minimum_requirement"].append(row)

        # job_preferred_requirement: id_job, id_skill
        files["job_preferred_requirement"] = []
        row = ["id_job", "id_skill"]
        files["job_preferred_requirement"].append(row)
        for j in self.job_nodes:
            jn = self.job_nodes[j]
            for s in jn.preferred:
                row = [job_id_lookup[j], skill_id_lookup[s.name]]
                files["job_preferred_requirement"].append(row)

        # job_required_experience: id_job, id_skill
        files["job_required_experience"] = []
        row = ["id_job", "id_skill"]
        files["job_required_experience"].append(row)
        for j in self.job_nodes:
            jn = self.job_nodes[j]
            for s in jn.required:
                row = [job_id_lookup[j], skill_id_lookup[s.name]]
                files["job_required_experience"].append(row)

        # job_responsibility: id_job, id_skill
        files["job_responsibility"] = []
        row = ["id_job", "id_skill"]
        files["job_responsibility"].append(row)
        for j in self.job_nodes:
            jn = self.job_nodes[j]
            for s in jn.responsibility:
                row = [job_id_lookup[j], skill_id_lookup[s.name]]
                files["job_responsibility"].append(row)

        # category_all_requirement: id_category, id_skill
        files["category_all_requirement"] = []
        row = ["id_category", "id_skill"]
        files["category_all_requirement"].append(row)
        for c in self.category_nodes:
            cn = self.category_nodes[c]
            for s in cn.skills:
                row = [category_id_lookup[c], skill_id_lookup[s]]
                files["category_all_requirement"].append(row)

        # course_skill: id_course, id_skill
        files["course_skill"] = []
        row = ["id_course", "id_skill"]
        files["course_skill"].append(row)
        for c in self.course_nodes:
            cn = self.course_nodes[c]
            for s in cn.skills:
                row = [course_id_lookup[c], skill_id_lookup[s.name]]
                files["course_skill"].append(row)

        return files


    def make_summary_csv(self):
        keys = list(self.skill_nodes.keys())
        keys.sort()
        file = {}

        all_list = []
        row = ["country + company + job title", "category"]
        row.extend(keys)
        all_list.append(row)
        for c in categories:
            l = []
            row = ["country + company + job title", "category"]
            row.extend(keys)
            l.append(row)
            for j in self.job_nodes:
                j = self.job_nodes[j]
                if j.category == c:
                    row = [j.country + ";" + j.company + ";" + j.job_title, j.category]
                    for e in keys:
                            row.append(1 if self.skill_nodes[e] in j.responsibility else 0)
                    l.append(row)
                    all_list.append(row)

                    row = [j.country + ";" + j.company + ";" + j.job_title, j.category]
                    for e in keys:
                            row.append(1 if self.skill_nodes[e] in j.minimum else 0)
                    l.append(row)
                    all_list.append(row)

                    row = [j.country + ";" + j.company + ";" + j.job_title, j.category]
                    for e in keys:
                            row.append(1 if self.skill_nodes[e] in j.preferred else 0)
                    l.append(row)
                    all_list.append(row)

                    row = [j.country + ";" + j.company + ";" + j.job_title, j.category]
                    for e in keys:
                            row.append(1 if self.skill_nodes[e] in j.required else 0)
                    l.append(row)
                    all_list.append(row)
            file[c] = l
        file["job_tag_summary"] = all_list
        return file


# tutorial: http://jonathansoma.com/lede/algorithms-2017/classes/networks/networkx-graphs-from-source-target-dataframe/
    def drawNetworkXGraph(self):
        top = self.top_skills(count=30, columns=categories)
        G = nx.Graph()
        edges = []

        all_nodes = set()
        all_nodes.update(["c:" + c for c in categories])

        for c in self.category_nodes:
            cn = self.category_nodes[c]
            for s in cn.skills:
                if s in top[c]:
                    edges.append((s, "c:" + c))
                    all_nodes.add(s)
        G.add_edges_from(edges)

        skill_size = {}
        for c in top:
            for s in top[c]:
                if s not in skill_size:
                    skill_size[s] = 0
                skill_size[s] += self.category_nodes[c].skills[s]

        plt.figure(figsize=(12, 12))
        # layout = nx.shell_layout(G, nlist=[["c:" + c for c in categories], list(skill_size.keys())])
        layout = nx.kamada_kawai_layout(G)

        nx.draw_networkx_edges(G, layout, width=1, edge_color="#cccccc")

        # draw category nodes
        category_size = [len(self.category_nodes[c].skills) * 15 for c in categories]
        nodes = nx.draw_networkx_nodes(G,
                       layout,
                       nodelist=["c:" + c for c in categories],
                       node_size=category_size,
                       node_color='lightblue')
        nodes.set_edgecolor('#888888')


        # draw frequent skill nodes, size based on frequency of appearances
        frequent_skills = [s for s in skill_size if G.degree(s) > 1]
        frequent_skills_size = [skill_size[s] * 10 for s in frequent_skills]
        nodes = nx.draw_networkx_nodes(G,
                                    layout,
                                    nodelist=frequent_skills,
                                    node_color='#fc8d62',
                                    node_size=frequent_skills_size)
        nodes.set_edgecolor('#888888')
        frequent_skills_edges = G.edges(frequent_skills)
        nx.draw_networkx_edges(G, layout, edgelist=frequent_skills_edges, width=1, edge_color="#bbbbbb")


        #draw remaining skill nodes
        remaining_skills = [s for s in skill_size if G.degree(s) == 1]
        remaining_skills_size = [skill_size[s] * 20 for s in remaining_skills]
        nodes = nx.draw_networkx_nodes(G,
                                    layout,
                                    nodelist=remaining_skills,
                                    node_size=remaining_skills_size,
                                    node_color='#cccccc')
        nodes.set_edgecolor('#888888')

        nx.draw_networkx_labels(G, layout, font_size=8)

        plt.axis('off')
        plt.show()
