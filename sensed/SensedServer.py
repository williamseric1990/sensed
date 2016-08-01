import time
import struct
import msgpack
import socketserver
from Map import Map


HEADERS = Map()
HEADERS.ID = b'\x01\x00'
HEADERS.REQ = b'\x01\x01'
HEADERS.ERR = b'\x01\x02'


class SensedServer(socketserver.BaseRequestHandler):
    def handle(self):
        data, host = self.mp_recv()
        packet = Map()
        if data.header == HEADERS.ID:
            # Metadata request recieved
            sensors = list(self.server.config['sensors'].keys())
            packet = Map({'name': self.server.config['name'],
                          'sensors': sensors})
            header = HEADERS.ID
        elif data.header == HEADERS.REQ:
            # Sensor data request recieved
            packet = self.get_sensors(data['body'])
            header = HEADERS.REQ
        else:
            # Erroneous packet header supplied
            packet = {'_error': 'Invalid header'}
            header = HEADERS.ERR

        packet['timestamp'] = int(time.time())
        self.mp_send(header, packet, host)

    def get_sensors(self, sensors=[]):
        '''
        Using the configured list of sensors, queries them
        for data. If `sensors` is supplied, only the listed
        sensors will be queried.
        '''
        ret = {'sensors':{}}
        for sensor in self.server.sensors:
            if len(sensors) == 0 or sensor in sensors:
                if self.server.config['test'] == True:
                    data = self.server.sensors[sensor].test()
                else:
                    data = self.server.sensors[sensor].get_data()
                ret['sensors'][sensor] = data
        return ret

    def mp_send(self, header, data, host):
        '''
        Sends data over the UDP socket in MessagePack format.
        First sends a four byte packet representing the size of the
        data to follow.
        '''
        mdata = header + msgpack.packb(data)
        if header == DATA_REQ:
            size = struct.pack('I', len(mdata))
            self.request[1].sendto(size, host)
        self.request[1].sendto(mdata, host)

    def mp_recv(self):
        packet = self.request[0]
        host = self.client_address
        header = packet[:2]
        data = packet[2:]
        if len(data) > 0:
            data = msgpack.unpackb(data)
        return {'header': header, 'body': data}, host
