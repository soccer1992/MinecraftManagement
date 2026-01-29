import struct
class UnsignedShort:
	def __init__(self, dta):
		self.num = dta
	def read(data):
		return [struct.unpack('>H',data)[0],data[1:]]

	def getBytes(self):
		return struct.pack('>H',self.num)