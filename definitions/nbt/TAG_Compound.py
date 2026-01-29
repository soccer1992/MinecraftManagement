from short import Short
from byte import Byte
from int import Int
from .TAG_String import *
from .TAG_END import *

class TAG_COMPOUND:
	def __init__(self, compoundName, keepName):
		self.compoundName = compoundName
		self.compoundlist = {}
		self.keepName = keepName




	def add(self, name, nbt):
		self.compoundlist[name] = nbt
	def remove(self, name):
		del self.compoundlist[name]



	def getBytes(self):
		#output = self.id
		#output += Int(len(self.arr)).getBytes()
		#for i in self.arr:
	#		output += i.getBytes()[1:]
		output = b''
		if self.keepName:
			#print(self.compoundName.encode())
			output += TAG_STRING(self.compoundName).getBytes()[1:]
		for i in self.compoundlist.keys():
			e = self.compoundlist[i].getBytes()
			print(e)
			output += bytes([e[0]])
			output += TAG_STRING(i).getBytes()[1:]
			output += e[1:]
		output += TAG_END().getBytes()
		return b'\x0a' + output