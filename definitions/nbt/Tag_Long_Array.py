from byte import Byte
from int import Int
from long import Long

from .BaseArray import *
class TAG_LONG_ARRAY(BaseArray):
	def __init__(self, startArray=[]):
		self.arr = startArray
		self.id = b'\x0c'
		self.type = Long
		self._validate(self.arr)
