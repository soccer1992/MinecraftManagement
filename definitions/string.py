import struct
class Double:
	def __init__(self, string):
		self.str = string.encode()
	def read(data):
		dta = data
		stringLength, dta = VarInt.read(dta)
		string, dta = dta[:stringLength], dta[stringLength:]
		return [string, dta]

	def getBytes(self):
		e = VarInt(len(self.str))
		return e.getBytes() + self.str