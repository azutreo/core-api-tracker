def get_differences(newJson, oldJson):
	differences = []

	def add(difference, type, value):
		differences.append({
			"difference": difference,
			"type": type,
			"value": value
		})

	def get_namespace(list, namespaceName):
		for namespace in list["Namespaces"]:
			if namespace["Name"] == namespaceName:
				return namespace

	def get_namespace_staticfunction(list, namespaceName, staticFunctionName):
		namespace = get_namespace(list, namespaceName)
		for staticFunction in namespace["StaticFunctions"]:
			if staticFunction["Name"] == staticFunctionName:
				return staticFunction

	def get_parameter_format(signature):
		return "(" + (", ").join(
			("[{} {}]" if "IsOptional" in parameter else "{} {}").format(
				parameter["Type"] if "Type" in parameter else "void",
				parameter["Name"]) for parameter in signature["Parameters"]
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

	def get_return_type(returns):
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


	for namespace in newJson["Namespaces"]:
		if not oldJson["Namespaces"]:
			add("Added", "Namespace", namespace["Name"])

			for staticFunction in namespace["StaticFunctions"]:
				for signature in staticFunction["Signatures"]:
					parameterFormat = get_parameter_format(signature)
					add("\tAdded", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)

			continue

		oldNamespace = get_namespace(oldJson, namespace["Name"])
		if oldNamespace:
			wasChanged = False

			for staticFunction in namespace["StaticFunctions"]:
				oldStaticFunction = get_namespace_staticfunction(oldJson, namespace["Name"], staticFunction["Name"])
				
				if oldStaticFunction:
					for signature in staticFunction["Signatures"]:
						if not signature in oldStaticFunction["Signatures"]:
							if not wasChanged:
								add("Changed", "Namespace", namespace["Name"])
								wasChanged = True
							parameterFormat = get_parameter_format(signature)
							add("\tAdded", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)
				else:
					for signature in staticFunction["Signatures"]:
						if not wasChanged:
							add("Changed", "Namespace", namespace["Name"])
							wasChanged = True
						parameterFormat = get_parameter_format(signature)
						add("\tAdded", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)
		else:
			add("Added", "Namespace", namespace["Name"])

			for staticFunction in namespace["StaticFunctions"]:
				for signature in staticFunction["Signatures"]:
					parameterFormat = get_parameter_format(signature)
					add("\tAdded", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)

	for namespace in oldJson["Namespaces"]:
		if not newJson["Namespaces"]:
			add("Removed", "Namespace", namespace["Name"])

			for staticFunction in namespace["StaticFunctions"]:
				for signature in staticFunction["Signatures"]:
					parameterFormat = get_parameter_format(signature)
					add("\tRemoved", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)

			continue

		newNamespace = get_namespace(newJson, namespace["Name"])
		if newNamespace:
			wasChanged = False

			for staticFunction in namespace["StaticFunctions"]:
				newStaticFunction = get_namespace_staticfunction(newJson, namespace["Name"], staticFunction["Name"])

				if newStaticFunction:
					for signature in staticFunction["Signatures"]:
						if not signature in newStaticFunction["Signatures"]:
							if not wasChanged:
								add("Changed", "Namespace", namespace["Name"])
								wasChanged = True
							parameterFormat = get_parameter_format(signature)
							add("\tRemoved", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)
				else:
					for signature in staticFunction["Signatures"]:
						if not wasChanged:
							add("Changed", "Namespace", namespace["Name"])
							wasChanged = True
						parameterFormat = get_parameter_format(signature)
						add("\tRemoved", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)
		else:
			add("Removed", "Namespace", namespace["Name"])

			for staticFunction in namespace["StaticFunctions"]:
				for signature in staticFunction["Signatures"]:
					parameterFormat = get_parameter_format(signature)
					add("\tRemoved", "StaticFunction", get_return_type(signature["Returns"]) + " " + namespace["Name"] + "." + staticFunction["Name"] + parameterFormat)

	return differences
