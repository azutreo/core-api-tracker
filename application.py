import json
from urllib.request import urlopen
import core_api_types.classes as core_classes
import core_api_types.namespaces as core_namespaces
import core_api_types.enums as core_enums


PAGE_LINK = "https://docs.coregames.com/assets/api/CoreLuaAPI.json"

FILE_DUMP_TEXT = "dumps/core_api_dump.txt"
FILE_DUMP_JSON = "dumps/core_api_dump.json"
FILE_DIFFERENCE_TEXT = "dumps/core_api_difference.txt"

KEY = '''\n\n[color=#e0e0e0]**Changed**[/color]
[color=#4caf50]**Added**[/color]
[color=#f44336]**Removed**[/color]

[color=#1976d2]**Class**[/color]
[color=#80cbc4]**Property**[/color]
[color=#ffd54f]**Event**[/color]
[color=#f48fb1]**MemberFunction**[/color]
[color=#42a5f5]**Constructor**[/color]
[color=#9fa8da]**Constant**[/color]
[color=#f48fb1]**StaticFunction**[/color]
[color=#ff0000]***\[Tag\]***[/color]
[color=#c8e6c9]*Parameter*[/color]
[color=#795548]*Type*[/color]

[color=#ad1457]**Namespace**[/color]
[color=#f48fb1]**StaticFunction**[/color]

[color=#7b1fa2]**Enum**[/color]
[color=#ba68c8]**Value**[/color] [color=#e1bee7]VALUE[/color][color=#9e9e9e]: NUM[/color]'''


def get_file_contents(filename):
	file = open(filename, "r")
	contents = file.read()
	file.close()

	return contents


def is_same(dump):
	contents = get_file_contents(FILE_DUMP_TEXT)

	return dump == contents


def write_contents(contents):
	textDump = open(FILE_DUMP_TEXT, "w")
	textDump.write(contents)
	textDump.close()


def get_json_parsed_data(url):
	response = urlopen(url)
	data = response.read().decode("utf-8")
	return json.loads(data), data


def main():
	# See if the API has changed AT ALL
	'''response = urlopen(PAGE_LINK)
	pageContents = str(response.read())

	if is_same(pageContents):
		return
	
	write_contents(pageContents)'''

	# Grab the old/new json required for comparisons
	newJsonData, newJsonText = get_json_parsed_data(PAGE_LINK)
	oldJsonText = get_file_contents(FILE_DUMP_JSON)
	oldJsonData = json.loads(oldJsonText)

	# DIFFERENCES IN CLASSES
	classDifferences = core_classes.GetDifferences(newJsonData, oldJsonData)
	classSequence = []
	for classDifference in classDifferences:
		classSequence.append(classDifference + "\n")
	if len(classSequence) >= 1:
		classSequence.append("\n")

	# DIFFERENCES IN NAMESPACES
	namespaceDifferences = core_namespaces.GetDifferences(newJsonData, oldJsonData)
	namespaceSequence = []
	for namespaceDifference in namespaceDifferences:
		namespaceSequence.append(namespaceDifference + "\n")
	if len(namespaceSequence) >= 1:
		namespaceSequence.append("\n")

	# DIFFERENCES IN ENUMS
	enumDifferences = core_enums.GetDifferences(newJsonData, oldJsonData)
	enumSequence = []
	for enumDifference in enumDifferences:
		enumSequence.append(enumDifference + "\n")

	# Begin the differences file
	differencesTextFile = open(FILE_DIFFERENCE_TEXT, "w")
	differencesTextFile.write("")
	
	# Write the sequences collected above
	differencesTextFile.writelines(classSequence + namespaceSequence + enumSequence + [KEY])

	# Close the differences text file
	differencesTextFile.close()

	# Set the "new" to be what was grabbed from online
	newJsonFile = open(FILE_DUMP_JSON, "w")
	newJsonFile.write(newJsonText)
	newJsonFile.close()


if __name__ == "__main__":
	main()
