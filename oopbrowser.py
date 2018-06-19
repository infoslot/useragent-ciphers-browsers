class oopbrowser(object):
	
	ciphersList = []

	def __init__(self,browser_name, browser_version, ciphers):
		self.browser_name = browser_name
        	self.browser_version = browser_version
        	self.ciphers = ciphers

	def setName(self, name):
	     	self.name = name

	def getName(self):
	     	return self.browser_name


	def setVersion(self, version):
		self.version = version

	def getVersion(self):
	     	return self.browser_version

	def setCiphers(self, cipher):
		self.ciphersList.append(cipher)

	def getCiphers(self, cipher):
		return self.ciphersList

	def close(self):
		pass
