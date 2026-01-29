from int import Int
class BaseArray:
	def __init__(self, startArray=[]):
		self.arr = startArray
		self.type = None
		self.id = b'\xff'
		_validate(self.arr)
	def length():
		return len(self.arr)
	def pop(self, *args):
		return self.arr.pop(*args)
	def remove(self,element):
		return self.arr.remove(element)
	def append(self,element):
		if not isinstance(element, self.type):
			raise SyntaxError("Not the correct type.")
		self.arr.append(element)
	def _validate(self, array):
		for i in array:
			if not isinstance(i,self.type):
				raise SyntaxError('Element in array is not the correct type.')

	def getBytes(self):
		output = Int(len(self.arr)).getBytes()
		for i in self.arr:
			output += i.getBytes()

		return self.id + output