import struct
import time
import socket
import os
import bencode
import hashlib
import socket
import argparse

parser =  argparse.ArgumentParser()
parser.add_argument('torrent')
parser.add_argument('IP')
parser.add_argument('Port', type=int)
args = parser.parse_args()

torrent = args.torrent
metainf = bencode.bdecode(open(torrent, 'rb').read())
infostring = bencode.bencode(metainf.get('info'))
infohash = hashlib.sha1(infostring).digest()
IP = args.IP
PORT = args.Port
BUFFER_SIZE = 1024
MESSAGE = "\x13BitTorrent protocol" + struct.pack("!8x20s20s", infohash, os.urandom(20))
BLOCK_SIZE = 2**14
counter = 1
NUM_PIECES = metainf.get('info').get('length')/metainf.get('info').get('piece length')

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
        piece_number <= NUM_PIECES and 
        parsed_header[2] == piece_number and 
        parsed_header[3] == block_offset):
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
    while(True):
	    if piece_number == NUM_PIECES:
	       block_count = (metainf.get('info').get('length') - ((NUM_PIECES - 1) * metainf.get('info').get('piece_length')))/BLOCK_SIZE
	    for block_number in xrange(block_count):
		piece_in_progress += request(socket, piece_number, block_number*BLOCK_SIZE)
	    
	    calculated_hash = hashlib.sha1(piece_in_progress).digest()
	    print 'Calculated hash: {}'.format(calculated_hash)
	    expected_hash = metainf.get('info').get('pieces')[20*piece_number:20*piece_number+20]
	    print 'Expected hash: {}'.format(expected_hash)

	    if calculated_hash == expected_hash:
	       break
	    elif calculated_hash != expected_hash:
	       piece_in_progress = b''

    return piece_in_progress

def get_file(socket):
    file_length = metainf.get('info').get('length')
    piece_length = metainf.get('info').get('piece length')
    piece_count = file_length/piece_length

    for piece_number in xrange(0,piece_count+1):
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
