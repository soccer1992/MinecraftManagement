from short import Short
class TAG_SHORT:
	def __init__(self, num):
		self.num = num
	def getBytes(self):
		return b'\x02' + Short(self.num).getBytes()
