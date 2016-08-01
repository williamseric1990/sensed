import time
import pprint
import struct
import socket
import msgpack
from Map import Map


HEADERS = Map()
HEADERS.ID = b'\x01\x00'
HEADERS.REQ = b'\x01\x01'
HEADERS.ERR = b'\x01\x02'


class SensedClient(object):
    def __init__(self, cfg):
        self.hosts = cfg['hosts']
        self.interval = cfg['interval']
        self.pp = pprint.PrettyPrinter(indent=2, width=80)

    def run_meta(self):
        print('Meta Process')
        for host in self.hosts:
            print('Pinging {}...'.format(host), end=' ')
            meta = self.get_meta(host)
            return meta

    def run_once(self):
        for host in self.hosts:
            print('Pinging {}...'.format(host), end=' ')
            data = self.get_sensors(host)
            print('Recieved data:')
            self.pp.pprint(data)
            print()

    def get_meta(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(HEADERS.ID, host)

        raw_data = s.recv(1024)
        header = raw_data[:2]
        raw_meta = raw_data[2:]
        meta = msgpack.unpackb(raw_meta)

        return meta

    def get_sensors(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(HEADERS.REQ, host)

        raw_size = s.recv(4)
        size = struct.unpack('I', raw_size)[0]

        raw_data = s.recv(size)
        header = raw_data[:2]
        data = msgpack.unpackb(raw_data[2:])

        return {'header': header, 'body': data}
