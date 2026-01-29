from double import Double
class TAG_DOUBLE:
	def __init__(self, num):
		self.num = num
	def getBytes(self):
		return b'\x06' + Double(self.num).getBytes()
