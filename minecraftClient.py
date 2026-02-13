import json
from MinecraftTools import *
import socket


class Client:
    def __init__(self, host, port):
        self.addr = (host, port)
    def getPingInfo(self, protocol=767, defaultError={}):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as e:
                e.settimeout(10)
                e.connect(self.addr)
                helper = PacketHelper()
                handshake = Packet()
                handshake.writeVarInt(0)
                handshake.writeVarInt(protocol)
                handshake.writeString(self.addr[0].encode())
                handshake.writeUSignInt(self.addr[1])
                handshake.writeVarInt(1)
                e.sendall(handshake.getPacket())
                req = Packet()
                req.writeVarInt(0)
                e.sendall(req.getPacket())

                p = None
                while not p:
                    z = e.recv(1024)
                    #print(z)
                    if not z:
                        p = '\x01\x00'
                    #if z:
                    #    print(z)
                    helper.addPacket(z)
                    p = helper.readPacket()
                #print(p.packet)
                p.readVarInt()
                returnedData =  p.readString()
                if not returnedData:
                    if defaultError: return defaultError

                    return None
                try:
                    jsonData = json.loads(returnedData)
                except:
                    if defaultError: return defaultError
                    return None
                return jsonData
        except Exception as m:
            if defaultError: return defaultError
            return None

