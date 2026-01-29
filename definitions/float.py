import struct
class Float:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>f',data[4:])[0],data[4:]]

	def getBytes(self):
		return struct.pack('>f',self.num)