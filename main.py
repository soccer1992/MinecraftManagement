import json
import os.path
import socket
import colorama
colorama.init() # Initiates the terminal colors.
import random
import threading # For the client connection threads + RCON
import dns.resolver

from MinecraftTools import * # For minecraft packet handling.
from minecraftClient import Client
import uuid


if not os.path.exists("config.json"):
    with open('config.json','w') as f:
        json.dump({"host":"","port":0},f)
config = json.load(open('config.json'))
host,port = config['host'], config['port']

if port=='default':
    print('[SCANNER] Port is default, fetching SRV host & port')
    port = 25565
    if socket.gethostbyname(host)==host:
        print('[SCANNER] Host inputted is a IP, no fetching required. (Using default port of 25565)')
    else:
        print('[SCANNER] Fetching SRV info...')
        try:
            answer = dns.resolver.resolve('_minecraft._tcp.' + host, 'SRV')[0]
            print(f'[SCANNER] Detected SRV info:\nHost: {answer.target}\nPort: {answer.port}')
            host,port = answer.target.to_text(), answer.port
        except:
            print('[SCANNER] No SRV found, using default 25565 port')

onlinePlayers=[]
HOST = "0.0.0.0"   # Listen on all interfaces
PORT = 25568

def kickPlayerInLogin(conn, msg):
    kickPacket = Packet()
    kickPacket.writeVarInt(0)
    kickPacket.writeString(msg)
    conn.sendall(kickPacket.getPacket())
def forward_data(c, s, instantSend: threading.Event, token):
    global sessions
    helper = PacketHelper()
    try:
        while True:

            m = c.recv(2**16)
            #print(m)
            if not m:
                #print('close')
                s.close()
                break
            #print(instantSend.is_set(),m)
            #print(m)
            if instantSend.is_set():
                s.sendall(m)
                continue
            helper.addPacket(m)
            readPacket = helper.readPacket()

            #ireadPacket:
            while readPacket:
                notInLoginStage = sessions[token]['login_stage_not']
                state = sessions[token]['state']
                overrideDefaultPacketSending = False

                packetId = readPacket.readVarInt()
                realOrigPacket = readPacket.origPacket
                compressLimit = sessions[token]['compression_limit']
                if compressLimit is not None:
                    if packetId == 0:
                        readPacket.origPacket = readPacket.packet
                    else:
                        readPacket.origPacket = zlib.decompress(readPacket.packet)
                        readPacket.packet = readPacket.origPacket
                    packetId = readPacket.readVarInt()
                #print(packetId, readPacket.packet)
                if state=='CONFIG':
                    if packetId==0x01:
                        dumbPacket = Packet()
                        if readPacket.readString()==b'minecraft:brand':
                            dumbPacket.writeVarInt(packetId)
                            dumbPacket.writeString(b'minecraft:brand')
                            dumbPacket.writeString(readPacket.readString() + b' [MineManagement]')
                            readPacket.origPacket = dumbPacket.packet
                            readPacket.packet = readPacket.origPacket
                        #dumbPacket.writeVarInt(packetId)
                        #dumbPacket

                if not notInLoginStage.is_set():
                    #print(packetId)
                    if packetId==0x01:
                        instantSend.set()
                        print("[FORWARDER] The server is online-mode, enabling instant-forward mode.")
                    if packetId==0x02:
                        ...
                        #inLoginStage = False
                        #print("[FORWARDER] Entered configuration phase.")
                        #instantSend.set()

                    if packetId==0x03:
                        compressAmount = readPacket.readVarInt()
                        print(f'[FORWARDER] Compression has been changed to: {compressAmount}')
                        if compressAmount>-1:
                            sessions[token]['compression_limit'] = compressAmount
                copyP = Packet()
                #copyP.writeVarInt(packetId)
                copyP.writeRaw(readPacket.origPacket)
                #print(copyP.packet,compressLimit)
                s.sendall(getCompress(copyP, compressLimit))
                readPacket = helper.readPacket()



    except Exception as e:
        print('error',e)
        s.close()
def getCompress(packet, compressLimit):
    if compressLimit is not None:
        return packet.getPacket(1, ((len(packet.packet) >= compressLimit)))

        return packet.getPacket(1, ((len(packet.packet) >= compressLimit)))
    else:
        return packet.getPacket()
sessions = {}
def handle_client(conn, addr):
    global sessions
    print(f"[NEW CONNECTION] {addr}")
    sessionToken = ''.join(random.choices('0123456789abcdef',k=16))
    sessions[sessionToken] = {"serverConnection":None, "client":conn, "compression_limit": None, "login_stage_not":threading.Event(),"state":None,'username':None}
    hasHandshaked = False
    STATE = "HANDSHAKE"
    clientPacket = PacketHelper()

    clientServer = Client(host, port)
    instantForward = threading.Event()
    serverConnection = None
    try:
        with conn:
            while True:
                #print(conn.fileno())
                try:
                    data = conn.recv(2**16)
                except:
                    break
                if not data:
                    break

                #print(instantForward.is_set())
                if instantForward.is_set():
                    #print(data)
                    serverConnection.sendall(data)
                    continue
                clientPacket.addPacket(data)
                #print(clientPacket.packet)

                packet = clientPacket.readPacket()
                while packet:
                    #packet = clientPacket.readPacket()

                    #print(packet.origPacket)
                    packetId = packet.readVarInt()
                    # If compression is enabled, we have to parse the compressed packet format
                    compressLimit = sessions[sessionToken]['compression_limit']
                    if compressLimit is not None:
                        if packetId==0:
                            packet.origPacket = packet.packet
                        else:
                            packet.origPacket = zlib.decompress(packet.packet)
                            packet.packet = packet.origPacket
                        packetId = packet.readVarInt()
                    #print(packet.origPacket)

                    # The server should first send a 0x00 Packet (Handshake)
                    if not hasHandshaked:
                        if packetId!=0x00:
                            print(f"[DISCONNECTED - INVALID PACKET] {addr} ")
                            conn.close()
                            return
                        hasHandshaked = True

                        protoVersion = packet.readVarInt()
                        connectAddr = packet.readString()
                        connectPort = packet.readUSignInt()[0]
                        intent = packet.readVarInt()
                        print("[HANDSHAKE] Player connected with handshake IP:",(connectAddr.decode()) + ":" + str(connectPort))
                        print("[HANDSHAKE] Protocol version:",protoVersion)
                        print("[HANDSHAKE] Intent:",intent)
                        if intent==1:
                            # Status
                            STATE = "STATUS"

                            ## Send the basic MOTD.

                            #conn.close()
                            #return
                        elif intent==2:
                            STATE = "LOGINAWAIT"
                            #kickPlayerInLogin(conn, json.dumps({"text":"Login isn't supported"}).encode())
                        elif intent==3:
                            # WIP transfer.
                            kickPlayerInLogin(conn, json.dumps({"text": "Transfer isn't supported"}).encode())
                            #return
                    else:
                        match STATE:
                            case "CONFIG":
                                if packetId==0x03:
                                    STATE = "PLAY"
                                    print("[FORWARDER (C->S)] Entered the PLAY state.")
                                #print('config')
                            case "LOGINAWAIT":
                                # Next packet will be the login data
                                # forward thing
                                if packetId==0x03:
                                    STATE = "CONFIG"
                                    sessions[sessionToken]['login_stage_not'].set()
                                    print("[FORWARDER (C->S)] Entered configuration phase.")

                                if packetId==0x00:
                                    # its gonna contain a username + UUID
                                    #print(packet.origPacket)
                                    username = packet.readString().decode()
                                    uuid14 = packet.readUUID()
                                    continueThrough = True

                                    print(f"[LOGIN] User {username} ({str(uuid.UUID(hex(uuid14)[2:]))}) connected.")

                                    print("[FORWARDER] Starting.")
                                    serverConnection =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    serverConnection.settimeout(15)
                                    if 1:
                                        try:
                                            serverConnection.connect((host, port))
                                        except Exception as e:
                                            kickPlayerInLogin(conn, json.dumps({"text":"Failed to connect: ","color":"red","extra":[{"text":str(e),"color":"red"}]}).encode())
                                            continueThrough = False
                                            serverConnection = None
                                    if continueThrough:

                                        handshakePacket = Packet()
                                        handshakePacket.writeVarInt(0)
                                        handshakePacket.writeVarInt(protoVersion)
                                        handshakePacket.writeString(host.encode()) # connectAddr
                                        handshakePacket.writeUSignInt(port) # connectPort
                                        handshakePacket.writeVarInt(2)
                                        serverConnection.sendall(handshakePacket.getPacket())
                                        newThing = Packet()
                                        newThing.writeVarInt(0)
                                        newThing.writeString(username.encode())
                                        newThing.writeUUID(uuid14)
                                        #serverConnection.sendall(newThing.getPacket())
                                        #instantForward.set()

                                        sessions[sessionToken]['serverConnection'] = serverConnection
                                        threading.Thread(target=forward_data,args=(serverConnection, conn, instantForward, sessionToken)).start()
                                    #instantForward.set()
                            case "STATUS":
                                #print(packetId)
                                if packetId==0x01:
                                    # thats a ping packet.
                                    # Because its the EXACT same, we just send the exact same
                                    copyPacket = Packet()
                                    copyPacket.writeRaw(packet.origPacket)
                                    conn.sendall(copyPacket.getPacket())
                                if packetId==0x00:
                                    print("[STATUS] Pinging server...")
                                    newPacket = Packet()
                                    newPacket.writeVarInt(0)
                                    newPacket.writeString(json.dumps(clientServer.getPingInfo(protoVersion,defaultError=
                                                                                              buildMotdJSON("MineManagement", protoVersion, {"text": "Failed to connect to server...","color":"red"}, -1, 1))
                                                                     ).encode())
                                    #newPacket.writeString(json.dumps(
                                    #    buildMotdJSON("MineTest", protoVersion, {"text": "MOTD test"}, 999, 999)).encode())
                                    conn.sendall(newPacket.getPacket())
                                    #conn.close()
                                    #retur
                    if serverConnection:
                        #print('forward')
                        copyPacket = Packet()
                        copyPacket.writeRaw(packet.origPacket)
                        serverConnection.sendall(getCompress(copyPacket, compressLimit))
                    packet = clientPacket.readPacket()
                    sessions[sessionToken]['state'] = STATE

                    #print(packet.packet)
                    # Read the packet data.
    except Exception as err:
       print(f'[CONNECTION] Connection error, {repr(err)}')

    print(f"[DISCONNECTED] {addr}")
    del sessions[sessionToken]
    if serverConnection:
        serverConnection.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()

        #print(f"[ACTIVE THREADS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
