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
PORT = 56573
BUFFER_SIZE = 1024
MESSAGE = "\x13BitTorrent protocol" + struct.pack("!8x20s20s", infohash, os.urandom(20))
BLOCK_SIZE = 2**14

counter = 0

def send_handshake(socket):
    socket.send(MESSAGE)
    data = socket.recv(BUFFER_SIZE)
    return data

def unchoke(socket):
    m = struct.pack("!iB", 1, 1)
    socket.send(m)
    data = socket.recv(BUFFER_SIZE)
    return data

def express_interest(socket):
    m = struct.pack("!iB", 1, 2)
    socket.send(m)
    data = socket.recv(BUFFER_SIZE)
    return data

def request(socket, piece_number, block_offset):
    m = struct.pack("!iBiii", 13, 6, piece_number, block_offset, BLOCK_SIZE)
    socket.send(m)

    while(True):
        data = socket.recv(BLOCK_SIZE+13)
        if len(data)<13:
            continue
        header = data[:13]
        parsed_header = struct.unpack('!iBii', header)
        if (parsed_header[1] == 7 and
            len(data[13:]) == BLOCK_SIZE and
            piece_number != 693 and
            parsed_header[2] == piece_number and parsed_header[3] == block_offset):
            break
        else:
            socket.send(m)

    global counter
    print('block #: {}'.format(counter))
    counter += 1
    print('message length: {}'.format(parsed_header[0]))
    print('message ID: {}'.format(parsed_header[1]))
    print('piece index: {}'.format(parsed_header[2]))
    print('block index: {}'.format(parsed_header[3]))

    payload = data[13:]
    print('size of payload: {}'.format(len(payload)))
    print('\n\n')

    return payload

def get_piece(socket, piece_number):
    block_count = metainf.get('info').get('piece length')/BLOCK_SIZE

    piece_in_progress = b''

    for block_number in xrange(block_count):
        piece_in_progress += request(socket, piece_number, block_number*BLOCK_SIZE)

    print 'length of what we downloaded: {}'.format(len(piece_in_progress))
    print 'expected piece length: {}'.format(metainf.get('info').get('piece length'))

    '''
    calculated_hash = hashlib.sha1(piece_in_progress).hexdigest()
    expected_hash = metainf.get('info').get('pieces')[20*piece_number:20*piece_number+20]
    if  calculated_hash != expected_hash:
        raise ValueError('THE HASHES DON"T MATCH OMG\npiece_number: {}\ncalculated hash: {}\nexpected hash: {}'.format(piece_number, calculated_hash, expected_hash))
    '''
    return piece_in_progress

def get_file(socket):
    file_length = metainf.get('info').get('length')
    piece_length = metainf.get('info').get('piece length')
    piece_count = file_length/piece_length

    for piece_number in xrange(piece_count):
        if piece_number == 0:
            with open(metainf.get('info').get('name'), 'wb') as partial_file:
                partial_file.write(get_piece(socket, piece_number))
        else:
            with open(metainf.get('info').get('name'), 'ab') as partial_file:
                partial_file.write(get_piece(socket, piece_number))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
send_handshake(s)
unchoke(s)
express_interest(s)
get_file(s)
s.close()
