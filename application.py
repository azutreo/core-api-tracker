import json
import pathlib
import warnings
import os, sys

from time import strftime, gmtime, sleep
from urllib.request import urlopen

import core_api_types.classes as CoreClasses
import core_api_types.namespaces as CoreNamespaces
import core_api_types.enums as CoreEnums

from git import Repo


CORE_API_URL = "https://docs.coregames.com/assets/api/CoreLuaAPI.json"
REPOSITORY_URL = "https://github.com/azutreo/core-api-tracker.git"

FILE_DUMP_TEXT = "internal_dumps/core_api_dump.txt"
FILE_DUMP_JSON = "internal_dumps/core_api_dump.json"

COMMIT_MESSAGE = "Update to Core API: %s"


def list_files(start_path):
	for root, dirs, files in os.walk(start_path):
		level = root.replace(start_path, '', 1).count(os.sep)
		indent = ' ' * 4 * (level)
		print('{}{}/'.format(indent, os.path.basename(root)))
		sub_indent = ' ' * 4 * (level + 1)
		for f in files:
			print('{}{}'.format(sub_indent, f))


list_files(str(pathlib.Path().absolute()))
sys.stdout.flush()


repository = Repo(pathlib.Path().absolute())
origin = repository.remote(name='origin')

with repository.config_writer() as git_config:
	git_config.set_value('user', 'email', 'nicholas.w.foreman@outlook.com')
	git_config.set_value('user', 'name', 'azutreo')


def PushToRepository(datetimeGMT):
	if True:
		return

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


def GetJsonParsedData(response):
	data = response.read().decode("utf-8")
	return json.loads(data), data


def Main():
	# See if the API has changed AT ALL
	response = urlopen(CORE_API_URL)
	pageContents = str(response.read())

	isSame = IsSame(pageContents)
	if isSame:
		return

	WriteDumpText(pageContents)

	# Grab the old/new json required for comparisons
	newJsonData, newJsonText = GetJsonParsedData(response)
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
