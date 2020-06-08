import json

class Language():

	def __init__(self,languageFilePath=None):
		self.languageFilePath = languageFilePath

		self.fields = []

	def loadLanguageData(self):

		file = open(self.languageFilePath,"r")

		self.data = json.load(file)

		file.close()

	def getText(self,fieldName=None):

		if fieldName == None:
			return None

		return self.data[fieldName]	