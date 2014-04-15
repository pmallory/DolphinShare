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

def send_handshake():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    s.send(MESSAGE)
    time.sleep(5)
    data = s.recv(BUFFER_SIZE)
    s.close()
    return data

print send_handshake()
