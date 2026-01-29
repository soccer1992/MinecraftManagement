import struct
class Byte:
	def __init__(self, dta):
		self.num = dta
		if not (-128 <= dta <= 127):
			raise SyntaxError('Byte out of range')

	def read(data):
		return [struct.unpack('>b',data[0])[0],data[1:]]

	def getBytes(self):
		return struct.pack('>b',self.num)