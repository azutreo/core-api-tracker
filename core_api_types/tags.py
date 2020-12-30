def GetTagsFormat(parent):
	if "Tags" not in parent:
		return ""
	
	return " " + (" ").join("[{}]".format(tag) for tag in parent["Tags"])
