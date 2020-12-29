def AddEnum(differences, enumName):
	differences.append("Added Enum " + enumName)

def RemoveEnum(differences, enumName):
	differences.append("Removed Enum " + enumName)

def ChangeEnum(differences, enumName):
	differences.append("Changed Enum " + enumName)

def AddEnumValue(differences, value):
	differences.append("\tAdded Value " + value["Name"] + ": " + str(value["Value"]))

def RemoveEnumValue(differences, value):
	differences.append("\tRemoved Value " + value["Name"] + ": " + str(value["Value"]))

def GetEnumByName(enums, enumName):
	for enum in enums["Enums"]:
		if enum["Name"] == enumName:
			return enum

def GetEnumValueByName(enum, valueName):
	for value in enum["Values"]:
		if value["Name"] == valueName:
			return value

def AddAllEnumDifferences(differences, addedOrRemoved, enum):
	if addedOrRemoved:
		AddEnum(differences, enum["Name"])
	else:
		RemoveEnum(differences, enum["Name"])

	for value in enum["Values"]:
		if addedOrRemoved:
			AddEnumValue(differences, value)
		else:
			RemoveEnumValue(differences, value)

def CompareEnumLists(differences, list1, list2, addedOrRemoved):
	for enum in list1["Enums"]:
		if not list2["Enums"]:
			AddAllEnumDifferences(differences, addedOrRemoved, enum)
			
			continue

		otherEnum = GetEnumByName(list2, enum["Name"])
		if otherEnum:
			for value in enum["Values"]:
				otherValue = GetEnumValueByName( otherEnum, value["Name"])

				if otherValue:
					continue

				wasChanged = False
				if not wasChanged:
					wasChanged = True
					ChangeEnum(differences, enum["Name"])
				
				if addedOrRemoved:
					AddEnumValue(differences, value)
				else:
					RemoveEnumValue(differences, value)
		else:
			AddAllEnumDifferences(differences, addedOrRemoved, enum)

def GetDifferences(list1, list2):
	differences = []

	CompareEnumLists(differences, list1, list2, True)
	CompareEnumLists(differences, list2, list1, False)

	return differences
