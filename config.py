import json

class JsonConfig():
	
	def __init__(self,configFilePath=None):
		self.configFilePath = configFilePath

		self.fields = []

	def loadConfig(self):

		file = open(self.configFilePath,"r")

		self.data = json.load(file)

		file.close()

	def getOption(self,fieldName=None):

		if fieldName == None:
			return None

		return self.data[fieldName]	

	def setOption(self,fieldName=None,Option=None):
		
		self.data[fieldName] = Option
		
	def saveConfig(self, path=None):
		
		if path == None:
			path = self.configFilePath
		
		file = open(path,"w")
		
		json.dump(self.data,file,ensure_ascii = False, indent=4)
		
		file.close()
