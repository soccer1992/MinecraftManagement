from byte import Byte
from int import Int
from .BaseArray import *
class TAG_BYTE_ARRAY(BaseArray):
	def __init__(self, startArray=[]):
		self.arr = startArray
		self.id = b'\x07'
		self.type = Byte
		self._validate(self.arr)
