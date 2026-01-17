import zlib
import struct
import json
SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80;


def writeVarInt(value):
    output = bytearray()
    while (1):
        if ((value & ~SEGMENT_BITS) == 0):
            output.append(value);
            break;
            # return;

        output.append((value & SEGMENT_BITS) | CONTINUE_BIT);

        value = (value >> 7) & 0xFFFFFFFF;
    return (output)


def readVarInt(data):
    value = 0;
    position = 0;
    currentByte = None;
    string = data
    i = 0
    try:
        while True:
            currentByte = string[i]
            i += 1
            value |= (currentByte & SEGMENT_BITS) << position;

            if ((currentByte & CONTINUE_BIT) == 0): break;

            position += 7;

            if (position >= 32): return None
    except:
        return [0, 1]

    return [value, i];


def encode_as_unsigned_128_bit(value):
    if not (0 <= value < 2 ** 128):
        raise ValueError("Value must be in the range [0, 2^128)")

    # Get the most significant 64 bits
    msb = (value >> 64) & 0xFFFFFFFFFFFFFFFF
    # Get the least significant 64 bits
    lsb = value & 0xFFFFFFFFFFFFFFFF

    return msb, lsb


class MinecraftPacket:
    def __init__(self, packet):
        # print(packet)
        self.packet = packet
        self.origPacket = packet

    def readVarInt(self):
        varInt, exclude = readVarInt(self.packet)
        self.packet = self.packet[exclude:]
        return varInt

    def readString(self):
        stringLength = self.readVarInt()
        string = self.packet[:stringLength]
        self.packet = self.packet[stringLength:]
        return string

    def readUSignInt(self):
        out = struct.unpack('>H', self.packet[:2])
        self.packet = self.packet[2:]
        return out

    def readRaw(self, bytes1):
        out = self.packet[:bytes1]
        self.packet = self.packet[bytes1:]
        return out

    def readUUID(self):
        # print(self.packet)
        a = self.readRaw(16)
        # print(len(a))
        out = struct.unpack('>QQ', a)
        out = (out[0] << 64) | out[1]
        return out

mappings = {
"MINECRAFT_1_8" : 47,
"MINECRAFT_1_9": 107,
"MINECRAFT_1_9_1": 108,
"MINECRAFT_1_9_2": 109,
"MINECRAFT_1_9_4": 110,
"MINECRAFT_1_10": 210,
"MINECRAFT_1_11": 315,
"MINECRAFT_1_11_1": 316,
"MINECRAFT_1_12": 335,
"MINECRAFT_1_12_1": 338,
"MINECRAFT_1_12_2": 340,
"MINECRAFT_1_13": 393,
"MINECRAFT_1_13_1": 401,
"MINECRAFT_1_13_2": 404,
"MINECRAFT_1_14": 477,
"MINECRAFT_1_14_1": 480,
"MINECRAFT_1_14_2": 485,
"MINECRAFT_1_14_3": 490,
"MINECRAFT_1_14_4": 498,
"MINECRAFT_1_15": 573,
"MINECRAFT_1_15_1": 575,
"MINECRAFT_1_15_2": 578,
"MINECRAFT_1_16": 735,
"MINECRAFT_1_16_1": 736,
"MINECRAFT_1_16_2": 751,
"MINECRAFT_1_16_3": 753,
"MINECRAFT_1_16_4": 754,
"MINECRAFT_1_17": 755,
"MINECRAFT_1_17_1": 756,
"MINECRAFT_1_18": 757,
"MINECRAFT_1_18_2": 758,
"MINECRAFT_1_19": 759,
"MINECRAFT_1_19_1": 760,
"MINECRAFT_1_19_3": 761,
"MINECRAFT_1_19_4": 762,
"MINECRAFT_1_20": 763,
"MINECRAFT_1_20_2": 764,
"MINECRAFT_1_20_3": 765,
"MINECRAFT_1_20_5": 766,
"MINECRAFT_1_21": 767,
"MINECRAFT_1_21_2": 768,
"MINECRAFT_1_21_4": 769,
"MINECRAFT_1_21_5": 770,
"MINECRAFT_1_21_6": 771,
"MINECRAFT_1_21_7": 772,
}

def make_bytes(data):
    if isinstance(data,str):
        return data.encode()
    if isinstance(data,list):
        out = []
        for i in data:
            out.append(make_bytes(i))
        return out
    if isinstance(data,dict):
        out = {}
        for i in data.keys():
            out[i] = make_bytes(data[i])
        return out




def format_json(data,proto):
    out = {}



    out1 = []
    if isinstance(data,str):
        out1 = {"text":data}
    elif isinstance(data,list):
        for i in data:
            #print(i)
            if isinstance(i,str) or isinstance(i,bytes):
                se = i
                if isinstance(se,bytes):
                    se = se.decode()
                out1.append({"text":i})
            else:
                out1.append(i)
    #elif isinstance(data, dict):
    #    out1 = data
    if isinstance(out1,list):
        out = out1[0]
        if len(out1)>1:
            out['extra'] = out1[1:]

   # print(make_bytes(out))
    if proto>=mappings['MINECRAFT_1_20_3']:
        a = make_bytes(out)

        a = SNBT_TO_NBT(a,1)
    else:
        a = json.dumps(out).encode()
        a = writeVarInt(len(a)) + a
    #print(a)
    #print(a)
    return a




def SNBT_TO_NBT(data,exclude_name,recurse=0,add_prefix=1,name=b'',strip_headers=0):
    structure = {}
    out = b''
    if not recurse:
        out = b'\x0a'
        if not exclude_name:
            out += struct.pack('>h',len(name))
            out += name

    if isinstance(data,list):

        use_type = b'\x0a'
        if isinstance(data[0], bytes):
            use_type = b'\x08'
        out += b'\x09'
        if strip_headers:
            out = b''
        out += struct.pack('>h',len(name)) + name +  use_type + struct.pack('>i',len(data))

        for i in data:
            out += SNBT_TO_NBT(i,1,1,1,b'',1)
       # out += b'\x01'
    elif isinstance(data, dict):
        out = b'\x0a'
        if strip_headers:
            out = b''

        if not exclude_name:
            out += struct.pack('>h',len(name)) + name
        #print(sorted(data.keys()))
        for i in data.keys():
            other = data[i]
            if isinstance(other,bytes):
                out += b'\x08' + struct.pack('>h',len(i.encode())) + i.encode() + struct.pack('>h',len(other)) + other
            if isinstance(other, dict):
                out += SNBT_TO_NBT(other, False, 1, 0, i.encode())
            if isinstance(other,list):
                out += SNBT_TO_NBT(other, False, 1, 0, i.encode())
        out += b'\x00'
    elif isinstance(data, bytes):

        out += b'\x08'
        if strip_headers:
            out = b''
        if not exclude_name:
            out += struct.pack('>h',len(name)) + name
        out += struct.pack('>h',len(data)) + data
    #if not recurse:
    #    out += b'\x00'
    return out
class Packet:
    def __init__(self):
        self.packet = b''
    def writeVarInt(self, num):
        self.packet += writeVarInt(num)
    def writeString(self, string):
        self.writeVarInt(len(string))
        self.writeRaw(string)
    def writeUUID(self, num):
        self.writeRaw(struct.pack('>QQ',*encode_as_unsigned_128_bit(num)))
    def writeRaw(self, data):
        self.packet += data
    def writeUSignInt(self, num):
        out = struct.pack('>H', num)
        self.writeRaw(out)
    def getPacket(self, compress_format=0, compress=0):
        if not compress_format:
            return writeVarInt(len(self.packet)) + self.packet
        else:
            if compress:
                out_data = zlib.compress(self.packet)
            else:
                out_data = self.packet
            compressed_packet = b''
            if compress:
                #print(len(self.packet),'packet.')
                compressed_packet += writeVarInt(len(self.packet)) + out_data
            else:
                compressed_packet += writeVarInt(0) + out_data
            compressed_packet = writeVarInt(len(compressed_packet)) + compressed_packet
            #print(compressed_packet)
            return compressed_packet
class PacketHelper:
    def __init__(self):
        self.packet = b''
    def addPacket(self, packet):
        self.packet += packet
    def readPacket(self):
        # detect if packet is long enough

        if not self.packet:
            return None

        varInt, exclude = readVarInt(self.packet)
        exclude_len = len(self.packet)-exclude
        if exclude_len<varInt:
            return None
        out = self.packet[exclude:][:varInt]
        self.packet = self.packet[varInt+exclude:]
        return MinecraftPacket(out)
        #self.packet = self.packet[exclude:]
        #return varInt


def buildMotdJSON(verName, verProtocol, motd, playerOnline, playerMax):
    return {"version":{
        "name": verName,
        "protocol": verProtocol
    },
    "players":{
        "max":playerMax,
        "online": playerOnline,
        "sample": []
    },
    "description":motd
    }

