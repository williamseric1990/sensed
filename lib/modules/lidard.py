import socket

DATA_ID = '\x01\x00'
DATA_REQ = '\x02\x00'


class Lidard(object):
    ''' A sensor module that interfaces with `lidard`. '''

    def __init__(self, host, port, meta_processor=None, data_processor=None):
        self.host = host
        self.port = port
        self.meta_processor = meta_processor or self._process_metadata
        self.data_processor = data_processor or self._process_scan
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meta = self.get_metadata()

    def get_metadata(self):
        self.sock.sendto(bytes(DATA_ID + '\n', 'utf-8'),
                         (self.host, self.port))
        r = self.sock.recv(1024).decode('utf-8').rstrip()
        return self.meta_processor(r)

    def get_data(self):
        self.sock.sendto(bytes(DATA_REQ + '\n', 'utf-8'),
                         (self.host, self.port))
        r = self.sock.recv(1024).decode('utf-8').rstrip()
        r, timestamp = self.data_processor(r)
        return {'scan': r,
                'lidard_timestamp': timestamp,
                'meta': self.meta}

    def _process_metadata(self, data):
        pairs = data[:-1].split(';')
        ret = {}
        for p in pairs:
            k, v = p.split(',')
            ret[k] = v
        return ret

    def _process_scan(self, data):
        scan, timestamp = data[:-1].split('|')
        scan = scan.split(';')
        ret = []
        for p in scan:
            p = p.split(',')
            if len(p) < 2:
                continue
            try:
                p = float(p[0]), float(p[1])
            except:
                continue
            ret.append(p)
        return tuple(p), timestamp


Sensor = Lidard
