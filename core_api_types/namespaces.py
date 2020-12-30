import json
import core_api_types.functions as core_functions


def AddNamespace(differences: list, namespaceName: str):
	differences.append("Added Namespace " + namespaceName)
def RemoveNamespace(differences: list, namespaceName: str):
	differences.append("Removed Namespace " + namespaceName)
def ChangeNamespace(differences: list, namespaceName: str):
	differences.append("Changed Namespace " + namespaceName)

def AddStaticFunction(differences: list, returnType: str, namespaceName: str, functionName: str, parameterFormat: str):
	differences.append("\tAdded " + "StaticFunction " + returnType + " " + namespaceName + "." + functionName + parameterFormat)
def RemoveStaticFunction(differences: list, returnType: str, namespaceName: str, functionName: str, parameterFormat: str):
	differences.append("\tRemoved " + "StaticFunction " + returnType + " " + namespaceName + "." + functionName + parameterFormat)


def GetNamespaceByName(namespaces: list, namespaceName: str):
	for namespace in namespaces["Namespaces"]:
		if namespace["Name"] == namespaceName:
			return namespace


def GetStaticFunctionByName(namespace: dict, functionName: str):
	for staticFunction in namespace["StaticFunctions"]:
		if staticFunction["Name"] == functionName:
			return staticFunction


def AddSignature(differences, signature, namespaceName: str, functionName: str, addedOrRemoved: bool):
	parameterFormat = core_functions.GetParameterFormat(signature, "(", ")", False)
	returnType = core_functions.GetReturnType(signature)
	
	if addedOrRemoved:
		AddStaticFunction(differences, returnType, namespaceName, functionName, parameterFormat)
	else:
		RemoveStaticFunction(differences, returnType, namespaceName, functionName, parameterFormat)


def AddAllSignatures(differences: list, signatures: dict, namespaceName: str, functionName: str, addedOrRemoved: bool):
	for signature in signatures:
		AddSignature(differences, signature, namespaceName, functionName, addedOrRemoved)

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
					
					AddSignature(differences, signature, namespace["Name"], staticFunction["Name"], addedOrRemoved)
			else:
				if not wasChanged:
					wasChanged = True
					ChangeNamespace(differences, namespace["Name"])
				
				AddAllSignatures(differences, staticFunction["Signatures"], namespace["Name"], staticFunction["Name"], addedOrRemoved)
	else:
		AddAllNamespaceDifferences(differences, namespace, addedOrRemoved)


def CompareLists(differences: list, list1: list, list2: list, addedOrRemoved: bool):
	for namespace in list1["Namespaces"]:
		CompareToOtherList(differences, namespace, list2, addedOrRemoved)


def GetDifferences(list1: list, list2: list):
	differences = []
	
	CompareLists(differences, list1, list2, True)
	CompareLists(differences, list2, list1, False)
	
	return differences
