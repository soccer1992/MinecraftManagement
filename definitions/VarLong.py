from long import Long
from unsignedbyte import UnsignedByte
from byte import Byte

import struct
class VarLong:
	SEGMENT_BITS = 0x7f
	CONTINUE_BIT = 0x80
	def __init__(self, dta):
		self.num = dta
	def read(data):
		value = 0
		pos = 0
		currByte = None
		currData = data
		while True:
			currByte,currData = UnsignedByte.read(currData)
			value |= (self.currByte & self.SEGMENT_BITS) << pos
			if ((self.currByte & self.CONTINUE_BIT) == 0): break
			pos += 7
			if (pos >= 64): raise OverflowError('VarLong is too large')
		return [value, currData]
		#return [struct.unpack('>f',data[0]),data[1:]]

	def getBytes(self):
		outBytes = b''
		currNum = self.num
		while True:
			#print(currNum)
			#print((currNum & self.SEGMENT_BITS) | self.CONTINUE_BIT)
			if ((currNum & ~self.SEGMENT_BITS) == 0):
				outBytes += UnsignedByte(currNum).getBytes()
				return outBytes
			outBytes += UnsignedByte((currNum & self.SEGMENT_BITS) | self.CONTINUE_BIT).getBytes()
			currNum =  (currNum & 0xFFFFFFFFFFFFFFFF) >> 7