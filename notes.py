# coding: utf-8

import hashlib
import bencode
metainf = bencode.bdecode(open('LibreOffice_4.1.5_MacOS_x86.dmg.torrent', 'rb').read())
hashlib.sha1(metainf.get('info'))
metainf
type(metainf)
bencode.bencode(metainf.get('info'))
_
_
infostring = _
infostring
hashlib.sha1(infostring)
hashlib.sha1(infostring).digest()
metainf
hashlib.sha1(infostring).digest()
hashlib.sha1('poop').digest()
import os
os.urandom(20)
os.urandom(20)
os.urandom(20)
os.urandom(20)
import socket
IP = 127.0.0.1
IP = '127.0.0.1'
PORT = 63576
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.senc(MESSAGE)
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
data
s.close()
\19
'\19'
bytearray([1,2,3])
bytearray([1,2,420])
bytearray([1,2,420])
bytearray([19,'bittorrent'])
bytearray([19,'b','i','t','t','o','r','r','e','n','t'])
'BitTorrent Protocol'.split()
list('BitTorrent Protocol')
bytearay([19]+list('BitTorrent Protocol'))
bytearray([19]+list('BitTorrent Protocol'))
[19, list('string')]
handhake1 = _
handshake1
handhake1
handshake1 = handhake1
del(handhake1)
bytearray(0,0,0,0,0,0,0,0)
bytearray([0,0,0,0,0,0,0,0])
handshake2 = bytearray([0,0,0,0,0,0,0,0])
hashlib.sha1(infostring).digest()
handshake3 = hashlib.sha1(infostring).digest()
handshake3
len(handshake3)
os.urandom(20)
handshake4 = _
handshake4
len(_)
handshake1+handshake2+handshake3+handshake4
[handshake1, handshake2, handshake3, handshake4]
b''.join([handshake1, handshake2, handshake3, handshake4])
handshake1.append(handshake2)
handshake1
handshake1 = bytearray([19]+list('BitTorrent Protocol'))
handshake1
handshake1.append(handshake2)
handshake1.join(handshake2)
handshake1.join([handshake2])
handshake1
handshake2
bytearray([handshake1, handshake2])
bytearray(handshake1, handshake2)
bytearray.join(handshake1, handshake2)
handshake1
handshake1 += handshake2
handshake1
handshake1 += handshake3
handshake1 += handshake4
handshake1
MESSAGE = handshake1
MESSAGE
MESSAGE.__str__
MESSAGE.__str__()
MESSAGE.__repr__()
MESSAGE.__str__()
MESSAGE = MESSAGE.__str__()
MESSAGE
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
data
len(MESSAGE)
s.connect((IP, PORT))
s.connect((IP, PORT))
IP
PORT
s.connect((IP, PORT))
s.close()
s.connect((IP, PORT))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
data
PORT
PORT = 60750
def send_handshake():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    return data
send_handshake()
send_handshake()
send_handshake()
send_handshake()
send_handshake()
