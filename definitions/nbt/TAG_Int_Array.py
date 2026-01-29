from byte import Byte
from int import Int
from .BaseArray import *
class TAG_INT_ARRAY(BaseArray):
	def __init__(self, startArray=[]):
		self.arr = startArray
		self.id = b'\x0b'
		self.type = Int
		self._validate(self.arr)
