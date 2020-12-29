def GetParameterFormat(signature):
	return "(" + (", ").join(
			("[{} {}]" if "IsOptional" in parameter else "{} {}").format(
				parameter["Type"] if "Type" in parameter else "void",
				parameter["Name"] if "Name" in parameter else "_")
				for parameter in signature["Parameters"]
			) + ")"
	
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
	return "void" if len(returns) == 0 else ", ".join(
		("..." if "IsVariadic" in returnStatement else returnStatement["Type"]) for returnStatement in returns)
	
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