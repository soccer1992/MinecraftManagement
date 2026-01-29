from short import Short
class TAG_STRING:
	def __init__(self, str1):
		self.string = str1
		if not isinstance(self.string,bytes):
			self.string = self.string.encode()
	def getBytes(self):
		return b'\x08' + Short(len(self.string)).getBytes() + self.string # screw this stupid modified utf-8 stuff