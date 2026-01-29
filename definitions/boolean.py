class Boolean:
	def __init__(self, boolean):
		if boolean:
			self.bytes = '\x01'
		else:
			self.bytes = '\x00'
	def read(data):
		if data:
			return [True, data[1:]]
		return [False, data[1:]]
	def getBytes(self):
		return self.bytes