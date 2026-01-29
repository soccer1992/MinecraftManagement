from int import Int
class TAG_INT:
	def __init__(self, num):
		self.num = num
	def getBytes(self):
		return b'\x03' + Int(self.num).getBytes()
