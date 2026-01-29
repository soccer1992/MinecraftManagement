import struct
class Long:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>l',data[:8])[0],data[8:]]

	def getBytes(self):
		return struct.pack('>l',self.num)