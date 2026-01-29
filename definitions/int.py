import struct
class Int:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>i',data[:4])[0],data[4:]]

	def getBytes(self):
		return struct.pack('>i',self.num)