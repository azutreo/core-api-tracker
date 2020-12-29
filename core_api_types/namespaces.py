import json
import core_api_types.functions as functions


def AddNamespace(differences: list, namespaceName: str):
	differences.append("Added Namespace " + namespaceName)


def RemoveNamespace(differences: list, namespaceName: str):
	differences.append("Removed Namespace " + namespaceName)


def ChangeNamespace(differences: list, namespaceName: str):
	differences.append("Changed Namespace " + namespaceName)


def AddStaticFunction(differences: list, returnType: str, namespaceName: str, staticFunctionName: str, parameterFormat: str):
	differences.append("\tAdded " + "StaticFunction " + returnType + " " + namespaceName + "." + staticFunctionName + parameterFormat)


def RemoveStaticFunction(differences: list, returnType: str, namespaceName: str, staticFunctionName: str, parameterFormat: str):
	differences.append("\tRemoved " + "StaticFunction " + returnType + " " + namespaceName + "." + staticFunctionName + parameterFormat)


def GetNamespaceByName(namespaces: list, namespaceName: str):
	for enum in namespaces["Namespaces"]:
		if enum["Name"] == namespaceName:
			return enum


def GetStaticFunctionByName(namespace: dict, staticFunctionName: str):
	for staticFunction in namespace["StaticFunctions"]:
		if staticFunction["Name"] == staticFunctionName:
			return staticFunction


def AddAllSignatures(differences: list, signatures: dict, namespaceName: str, staticFunctionName: str, addedOrRemoved: bool):
	for signature in signatures:
		parameterFormat = functions.GetParameterFormat(signature)
		returnType = functions.GetReturnType(signature["Returns"])
		
		if addedOrRemoved:
			AddStaticFunction(differences, returnType, namespaceName, staticFunctionName, parameterFormat)
		else:
			RemoveStaticFunction(differences, returnType, namespaceName, staticFunctionName, parameterFormat)


def AddAllStaticFunctions(differences: list, namespace: dict, addedOrRemoved: bool):
	for staticFunction in namespace["StaticFunctions"]:
		AddAllSignatures(differences, staticFunction["Signatures"], namespace["Name"], staticFunction["Name"], addedOrRemoved)


def AddAllNamespaceDifferences(differences: list, namespace: dict, addedOrRemoved: bool):
	if addedOrRemoved:
		AddNamespace(differences, namespace["Name"])
	else:
		RemoveNamespace(differences, namespace["Name"])
	
	AddAllStaticFunctions(differences, namespace, addedOrRemoved)


def CompareToOtherList(differences: list, namespace: dict, otherList: list, addedOrRemoved: bool):
	if not otherList["Namespaces"]:
		return AddAllNamespaceDifferences(differences, namespace, addedOrRemoved)
	
	otherNamespace = GetNamespaceByName(otherList, namespace["Name"])
	if otherNamespace:
		wasChanged = False
		
		for staticFunction in namespace["StaticFunctions"]:
			otherStaticFunction = GetStaticFunctionByName(otherNamespace, staticFunction["Name"])
			
			if otherStaticFunction:
				for signature in staticFunction["Signatures"]:
					if signature in otherStaticFunction["Signatures"]:
						continue
					
					if not wasChanged:
						wasChanged = True
						ChangeNamespace(differences, namespace["Name"])
					
					parameterFormat = functions.GetParameterFormat(signature)
					returnType = functions.GetReturnType(signature["Returns"])
					
					if addedOrRemoved:
						AddStaticFunction(differences, returnType, namespace["Name"], staticFunction["Name"], parameterFormat)
					else:
						RemoveStaticFunction(differences, returnType, namespace["Name"], staticFunction["Name"], parameterFormat)
			else:
				if not wasChanged:
					wasChanged = True
					ChangeNamespace(differences, namespace["Name"])
				
				AddAllSignatures(differences, staticFunction["Signatures"], namespace["Name"], staticFunction["Name"], addedOrRemoved)
	else:
		AddAllNamespaceDifferences(differences, namespace, addedOrRemoved)


def CompareLists(differences: list, list1: list, list2: list, addedOrRemoved: bool):
	for enum in list1["Namespaces"]:
		CompareToOtherList(differences, enum, list2, addedOrRemoved)


def GetDifferences(list1: list, list2: list):
	differences = []
	
	CompareLists(differences, list1, list2, True)
	CompareLists(differences, list2, list1, False)
	
	return differences
