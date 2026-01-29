import struct
class Short:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>h',data[:2])[0],data[2:]]

	def getBytes(self):
		return struct.pack('>h',self.num)