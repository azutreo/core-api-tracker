import json
import pathlib
import warnings
import os
import shutil

from time import strftime, gmtime, sleep
from urllib.request import urlopen

import core_api_types.classes as CoreClasses
import core_api_types.namespaces as CoreNamespaces
import core_api_types.enums as CoreEnums

from git import Repo


CORE_API_URL = "https://docs.coregames.com/assets/api/CoreLuaAPI.json"

FILE_DUMP_TEXT = "internal_dumps/core_api_dump.txt"
FILE_DUMP_JSON = "internal_dumps/core_api_dump.json"

COMMIT_MESSAGE = "Update to Core API: %s"


repository = Repo(str(pathlib.Path().absolute()))
origin = repository.remote(name='origin')

with repository.config_writer() as git_config:
	git_config.set_value('user', 'email', 'nicholas.w.foreman@outlook.com')
	git_config.set_value('user', 'name', 'azutreo')


def PushToRepository(datetimeGMT):
	try:
		repository.git.add(A=True)
		repository.index.commit(COMMIT_MESSAGE % datetimeGMT)

		origin.pull()
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


def GetJsonParsedData(content):
	# data = content.decode("UTF-8")
	return json.loads(content)


def Main():
	# See if the API has changed AT ALL
	response = urlopen(CORE_API_URL)
	pageContents = response.read().decode("UTF-8")

	if IsSame(pageContents):
		return

	WriteDumpText(pageContents)

	# Grab the old/new json required for comparisons
	newJsonData = json.loads(pageContents)
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

	# Create differences file
	differencesTextFile = open("differences/" + datetimeGMT + ".txt", "w+")
	differencesTextFile.writelines(classSequence + namespaceSequence + enumSequence)
	differencesTextFile.close()

	# Create a dump into api_dumps
	newJsonFile = open("api_dumps/" + datetimeGMT + ".json", "w+")
	newJsonFile.write(pageContents)
	newJsonFile.close()

	# Set the "new" to be what was grabbed from online
	newJsonFile = open(FILE_DUMP_JSON, "w+")
	newJsonFile.write(pageContents)
	newJsonFile.close()

	PushToRepository(datetimeGMT)


if __name__ == "__main__":
	print("Running program; close to cancel (Ctrl + C if in console)")

	Main()
	try:
		while sleep(60):
			Main()
	except(KeyboardInterrupt):
		print("Cancelled program")
