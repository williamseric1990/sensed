import time
import struct
import msgpack
import socketserver

DATA_ID = b'\x01\x00'
DATA_REQ = b'\x01\x01'
DATA_ERR = b'\x01\x02'


class SensedServer(socketserver.BaseRequestHandler):
    def handle(self):
        data, host = self.mp_recv()
        if data['header'] == DATA_ID:
            # Metadata request recieved
            packet = {'name': self.server.config['name'],
                      'sensors': list(self.server.config['sensors'].keys())}
            header = DATA_ID
        elif data['header'] == DATA_REQ:
            # Sensor data request recieved
            packet = self.get_sensors(data['body'])
            header = DATA_REQ
        else:
            # Erroneous packet header supplied
            packet = msgpack.pack({'_error': 'Invalid header'})
            header = DATA_ERR

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
