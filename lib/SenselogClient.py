import socket


class SenselogClient(object):
    def __init__(self, host, port, sensors={}):
        self.host = host
        self.port = port
        self.sensors = sensors
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_sensor(self, sensor):
        if sensor in self.sensors:
            return self.sensors[sensor].get_data()

    def get_sensors(self):
        ret = {}
        for sensor in self.sensors:
            data = self.sensors[sensor].get_data()
            ret[sensor] = data
        return ret

    def send(self, data):
        data = bytes(data + '\n', 'utf-8')
        self.sock.sendto(data, (self.host, self.port))

    def recv(self):
        data = self.sock.recv(1024).decode('utf-8').rstrip()
        return data
