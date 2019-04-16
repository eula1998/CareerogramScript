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
def writeToCSVs(directory, dict):
    for k in dict:
        filename = "%s/%s.csv" %(directory, k.replace(" ","_"))
        writeToCSV(filename=filename, list=dict[k])

def writeToCSV(filename, list):
    with open(filename, 'w+', newline='', encoding="utf-8") as file:
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
finu_courses_lookup = finu_course_parser.courses_lookup
finu_degrees = finu_course_parser.degree_requirement_lookup


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
careergraph.import_degrees(school="wpi", degree_list=wpi_degrees, course_lookup=wpi_courses_lookup)
careergraph.import_degrees(school="finu", degree_list=finu_degrees, course_lookup=finu_courses_lookup)
careergraph.set_up_job_skill_dataframe(make_csv=False)
careergraph.set_up_course_skill_dataframe(make_csv=False)

# top20 = careergraph.top_skills(count=21)
# writeToCSV("us_job_data/job_tag_distribution.csv", careergraph.calculate_skill_category_distribution_csv())
# writeToCSVs("combined_data", careergraph.make_summary_csv())
# writeToCSVs("sql_files", careergraph.generate_sql_csv())
# careergraph.drawJobSkillNetworkXGraph()
careergraph.drawDegreeSkillNetworkXGraph(top_count=10)

#------------------------------------------------------
# Combined Analysis
#------------------------------------------------------
# finu_degrees_skills = {}
# for d in finu_degrees:
#     finu_degrees_skills[d] = set()
#     for c in finu_degrees[d]:
#         c = finu_courses_lookup[c]
#         skills = c[3]
#         finu_degrees_skills[d].update(skills)
#
# temp_df = careergraph.skill_df.copy()
#
# ## py -3 parse_data.py > combined_data/wpi_job_match.txt
# for c in categories:
#     # c = "data scientist"
#     l = temp_df.index[temp_df[c] > 0].tolist()
#     print("total number of skills in " + c + ": " + str(len(l) - 1))
#
#     for d in finu_degrees_skills:
#         count = 0
#         print("===================================")
#         for s in finu_degrees_skills[d]:
#             if s in l and s != "":
#                 print(s)
#                 count+=1
#         print("total matched skills of " + d + " at FinU: " + str(count), "\t", str(count/len(l)))
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#
#
# print("Top 20 skills")
# for c in categories:
#     l = top20[c]
#     print(c)
#     for d in finu_degrees_skills:
#         count = 0
#         print("===================================")
#         for s in finu_degrees_skills[d]:
#             if s in l and s != "":
#                 print(s)
#                 count+=1
#         print("total matched skills of " + d + " at FinU: " + str(count), "\t", str(count/len(l)))
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


#------------------------------------------------------
# Metrics
#------------------------------------------------------
# job_count = len(careergraph.job_nodes)
# skill_count = len(careergraph.skill_nodes)
# course_count = len(careergraph.course_nodes)
# tag_count = 0
# for i in list(careergraph.skill_df.index.values):
#     tag_count += careergraph.skill_df.at[i, "all"]
#
# print("We gathered: ")
# print("\t", job_count, "jobs from two countries in", len(categories), "different categories")
# print("\t", course_count, "courses from two schools, out of which",
#     len(wpi_courses_lookup), "from WPI, and", len(finu_courses_lookup), "from Financial University")
# print("\t", int(tag_count), "tags, out of which", skill_count, "are unique skills")
