from short import Short
from byte import Byte
from int import Int

class TAG_List:
	def __init__(self, tagId, startArray=[]):
		self.arr = startArray
		self.id = tagId
		__validate(self.arr)
	def length():
		return len(self.arr)
	def pop(*args):
		return self.arr.pop(*args)
	def remove(element):
		return self.arr.remove(element)
	def append(element):
		if element.getBytes()[0]!=tagId:
			raise TypeException("Not the same type id")
		self.arr.append(element)
	def __validate(array):
		for i in array:
			if i.getBytes()[0]!=tagId:
				raise TypeException("Not the same type id")
			#if not isinstance(i,Byte):
			#	raise TypeException('Element in bytearray is not a byte.')

	def getBytes(self):
		output = self.id
		output += Int(len(self.arr)).getBytes()
		for i in self.arr:
			output += i.getBytes()[1:]

		return b'\x09' + output