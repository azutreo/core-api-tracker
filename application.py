import json
from time import strftime, gmtime, sleep
from urllib.request import urlopen
import warnings
import pathlib

import core_api_types.classes as CoreClasses
import core_api_types.namespaces as CoreNamespaces
import core_api_types.enums as CoreEnums

from git import Repo


API_LINK = "https://docs.coregames.com/assets/api/CoreLuaAPI.json"
REPOSITORY_LINK = "https://github.com/azutreo/core-api-tracker.git"

FILE_DUMP_TEXT = "internal_dumps/core_api_dump.txt"
FILE_DUMP_JSON = "internal_dumps/core_api_dump.json"

COMMIT_MESSAGE = "Update to Core API: %s"


repository = Repo(pathlib.Path().absolute())
origin = repository.remote(name='origin')

with repository.config_writer() as git_config:
	git_config.set_value('user', 'email', 'nicholas.w.foreman@outlook.com')
	git_config.set_value('user', 'name', 'azutreo')


def PushToRepository(datetimeGMT):
	try:
		origin.pull()

		repository.index.add(A=True)
		repository.index.commit(COMMIT_MESSAGE % datetimeGMT)

		origin.push()
	except Exception as e:
		warnings.warn(e, UserWarning)
	else:
		print("Successfully pushed changes: " + datetimeGMT)


def GetFileContents(filename):
	file = open(filename, "r")
	contents = file.read()
	file.close()

	return contents


def IsSame(dump):
	contents = GetFileContents(FILE_DUMP_TEXT)

	return dump == contents


def WriteDumpText(contents):
	textDump = open(FILE_DUMP_TEXT, "w+")
	textDump.write(contents)
	textDump.close()


def GetJsonParsedData(url):
	response = urlopen(url)
	data = response.read().decode("utf-8")
	return json.loads(data), data


def Main():
	# See if the API has changed AT ALL
	response = urlopen(API_LINK)
	pageContents = str(response.read())

	isSame = IsSame(pageContents)
	if isSame:
		return

	WriteDumpText(pageContents)

	# Grab the old/new json required for comparisons
	newJsonData, newJsonText = GetJsonParsedData(PAGE_LINK)
	oldJsonText = GetFileContents(FILE_DUMP_JSON)
	oldJsonData = json.loads(oldJsonText)

	# DIFFERENCES IN CLASSES
	classDifferences = CoreClasses.GetDifferences(newJsonData, oldJsonData)
	classSequence = []
	for classDifference in classDifferences:
		classSequence.append(classDifference + "\n")
	if len(classSequence) >= 1:
		classSequence.append("\n")

	# DIFFERENCES IN NAMESPACES
	namespaceDifferences = CoreNamespaces.GetDifferences(newJsonData, oldJsonData)
	namespaceSequence = []
	for namespaceDifference in namespaceDifferences:
		namespaceSequence.append(namespaceDifference + "\n")
	if len(namespaceSequence) >= 1:
		namespaceSequence.append("\n")

	# DIFFERENCES IN ENUMS
	enumDifferences = CoreEnums.GetDifferences(newJsonData, oldJsonData)
	enumSequence = []
	for enumDifference in enumDifferences:
		enumSequence.append(enumDifference + "\n")

	# Current Time
	datetimeGMT = strftime("%Y-%m-%d", gmtime())

	# Begin the differences file
	differencesTextFile = open("differences/" + datetimeGMT + ".txt", "w+")

	# Write the sequences collected above
	differencesTextFile.writelines(classSequence + namespaceSequence + enumSequence)

	# Close the differences text file
	differencesTextFile.close()

	# Create a dump into api_dumps
	newJsonFile = open("api_dumps/" + datetimeGMT + ".json", "w+")
	newJsonFile.write(newJsonText)
	newJsonFile.close()

	# Set the "new" to be what was grabbed from online
	newJsonFile = open(FILE_DUMP_JSON, "w+")
	newJsonFile.write(newJsonText)
	newJsonFile.close()

	PushToRepository(datetimeGMT)


if __name__ == "__main__":
	print("Running program; close to cancel (Ctrl + C if in console)")
	print(pathlib.Path().absolute())

	Main()
	try:
		while sleep(60):
			Main()
	except(KeyboardInterrupt):
		print("Cancelled program")
