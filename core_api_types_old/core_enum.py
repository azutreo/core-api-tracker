def get_differences(newJson, oldJson):
	differences = []

	def add(difference, type, value):
		differences.append({
			"difference": difference,
			"type": type,
			"value": value
		})

	def get_enum(list, enumName):
		for enum in list["Enums"]:
			if enum["Name"] == enumName:
				return enum

	def get_enum_value(list, enumName, valueName):
		enum = get_enum(list, enumName)
		for value in enum["Values"]:
			if value["Name"] == valueName:
				return value

	for enum in newJson["Enums"]:
		if not oldJson["Enums"]:
			add("Added", "Enum", enum["Name"])

			for value in enum["Values"]:
				add("\tAdded", "Value", value["Name"] + ": " + str(value["Value"]))

			continue

		oldEnum = get_enum(oldJson, enum["Name"])
		if oldEnum:
			for value in enum["Values"]:
				oldValue = get_enum_value(oldJson, enum["Name"], value["Name"])

				wasChanged = False
				if not oldValue:
					if not wasChanged:
						add("Changed", "Enum", enum["Name"])
						wasChanged = True

					add("\tAdded", "Value", value["Name"] + ": " + str(value["Value"]))
		else:
			add("Added", "Enum", enum["Name"])

			for value in enum["Values"]:
				add("\tAdded", "Value", value["Name"] + ": " + str(value["Value"]))

	for enum in oldJson["Enums"]:
		if not newJson["Enums"]:
			add("Removed", "Enum", enum["Name"])

			for value in enum["Values"]:
				add("\tRemoved", "Value", value["Name"] + ": " + str(value["Value"]))

			continue

		newEnum = get_enum(newJson, enum["Name"])
		if newEnum:
			for value in enum["Values"]:
				newValue = get_enum_value(newJson, enum["Name"], value["Name"])

				wasChanged = False
				if not newValue:
					if not wasChanged:
						add("Changed", "Enum", enum["Name"])
						wasChanged = True

					add("\tRemoved", "Value", value["Name"] + ": " + str(value["Value"]))
		else:
			add("Removed", "Enum", enum["Name"])

			for value in enum["Values"]:
				add("\tRemoved", "Value", value["Name"] + ": " + str(value["Value"]))

	return differences
