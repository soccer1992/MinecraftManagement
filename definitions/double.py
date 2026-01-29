import struct
class Double:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>d',data[:8])[0],data[8:]]

	def getBytes(self):
		return struct.pack('>d',self.num)