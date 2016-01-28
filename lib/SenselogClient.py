import time
import socket


class SenselogClient(object):
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sensors = {}

        # Load all sensor modules that are enabled
        for sensor in config['sensors']:
            if config['sensors']['sensor']['enabled']:
                self.sensors[sensor] = importlib.import_module('modules.{}'.format(sensor))

    def get_sensor(self, sensor):
        if sensor in self.sensors:
            return self.sensors[sensor].get_data()
        else:
            return None

    def get_sensors(self):
        ret = {}
        for sensor in self.sensors:
            data = self.sensors[sensor].get_data()
            ret[sensor] = data
        return ret

    def send(self, data):
        data = data + '|' + str(int(time.time()))
        data = bytes(data + '\n', 'utf-8')
        self.sock.sendto(data, (self.host, self.port))

    def recv(self):
        data = self.sock.recv(1024).decode('utf-8').rstrip()
        return {'header': data[:2], 'body': data[2:]}

    def shutdown(self):
        self.sock.close()
