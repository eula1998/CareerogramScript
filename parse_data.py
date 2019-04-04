from xlrd import open_workbook
import csv
from career_graph import CareerGraph
from parser_us_job import UsJobParser
from parser_russian_job import RussianJobParser
from parser_wpi_course import WpiCourseParser
from parser_finu_course import FinUCourseParser
# import pandas as pd

categories = ["data scientist", "artificial intelligence", "machine learning", "software engineer", "firmware engineering"]

#####################################################
# Functions
#####################################################
def writeToCSV(filename, list):
    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file, delimiter = ",")
        # each row should be a tuple, maybe works with lists
        for row in list:
            writer.writerow(row)

def printDict(dict, separation=False):
    keys = list(dict.keys())
    keys.sort()
    for e in keys:
        print(e, ",", dict[e])
        if separation:
            print("========================================")


def labelTags(tags, filename):
    wb = open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    cats = {}

    for row_idx in range(1, sheet.nrows):
        row = [cell.value for cell in sheet.row(row_idx)]
        row[0] = row[0].lstrip().rstrip()
        cats[row[0]] = row[1].lower().lstrip().rstrip()
        if row[0] not in tags:
            print("not a valid tag: ", row[0])

    for t in tags:
        if t not in cats:
            print("not labeled: ", t)



#######################################################
# Main Script
#######################################################

#------------------------------------------------------
# PARSE spreadsheets
#------------------------------------------------------
us_job_parser = UsJobParser('US Jobs.xlsx')
us_job_parser.parse()
us_job_tags = us_job_parser.tags
us_jobs = us_job_parser.jobs

ru_job_parser = RussianJobParser('Russian Jobs.xlsx')
ru_job_parser.parse()
ru_job_tags = ru_job_parser.tags
ru_jobs = ru_job_parser.jobs

wpi_course_parser = WpiCourseParser("WPI Tracks.xlsx")
wpi_course_parser.parse()
wpi_course_tags = wpi_course_parser.tags
wpi_courses = wpi_course_parser.courses
wpi_courses_lookup = wpi_course_parser.courses_lookup
wpi_degrees = wpi_course_parser.degree_requirement_lookup

finu_course_parser = FinUCourseParser("FinU Tracks.xlsx")
finu_course_parser.parse()
finu_course_tags = finu_course_parser.tags
finu_courses = finu_course_parser.courses


# printDict(finu_course_tags) # py parse_data.py > ru_job_data/finu_course_tags.csv

# labelTags(us_job_tags, "US Job Glossary.xlsx")
# labelTags(wpi_course_tags, "WPI Tracks Glossary.xlsx")

# printDict(wpi_degrees_skills, separation=True)

#------------------------------------------------------
# MAKE GRAPH from job list and to analysis
#------------------------------------------------------
careergraph = CareerGraph()
careergraph.import_jobs(job_list=us_job_parser.jobs)
careergraph.import_jobs(job_list=ru_job_parser.jobs)
careergraph.import_courses(course_list=wpi_course_parser.courses)
careergraph.import_courses(course_list=finu_course_parser.courses)
careergraph.set_up_skill_dataframe(make_csv=False)
# top20 = careergraph.top_20_distribution()



#------------------------------------------------------
# Combined Analysis
#------------------------------------------------------
# wpi_degrees_skills = {}
# for d in wpi_degrees:
#     wpi_degrees_skills[d] = set()
#     for c in wpi_degrees[d]:
#         c = wpi_courses_lookup[c]
#         skills = c[3]
#         wpi_degrees_skills[d].update(skills)
#
# temp_df = careergraph.skill_df.copy()
#
# # py -3 parse_data.py > combined_data/ds_wpi_match.txt
# c = "data scientist"
# l = temp_df.index[temp_df[c] > 0].tolist()
# print("total number of skills in " + c + ": " + str(len(l)))
#
# for d in wpi_degrees_skills:
#     count = 0
#     print("===================================")
#     for s in wpi_degrees_skills[d]:
#         if s in l:
#             print(s)
#             count+=1
#     print("total matched skills of " + d + " at WPI: " + str(count), "\t", str(count/len(l) * 100) + "%")

#------------------------------------------------------
# Metrics
#------------------------------------------------------
job_count = len(careergraph.job_nodes)
skill_count = len(careergraph.skill_nodes)
course_count = len(careergraph.course_nodes)
tag_count = 0
for i in list(careergraph.skill_df.index.values):
    tag_count += careergraph.skill_df.at[i, "all"]

# print(len(wpi_courses_lookup))
# print(len(finu_courses))
print("We gathered: ")
print("\t", job_count, "jobs from two countries in", len(categories), "different categories")
print("\t", course_count, "courses from two schools, out of which",
    len(wpi_courses_lookup), "from WPI, and", len(finu_courses), "from Financial University")
print("\t", int(tag_count), "tags, out of which", skill_count, "are unique skills")

# careergraph.drawNetworkXGraph()


# file = careergraph.output_csv_edges()
# writeToCSV("us_job_data/edges.csv", file)
# json = careergraph.output_json_3djs()
# for e in json:
#     print(e)
# printDict(careergraph.skill_nodes)
# writeToCSV("us_job_data/job_tag_distribution.csv", careergraph.calculate_skill_category_distribution_csv())


#------------------------------------------------------
# WRITES us job output TO CSV FILES
#------------------------------------------------------
# keys = list(job_tags.keys())
# keys.sort()
# for c in categories:
#     filename = "us_job_data/%s.csv" %(c.replace(" ","_"))
#     list = []
#     row = ["company", "job title", "skill type"]
#     row.extend(keys)
#     list.append(row)
#     for j in jobs:
#         if j[0] == c:
#             row = [j[1], j[2], "responsibility"]
#             for e in keys:
#                     row.append(1 if e in j[3] else '')
#             list.append(row)
#
#             row = [j[1], j[2], "minimum requirement"]
#             for e in keys:
#                     row.append(1 if e in j[4] else '')
#             list.append(row)
#
#             row = [j[1], j[2], "preferred requirement"]
#             for e in keys:
#                     row.append(1 if e in j[5] else '')
#             list.append(row)
#
#             row = [j[1], j[2], "required experience"]
#             for e in keys:
#                     row.append(1 if e in j[6] else '')
#             list.append(row)
#     writeToCSV(filename, list)
#
# with open("us_job_data/%s.csv" %("job_tag_summary"), 'w+', newline='') as file:
#     writer = csv.writer(file, delimiter = ",")
#     row = ["company", "job title", "skill type"]
#     row.extend(keys)
#     writer.writerow(row)
#     for j in jobs:
#         row = [j[1], j[2], "responsibility"]
#         for e in keys:
#             row.append(1 if e in j[3] else '')
#         writer.writerow(row)
#
#         row = [j[1], j[2], "minimum requirement"]
#         for e in keys:
#             row.append(1 if e in j[4] else '')
#         writer.writerow(row)
#
#         row = [j[1], j[2], "preferred requirement"]
#         for e in keys:
#             row.append(1 if e in j[5] else '')
#         writer.writerow(row)
#
#         row = [j[1], j[2], "required experience"]
#         for e in keys:
#             row.append(1 if e in j[6] else '')
#         writer.writerow(row)
