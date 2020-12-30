import json
import core_api_types.functions as core_functions


def AddClass(differences: list, className: str):
	differences.append("Added Class " + className)
def RemoveClass(differences: list, className: str):
	differences.append("Removed Class " + className)
def ChangeClass(differences: list, className: str):
	differences.append("Changed Class " + className)


def AddStaticFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str):
	differences.append("\tAdded " + "StaticFunction " + returnType + " " + className + "." + functionName + parameterFormat)
def RemoveStaticFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str):
	differences.append("\tRemoved " + "StaticFunction " + returnType + " " + className + "." + functionName + parameterFormat)

def AddMemberFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str):
	differences.append("\tAdded " + "MemberFunction " + returnType + " " + className + ":" + functionName + parameterFormat)
def RemoveMemberFunction(differences: list, returnType: str, className: str, functionName: str, parameterFormat: str):
	differences.append("\tRemoved " + "MemberFunction " + returnType + " " + className + ":" + functionName + parameterFormat)

def GetClassByName(classes: list, className: str):
	for _class in classes["Classes"]:
		if _class["Name"] == className:
			return _class


def GetFunctionByName(_class: dict, functionName: str, _type: str):
	if _type not in _class:
		return
	for function in _class[_type]:
		if function["Name"] == functionName:
			return function


def AddSignature(differences, signature, className: str, functionName: str, isMemberFunction: bool, addedOrRemoved: bool):
	parameterFormat = core_functions.GetParameterFormat(signature)
	returnType = core_functions.GetReturnType(signature["Returns"])
	
	if addedOrRemoved:
		if isMemberFunction:
			AddMemberFunction(differences, returnType, className, functionName, parameterFormat)
		else:
			AddStaticFunction(differences, returnType, className, functionName, parameterFormat)
	else:
		if isMemberFunction:
			RemoveMemberFunction(differences, returnType, className, functionName, parameterFormat)
		else:
			RemoveStaticFunction(differences, returnType, className, functionName, parameterFormat)


def AddAllSignatures(isMemberFunction: bool, differences: list, signatures: dict, className: str, functionName: str, addedOrRemoved: bool):
	for signature in signatures:
		AddSignature(differences, signature, className, functionName, isMemberFunction, addedOrRemoved)


def AddAllStaticFunctions(differences: list, _class: dict, addedOrRemoved: bool):
	if "StaticFunctions" not in _class:
		return
	for staticFunction in _class["StaticFunctions"]:
		AddAllSignatures(False, differences, staticFunction["Signatures"], _class["Name"], staticFunction["Name"], addedOrRemoved)


def AddAllMemberFunctions(differences: list, _class: dict, addedOrRemoved: bool):
	if "MemberFunctions" not in _class:
		return
	for staticFunction in _class["MemberFunctions"]:
		AddAllSignatures(True, differences, staticFunction["Signatures"], _class["Name"], staticFunction["Name"], addedOrRemoved)


def AddAllClassDifferences(differences: list, _class: dict, addedOrRemoved: bool):
	if addedOrRemoved:
		AddClass(differences, _class["Name"])
	else:
		RemoveClass(differences, _class["Name"])
	
	AddAllStaticFunctions(differences, _class, addedOrRemoved)
	AddAllMemberFunctions(differences, _class, addedOrRemoved)


def CompareFunctions(differences: list, functionList: list, _class: dict, otherClass: dict, isMemberFunction: bool, addedOrRemoved: bool, wasChanged: bool):
	for function in functionList:
		otherFunction = None
		if isMemberFunction:
			otherFunction = GetFunctionByName(otherClass, function["Name"], "MemberFunctions")
		else:
			otherFunction = GetFunctionByName(otherClass, function["Name"], "StaticFunctions")
		
		if otherFunction:
			for signature in function["Signatures"]:
				if signature in otherFunction["Signatures"]:
					continue
				
				if not wasChanged:
					wasChanged = True
					ChangeClass(differences, _class["Name"])
				
				AddSignature(differences, signature, _class["Name"], function["Name"], isMemberFunction, addedOrRemoved)
		else:
			if not wasChanged:
				wasChanged = True
				ChangeClass(differences, _class["Name"])
			
			AddAllSignatures(isMemberFunction, differences, function["Signatures"], _class["Name"], function["Name"], addedOrRemoved)
	
	return wasChanged


def CompareToOtherList(differences: list, _class: dict, otherList: list, addedOrRemoved: bool):
	if not otherList["Classes"]:
		return AddAllClassDifferences(differences, _class, addedOrRemoved)
	
	otherClass = GetClassByName(otherList, _class["Name"])
	if otherClass:
		wasChanged = False
		
		if "StaticFunctions" in _class:
			wasChanged = CompareFunctions(differences, _class["StaticFunctions"], _class, otherClass, False, addedOrRemoved, wasChanged)
		if "MemberFunctions" in _class:
			wasChanged = CompareFunctions(differences, _class["MemberFunctions"], _class, otherClass, True, addedOrRemoved, wasChanged)
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
