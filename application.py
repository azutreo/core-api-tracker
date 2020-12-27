import json
from urllib.request import urlopen
import core_enum


PAGE_LINK = "https://docs.coregames.com/assets/api/CoreLuaAPI.json"

FILE_DUMP_TEXT = "core_api_dump.txt"
FILE_DUMP_JSON = "core_api_dump.json"
FILE_DIFFERENCE_TEXT = "core_api_difference.txt"


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

	# DIFFERENCES IN ENUMS
	enumDifferences = core_enum.get_differences(newJsonData, oldJsonData)
	enumSequence = []
	for enumDifference in enumDifferences:
		enumSequence.append("%s %s %s\n" % (enumDifference["difference"], enumDifference["type"], enumDifference["value"]))

	# Begin the differences file
	differencesTextFile = open(FILE_DIFFERENCE_TEXT, "w")
	differencesTextFile.write("")
	
	# Write the sequences collected above
	differencesTextFile.writelines(enumSequence)

	# Close the differences text file
	differencesTextFile.close()

	# Set the "new" to be what was grabbed from online
	newJsonFile = open(FILE_DUMP_JSON, "w")
	newJsonFile.write(newJsonText)
	newJsonFile.close()


if __name__ == "__main__":
	main()
