def GetParameterFormat(signature: dict, left: str, right: str, ignoreName: bool):
	return left + (", ").join(
			("[{} {}]" if "IsOptional" in parameter else "{}{}").format(
				parameter["Type"] if "Type" in parameter else "void",
				(" " + parameter["Name"] if "Name" in parameter else " _") if not ignoreName else "")
				for parameter in signature["Parameters"]
			) + right
	
	'''parameterFormat = "("

	count = 0
	for parameter in signature["Parameters"]:
		count += 1
		
		notNil = "Type" in parameter
		parameterType = str(parameter["Type"] if notNil else "void")

		if "IsOptional" in parameter:
			parameterFormat += "[" + (parameterType + " " + parameter["Name"]) + "]"
		else:
			parameterFormat += (parameterType + " " + parameter["Name"])
		
		if count != len(signature["Parameters"]):
			parameterFormat += ", "

	return parameterFormat + ")"'''


def GetReturnType(returns):
	if "Returns" not in returns:
		return "void"

	return "void" if len(returns["Returns"]) == 0 else ", ".join(
		("..." if "IsVariadic" in returnStatement else returnStatement["Type"]) for returnStatement in returns["Returns"])
	
	'''count = 0
	returnsFormat = ""

	for returnStatement in returns:
		count += 1
		if "IsVariadic" in returnStatement:
			returnsFormat += "..."
		elif "Type" in returnStatement:
			returnsFormat += str(returnStatement["Type"])
		if count != len(returns):
			returnsFormat += ", "

	if count == 0:
		returnsFormat = "void"
	
	return returnsFormat'''
