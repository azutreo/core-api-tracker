import json


def AddEnum(differences: list, enumName: str):
	differences.append("Added Enum " + enumName)


def RemoveEnum(differences: list, enumName: str):
	differences.append("Removed Enum " + enumName)


def ChangeEnum(differences: list, enumName: str):
	differences.append("Changed Enum " + enumName)


def AddEnumValue(differences: list, value: dict):
	differences.append("\tAdded Value "
		+ value["Name"] + ": " + str(value["Value"]))


def RemoveEnumValue(differences: list, value: dict):
	differences.append("\tRemoved Value "
		+ value["Name"] + ": " + str(value["Value"]))


def GetEnumByName(enums: list, enumName: str):
	for enum in enums["Enums"]:
		if enum["Name"] == enumName:
			return enum


def GetEnumValueByName(enum: dict, valueName: str):
	for value in enum["Values"]:
		if value["Name"] == valueName:
			return value


def AddAllEnumDifferences(differences: list, addedOrRemoved: bool, enum: dict):
	if addedOrRemoved:
		AddEnum(differences, enum["Name"])
	else:
		RemoveEnum(differences, enum["Name"])

	for value in enum["Values"]:
		if addedOrRemoved:
			AddEnumValue(differences, value)
		else:
			RemoveEnumValue(differences, value)


def CompareToOtherList(differences: list, enum: dict, otherList: list, addedOrRemoved: bool):
	if not otherList["Enums"]:
		return AddAllEnumDifferences(differences, addedOrRemoved, enum)

	otherEnum = GetEnumByName(otherList, enum["Name"])
	if otherEnum:
		wasChanged = False
		
		for value in enum["Values"]:
			otherValue = GetEnumValueByName(otherEnum, value["Name"])
			if otherValue:
				continue

			if not wasChanged:
				wasChanged = True
				ChangeEnum(differences, enum["Name"])

			if addedOrRemoved:
				AddEnumValue(differences, value)
			else:
				RemoveEnumValue(differences, value)
	else:
		AddAllEnumDifferences(differences, addedOrRemoved, enum)


def CompareLists(differences: list, list1: list, list2: list, addedOrRemoved: bool):
	for enum in list1["Enums"]:
		CompareToOtherList(differences, enum, list2, addedOrRemoved)


def GetDifferences(list1: list, list2: list):
	differences = []

	CompareLists(differences, list1, list2, True)
	CompareLists(differences, list2, list1, False)

	return differences
