from long import Long
class TAG_LONG:
	def __init__(self, num):
		self.num = num
	def getBytes(self):
		return b'\x04' + Long(self.num).getBytes()
