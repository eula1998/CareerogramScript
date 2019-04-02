position = "survey_data/Position.txt"
industry = "survey_data/Industry.txt"
company = "survey_data/Company.txt"
second_major = "survey_data/Second_Major.txt"
experience = "survey_data/Experience.txt"

def parseCSV(filename):
	s = {}
	with open(filename, 'r') as fd:
		for l in fd:
			fields = l.split(',')
			for term in fields:
				t = term.lower().lstrip().rstrip()
				if t in s:
					s[t] += 1
				else:
					s[t] = 1
	for term in s:
		print(term, ", ", s[term])


print("========================")
print("Position")
print("========================")
parseCSV(position)
print()

print("========================")
print("Industry")
print("========================")
parseCSV(industry)
print()

print("========================")
print("Company")
print("========================")
parseCSV(company)
print()

print("========================")
print("Experience")
print("========================")
parseCSV(experience)
print()

print("========================")
print("Second Major")
print("========================")
parseCSV(second_major)
print()
