from nbt import *
from byte import *
from short import *
from int import *
from long import *
from double import *
from float import *
def parseNbtPart(nbtPart,ignoreComponentNamePart=False):
	match nbtPart[0]:
		case 0:
			return TAG_END(), 0
		case 1:
			# singular signed byte!
			return TAG_BYTE(Byte.read(nbtPart[1])[0]), 1
		case 2:
			return TAG_SHORT(Short.read(nbtPart[1:3])[0]), 2
		case 3:
			return TAG_INT(Int.read(nbtPart[1:5])[0]), 4
		case 4:
			return TAG_LONG(Long.read(nbtPart[1:9])[0]), 8
		case 5:
			return TAG_FLOAT(Float.read(nbtPart[1:5])[0]), 4
		case 6:
			return TAG_DOUBLE(Double.read(nbtPart[1:9])[0]), 8
		case 7:
			# byte array
			arrayBytes = nbtPart[1:]
			length,arrayBytes = Int.read(arrayBytes)
			returnType = TAG_BYTE_ARRAY()
			for i in range(length):
				returnType.append(Byte.read(arrayBytes[i])[0])
			return returnType, 5+length

		case 8:
			# byte array
			strBytes = nbtPart[1:]
			length,strBytes = Short.read(strBytes)
			return TAG_STRING(strBytes[:length]), 3+length
		case 9:
			tagBytes = nbtPart[1:]
			returnList = TAG_LIST(tagBytes[0])
			tagType = tagBytes[0]
			length,tagBytes = Int.read(tagBytes)
			totalBytes = 6
			for i in range(length):
				z=parseNbtPart(tagType + tagBytes)
				returnList.append(z[0])
				tagBytes = tagBytes[z[1]-1:]
				totalBytes += z[1]-1
			return returnList,totalBytes
		case 10:
			tagBytes = nbtPart[1:]
			totalBytes = 1
			name = None
			if not ignoreComponentNamePart:
				totalBytes += 2
				#print(tagBytes[:2])
				#print( Short.read(tagBytes[:2]))
				length,tagBytes = Short.read(tagBytes)
				totalBytes += length
				#print(tagBytes)
				name = tagBytes[:length]
				tagBytes = tagBytes[length:]
			compound = TAG_COMPOUND(name, not ignoreComponentNamePart)
			while tagBytes[0]!=0:
				#print(tagBytes,'be')
				readTag = bytes([tagBytes[0]])

				tagBytes = tagBytes[1:]
				totalBytes += 1
				#print(tagBytes,'af')
				nameLength,tagBytes = Short.read(tagBytes)
				totalBytes += 2
				totalBytes += nameLength
				tagName = tagBytes[:nameLength]
				tagBytes = tagBytes[nameLength:]
				#print(readTag)
				readTag += tagBytes
				parsed = parseNbtPart(readTag)
				compound.add(tagName,parsed[0])
				tagBytes = tagBytes[parsed[1]-1:]
				totalBytes += parsed[1]-1
			return compound, totalBytes
		case 11:
			tagBytes = nbtPart[1:]
			totalBytes = 1
			listArray = TAG_INT_ARRAY()
			length, tagBytes = Int.read(tagBytes)
			totalBytes += 4
			for i in range(length):
				out, tagBytes = Int.read(tagBytes)
				listArray.append(out)
				totalBytes += 4
			return listArray, totalBytes
		case 12:
			tagBytes = nbtPart[1:]
			totalBytes = 1
			listArray = TAG_INT_ARRAY()
			length, tagBytes = Int.read(tagBytes)
			totalBytes += 4
			for i in range(length):
				out, tagBytes = Long.read(tagBytes)
				listArray.append(out)
				totalBytes += 8
			return listArray, totalBytes



#print(TAG_STRING('test').getBytes())


#print(parseNbtPart(basicNbt)[0].getBytes())
#rootCompound = TAG_COMPOUND('gdclogne', True)
#rootCompound.add('text',TAG_STRING('test'))
#print(rootCompound.getBytes())