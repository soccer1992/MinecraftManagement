from byte import Byte
class TAG_BYTE:
	def __init__(self, num):
		self.num = num
	def getBytes(self):
		return b'\x01' + Byte(self.num).getBytes()
