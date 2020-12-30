import json
import core_api_types.functions as core_functions
import core_api_types.tags as core_tags


def AddClass(differences: list, className: str):
	differences.append("Added Class " + className)
def RemoveClass(differences: list, className: str):
	differences.append("Removed Class " + className)
def ChangeClass(differences: list, className: str):
	differences.append("Changed Class " + className)


def AddStaticFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str, parent: dict):
	differences.append("\tAdded " + "StaticFunction " + returnType + " " + className + "." + functionName + parameterFormat + core_tags.GetTagsFormat(parent))
def RemoveStaticFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str, parent: dict):
	differences.append("\tRemoved " + "StaticFunction " + returnType + " " + className + "." + functionName + parameterFormat + core_tags.GetTagsFormat(parent))

def AddMemberFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str, parent: dict):
	differences.append("\tAdded " + "MemberFunction " + returnType + " " + className + ":" + functionName + parameterFormat + core_tags.GetTagsFormat(parent))
def RemoveMemberFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str, parent: dict):
	differences.append("\tRemoved " + "MemberFunction " + returnType + " " + className + ":" + functionName + parameterFormat + core_tags.GetTagsFormat(parent))

def AddConstructor(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str, parent: dict):
	differences.append("\tAdded " + "Constructor " + returnType + " " + className + "." + functionName + parameterFormat + core_tags.GetTagsFormat(parent))
def RemoveConstructor(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str, parent: dict):
	differences.append("\tRemoved " + "Constructor " + returnType + " " + className + "." + functionName + parameterFormat + core_tags.GetTagsFormat(parent))

def AddProperty(differences: list, className: str, propertyType: str, propertyName: str, parent: dict):
	differences.append("\tAdded " + "Property " + propertyType + " " + className + "." + propertyName + core_tags.GetTagsFormat(parent))
def RemoveProperty(differences: list, className: str, propertyType: str, propertyName: str, parent: dict):
	differences.append("\tRemoved " + "Property " + propertyType + " " + className + "." + propertyName + core_tags.GetTagsFormat(parent))

def AddConstant(differences: list, className: str, constantType: str, constantName: str, parent: dict):
	differences.append("\tAdded " + "Constant " + constantType + " " + className + "." + constantName + core_tags.GetTagsFormat(parent))
def RemoveConstant(differences: list, className: str, constantType: str, constantName: str, parent: dict):
	differences.append("\tRemoved " + "Constant " + constantType + " " + className + "." + constantName + core_tags.GetTagsFormat(parent))

def AddEvent(differences: list, className: str, eventName: str, parameterFormat: str, parent: dict):
	differences.append("\tAdded " + "Event " + className + "." + eventName + parameterFormat + core_tags.GetTagsFormat(parent))
def RemoveEvent(differences: list, className: str, eventName: str, parameterFormat: str, parent: dict):
	differences.append("\tRemoved " + "Event " + className + "." + eventName + parameterFormat + core_tags.GetTagsFormat(parent))

def GetClassByName(classes: list, className: str):
	for _class in classes["Classes"]:
		if _class["Name"] == className:
			return _class


def GetMemberByName(_class: dict, name: str, _type: str):
	if _type not in _class:
		return
	for member in _class[_type]:
		if member["Name"] == name:
			return member


def AddSignature(differences: list, signature: dict, className: str, functionName: str, functionType: int, addedOrRemoved: bool, function: dict):
	parameterFormat = core_functions.GetParameterFormat(signature, "(", ")", False)
	returnType = core_functions.GetReturnType(signature)
	
	if addedOrRemoved:
		if functionType == 0:
			AddMemberFunction(differences, returnType, className, functionName, parameterFormat, function)
		elif functionType == 1:
			AddStaticFunction(differences, returnType, className, functionName, parameterFormat, function)
		elif functionType == 2:
			AddConstructor(differences, returnType, className, functionName, parameterFormat, function)
	else:
		if functionType == 0:
			RemoveMemberFunction(differences, returnType, className, functionName, parameterFormat, function)
		elif functionType == 1:
			RemoveStaticFunction(differences, returnType, className, functionName, parameterFormat, function)
		elif functionType == 2:
			RemoveConstructor(differences, returnType, className, functionName, parameterFormat, function)


def AddAllSignatures(functionType: int, differences: list, signatures: dict, className: str, functionName: str, addedOrRemoved: bool, function: dict):
	for signature in signatures:
		AddSignature(differences, signature, className, functionName, functionType, addedOrRemoved, function)


def AddAllStaticFunctions(differences: list, _class: dict, addedOrRemoved: bool):
	if "StaticFunctions" not in _class:
		return
	for function in _class["StaticFunctions"]:
		AddAllSignatures(1, differences, function["Signatures"], _class["Name"], function["Name"], addedOrRemoved, function)


def AddAllMemberFunctions(differences: list, _class: dict, addedOrRemoved: bool):
	if "MemberFunctions" not in _class:
		return
	for function in _class["MemberFunctions"]:
		AddAllSignatures(0, differences, function["Signatures"], _class["Name"], function["Name"], addedOrRemoved, function)


def AddAllConstructors(differences: list, _class: dict, addedOrRemoved: bool):
	if "Constructors" not in _class:
		return
	for constructor in _class["Constructors"]:
		AddAllSignatures(2, differences, constructor["Signatures"], _class["Name"], constructor["Name"], addedOrRemoved, constructor)


def AddEvent_(differences: list, event: dict, className: str, eventName: str, addedOrRemoved: bool):
	parameterFormat = core_functions.GetParameterFormat(event, "<", ">", True)

	if addedOrRemoved:
		AddEvent(differences, className, eventName, parameterFormat, event)
	else:
		RemoveEvent(differences, className, eventName, parameterFormat, event)


def AddAllEvents(differences: list, _class: dict, addedOrRemoved: bool):
	if "Events" not in _class:
		return
	for event in _class["Events"]:
		AddEvent_(differences, event, _class["Name"], event["Name"], addedOrRemoved)


def AddAllProperties(differences: list, _class: dict, addedOrRemoved: bool):
	if "Properties" not in _class:
		return
	for property in _class["Properties"]:
		if addedOrRemoved:
			AddProperty(differences, _class["Name"], property["Type"], property["Name"], property)
		else:
			RemoveProperty(differences, _class["Name"], property["Type"], property["Name"], property)


def AddAllConstants(differences: list, _class: dict, addedOrRemoved: bool):
	if "Constants" not in _class:
		return
	for constant in _class["Constants"]:
		if addedOrRemoved:
			AddConstant(differences, _class["Name"], constant["Type"], constant["Name"], constant)
		else:
			RemoveConstant(differences, _class["Name"], constant["Type"], constant["Name"], constant)


def AddAllClassDifferences(differences: list, _class: dict, addedOrRemoved: bool):
	if addedOrRemoved:
		AddClass(differences, _class["Name"])
	else:
		RemoveClass(differences, _class["Name"])
	
	AddAllProperties(differences, _class, addedOrRemoved)
	AddAllEvents(differences, _class, addedOrRemoved)
	AddAllMemberFunctions(differences, _class, addedOrRemoved)
	AddAllConstructors(differences, _class, addedOrRemoved)
	AddAllConstants(differences, _class, addedOrRemoved)
	AddAllStaticFunctions(differences, _class, addedOrRemoved)


def CompareFunctions(differences: list, functionList: list, _class: dict, otherClass: dict, functionType: int, addedOrRemoved: bool, wasChanged: bool):
	for function in functionList:
		otherFunction = None
		if functionType == 0:
			otherFunction = GetMemberByName(otherClass, function["Name"], "MemberFunctions")
		elif functionType == 1:
			otherFunction = GetMemberByName(otherClass, function["Name"], "StaticFunctions")
		elif functionType == 2:
			otherFunction = GetMemberByName(otherClass, function["Name"], "Constructors")
		
		if otherFunction:
			for signature in function["Signatures"]:
				if signature in otherFunction["Signatures"]:
					continue
				
				if not wasChanged:
					wasChanged = True
					ChangeClass(differences, _class["Name"])
				
				AddSignature(differences, signature, _class["Name"], function["Name"], functionType, addedOrRemoved, function)
		else:
			if not wasChanged:
				wasChanged = True
				ChangeClass(differences, _class["Name"])
			
			AddAllSignatures(functionType, differences, function["Signatures"], _class["Name"], function["Name"], addedOrRemoved, function)
	
	return wasChanged


def CompareEvents(differences: list, eventList: list, _class: dict, otherClass: dict, addedOrRemoved: bool, wasChanged: bool):
	for event in eventList:
		if ("Events" in otherClass) and (event in otherClass["Events"]):
			continue
		
		if not wasChanged:
			wasChanged = True
			ChangeClass(differences, _class["Name"])
		
		AddEvent_(differences, event, _class["Name"], event["Name"], addedOrRemoved)


def CompareProperties(differences: list, properties: list, _class: dict, otherClass: dict, addedOrRemoved: bool, wasChanged: bool):
	for property in properties:
		if ("Properties" not in otherClass) or (property not in otherClass["Properties"]):
			if addedOrRemoved:
				AddProperty(differences, _class["Name"], property["Type"], property["Name"], property)
			else:
				RemoveProperty(differences, _class["Name"], property["Type"], property["Name"], property)
	
	return wasChanged


def CompareConstants(differences: list, constants: list, _class: dict, otherClass: dict, addedOrRemoved: bool, wasChanged: bool):
	for constant in constants:
		if ("Constants" not in otherClass) or (constant not in otherClass["Constants"]):
			if addedOrRemoved:
				AddConstant(differences, _class["Name"], constant["Type"], constant["Name"], constant)
			else:
				RemoveConstant(differences, _class["Name"], constant["Type"], constant["Name"], constant)
	
	return wasChanged


def CompareToOtherList(differences: list, _class: dict, otherList: list, addedOrRemoved: bool):
	if not otherList["Classes"]:
		return AddAllClassDifferences(differences, _class, addedOrRemoved)
	
	otherClass = GetClassByName(otherList, _class["Name"])
	if otherClass:
		wasChanged = False
		
		if "Properties" in _class:
			wasChanged = CompareProperties(differences, _class["Properties"], _class, otherClass, addedOrRemoved, wasChanged)
		if "Events" in _class:
			wasChanged = CompareEvents(differences, _class["Events"], _class, otherClass, addedOrRemoved, wasChanged)
		if "MemberFunctions" in _class:
			wasChanged = CompareFunctions(differences, _class["MemberFunctions"], _class, otherClass, 0, addedOrRemoved, wasChanged)
		if "Constructors" in _class:
			wasChanged = CompareFunctions(differences, _class["Constructors"], _class, otherClass, 2, addedOrRemoved, wasChanged)
		if "Constants" in _class:
			wasChanged = CompareConstants(differences, _class["Constants"], _class, otherClass, addedOrRemoved, wasChanged)
		if "StaticFunctions" in _class:
			wasChanged = CompareFunctions(differences, _class["StaticFunctions"], _class, otherClass, 1, addedOrRemoved, wasChanged)
	else:
		AddAllClassDifferences(differences, _class, addedOrRemoved)


def CompareLists(differences: list, list1: list, list2: list, addedOrRemoved: bool):
	for _class in list1["Classes"]:
		CompareToOtherList(differences, _class, list2, addedOrRemoved)


def GetDifferences(list1: list, list2: list):
	differences = []
	
	CompareLists(differences, list1, list2, True)
	CompareLists(differences, list2, list1, False)
	
	return differences
