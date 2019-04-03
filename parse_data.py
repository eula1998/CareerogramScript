from xlrd import open_workbook
import csv
from career_graph import CareerGraph
from parser_us_job import UsJobParser
from parser_russian_job import RussianJobParser
from parser_wpi_course import WpiCourseParser
from parser_finu_course import FinUCourseParser

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

def printDict(dict):
    keys = list(dict.keys())
    keys.sort()
    for e in keys:
        print(e, ",", dict[e])

# def labelTags(tags, filename):
#     wb = open_workbook(filename)
#     sheet = wb.sheet_by_index(0)
#     cats = {}
#
#     for row_idx in range(1, sheet.nrows):
#         row = [cell.value for cell in sheet.row(row_idx)]
#         row[0] = row[0].lstrip().rstrip()
#         cats[row[0]] = row[1].lower().lstrip().rstrip()


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

finu_course_parser = FinUCourseParser("FinU Tracks.xlsx")
finu_course_parser.parse()
finu_course_tags = finu_course_parser.tags
finu_courses = finu_course_parser.courses

# printDict(finu_course_tags) # py parse_data.py > ru_job_data/finu_course_tags.csv

# labelTags(job_tags, "US Job Glossary.xlsx")


#------------------------------------------------------
# MAKE GRAPH from job list
#------------------------------------------------------
careergraph = CareerGraph()
careergraph.import_jobs(job_list=us_job_parser.jobs)
careergraph.import_jobs(job_list=ru_job_parser.jobs)
careergraph.import_courses(course_list=wpi_course_parser.courses)
careergraph.import_courses(course_list=finu_course_parser.courses)
careergraph.set_up_skill_dataframe(make_csv=False)
top20 = careergraph.top_20_skills(make_csv=False)

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
