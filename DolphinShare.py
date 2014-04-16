import struct
import time
import socket
import os
import bencode
import hashlib
import socket

metainf = bencode.bdecode(open('LibreOffice_4.1.5_MacOS_x86.dmg.torrent', 'rb').read())
infostring = bencode.bencode(metainf.get('info'))
infohash = hashlib.sha1(infostring).digest()

IP = '127.0.0.1'
PORT = 58220
BUFFER_SIZE = 1024
MESSAGE = "\x13BitTorrent protocol" + struct.pack("!8x20s20s", infohash, os.urandom(20))

def send_handshake(socket):
    socket.send(MESSAGE)
    time.sleep(.1)
    data = socket.recv(BUFFER_SIZE)
    return data

def unchoke(socket):
    m = struct.pack("!iB", 1, 1)
    socket.send(m)
    time.sleep(.1)
    data = socket.recv(BUFFER_SIZE)
    return data

def express_interest(socket):
    m = struct.pack("!iB", 1, 2)
    socket.send(m)
    time.sleep(.1)
    data = socket.recv(BUFFER_SIZE)
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
print send_handshake(s)
print unchoke(s)
print express_interest(s)
s.close()
