from float import Float
class TAG_FLOAT:
	def __init__(self, num):
		self.num = num
	def getBytes(self):
		return b'\x05' + Float(self.num).getBytes()
