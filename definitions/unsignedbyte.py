import struct
class UnsignedByte:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>B',data)[0],data[1:]]

	def getBytes(self):
		return struct.pack('>B',self.num)