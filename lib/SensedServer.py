import time
import socket
import importlib
import msgpack

DATA_ID = '\x01\x00'
DATA_REQ = '\x01\x01'
DATA_ERR = '\x01\x02'


class SensedServer(object):
    def setup(self):
        if not '_initialized' in self.__dict__:
            self.initialize()

    def handle(self):
        data = self.mp_recv()
        if data['header'] == DATA_ID:
            # Metadata request recieved
            packet = {'name': self.server.config['name'],
                      'sensors': self.server.config['sensors'].keys()}
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
        self.send_mp(packet, header)

    def get_sensors(self, sensors=[]):
        '''
        Using the configured list of sensors, queries them
        for data. If `sensors` is supplied, only the listed
        sensors will be queried.
        '''
        ret = {'sensors':{}}
        for sensor in self.sensors:
            if len(sensors) > 0 and sensor in sensors:
                data = self.sensors[sensor].get_data()
                ret['sensors'][sensor] = data
        return ret

    def mp_send(self, data, header):
        '''
        Sends data over the UDP socket in MessagePack format.
        First sends a four byte packet representing the size of the
        data to follow.
        '''
        mdata = header + msgpack.packb(data)
        size = struct.pack('I', len(mdata))
        self.sock.sendto(size, (self.host, self.port))
        self.sock.sendto(mdata, (self.host, self.port))

    def mp_recv(self):
        data = self.sock.recv(1024)
        return {'header': data[:2], 'body': msgpack.unpackb(data[2:])}
