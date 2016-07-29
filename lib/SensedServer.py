import time
import socket
import importlib
import msgpack

DATA_ID = '\x01\x00'
DATA_REQ = '\x01\x01'


class SensedServer(object):
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sensors = {}

        # Load all sensor modules that are enabled
        for sensor in config['sensors']:
            if config['sensors']['sensor']['enabled']:
                smod = importlib.import_module('modules.{}'.format(sensor))
                self.sensors[sensor] = smod.Sensor()

    def get_sensor(self, sensor):
        if sensor in self.sensors:
            data = self.sensors[sensor].get_data()
            data['sensed_ts'] = int(time.time())
            return data
        else:
            return None

    def get_sensors(self):
        ret = {}
        for sensor in self.sensors:
            data = self.sensors[sensor].get_data()
            ret[sensor] = data
        ret['sensed_ts'] = int(time.time())
        return ret

    def send(self, data):
        mdata = msgpack.packb(data)
        self.sock.sendto(mdata, (self.host, self.port))

    def recv(self):
        data = self.sock.recv(1024).decode('utf-8').rstrip()
        return {'header': data[:2], 'body': data[2:]}

    def shutdown(self):
        self.sock.close()
