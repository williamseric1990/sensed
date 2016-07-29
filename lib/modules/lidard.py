import struct
import socket
import msgpack

DATA_ID = b'\x02\x00'
DATA_REQ = b'\x02\x01'
DATA_ERR = b'\x02\x02'


class Lidard(object):
    ''' A sensor module that interfaces with `lidard`. '''

    def __init__(self, config):
        self.host = config['lidard']['host']
        self.port = config['lidard']['port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meta = self.get_metadata()

    def get_metadata(self):
        self.sock.sendto(DATA_ID, (self.host, self.port))
        raw_meta = self.sock.recv(1024)
        meta = msgpack.unpackb(raw_meta[2:])
        return meta

    def get_data(self):
        self.sock.sendto(DATA_REQ, (self.host, self.port))
        raw_size = s.recv(4)
        size = struct.unpack('I', raw_size)[0]

        raw_data = s.recv(size)
        data = msgpack.unpackb(raw_data[2:])
        data['meta'] = self.meta
        return data

    def test(self):
        return {}


Sensor = Lidard
