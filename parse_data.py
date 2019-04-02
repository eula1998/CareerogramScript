from xlrd import open_workbook
import csv
from career_graph import CareerGraph
from parser_us_job import UsJobParser
from parser_russian_job import RussianJobParser
from parser_wpi_course import WpiCourseParser

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

def labelTags(tags, filename):
    wb = open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    cats = {}

    for row_idx in range(1, sheet.nrows):
        row = [cell.value for cell in sheet.row(row_idx)]
        row[0] = row[0].lstrip().rstrip()
        cats[row[0]] = row[1].lower().lstrip().rstrip()
        # if row[0] not in tags:
        #     print("not a valid tag: ", "\"{}\"".format(row[0]))
    # for e in tags:
    #     if e not in cats:
    #         print("not labeled: ", e)

    # for e in cats:
    #     print("\"{}\" : \"{}\",".format(e, cats[e]))

    # s = set()
    # for e in cats:
    #     # print("\"{}\" : \"{}\",".format(e, cats[e]))
    #     s.add(cats[e])
    # for e in s:
    #     print(e)

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

# wpi_course_parser = WpiCourseParser("WPI Tracks.xlsx")
# wpi_course_parser.parse()
# wpi_course_tags = wpi_course_parser.tags
# wpi_courses = wpi_course_parser.courses

printDict(ru_job_tags)
# printDict(wpi_course_tags)

# labelTags(job_tags, "US Job Glossary.xlsx")



# count = 0
# for t in job_tags:
#     if t in wpi_course_tags:
#         # print(t)
#         count +=1
#
# print()
# print("number of job tags: ", len(job_tags))
# print("number of course tags:", len(wpi_course_tags))
# print("number of overlap: ", count)
# print("percentage: ", count / len(job_tags))
# print()


#------------------------------------------------------
# PRINT tag frequency
#------------------------------------------------------
# for e in keys:
#     print(e, ",", wpi_course_tags[e])


#------------------------------------------------------
# MAKE GRAPH from job list
#------------------------------------------------------
careergraph = CareerGraph()
# careergraph.import_job(job_list=us_job_parser.jobs)
# careergraph.import_courses(course_list=wpi_course_parser.courses)
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
